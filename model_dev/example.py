import datasets
import torch
import transformers
import pandas as pd
from datasets import Dataset

# Tokenizer
from transformers import RobertaTokenizerFast

# Encoder-Decoder Model
from transformers import EncoderDecoderModel

# Training 
from seq2seq_trainer import Seq2SeqTrainer
from transformers import Seq2SeqTrainingArguments
from dataclasses import dataclass, field
from typing import Optional


# This is a sample tutorial for RoBERTa fine-tuning
# This code is based on tutorial by
# https://github.com/facebookresearch/fairseq/blob/main/examples/roberta/README.pretraining.md 
# https://anubhav20057.medium.com/step-by-step-guide-abstractive-text-summarization-using-roberta-e93978234a90

DATA_PATH = "../../datasets/amazon_reviews/Reviews.csv"

df = pd.read_csv(DATA_PATH)
df.drop(columns=['Id', 'ProductId', 'UserId', 'ProfileName', 'HelpfulnessNumerator','HelpfulnessDenominator', 'Score', 'Time'],axis=1,inplace=True)
df = df.dropna()
print("Data size: ", len(df))
print(df.head())

train = Dataset.from_pandas(df[:550000])
val = Dataset.from_pandas(df[550000:555000])
test = Dataset.from_pandas(df[556000:557000])

print("-----------------Data Loading---------------------")

tokenizer = RobertaTokenizerFast.from_pretrained("roberta-base")
tokenizer.bos_token = tokenizer.cls_token
tokenizer.eos_token = tokenizer.sep_token

batch_size = 256
encoder_max_length = 40
decoder_max_length = 8

def process_data_to_model_inputs(batch):
  # tokenize the inputs and labels
  inputs = tokenizer(batch["Text"], padding="max_length", truncation=True, max_length=encoder_max_length)
  outputs = tokenizer(batch["Summary"], padding="max_length", truncation=True, max_length=decoder_max_length)

  batch["input_ids"] = inputs.input_ids
  batch["attention_mask"] = inputs.attention_mask
  batch["decoder_input_ids"] = outputs.input_ids
  batch["decoder_attention_mask"] = outputs.attention_mask
  batch["labels"] = outputs.input_ids.copy()

  # because RoBERTa automatically shifts the labels, the labels correspond exactly to `decoder_input_ids`. 
  # We have to make sure that the PAD token is ignored
  batch["labels"] = [[-100 if token == tokenizer.pad_token_id else token for token in labels] for labels in batch["labels"]]

  return batch

print("----------------- Data Mapping --------------------")

# Processing training data
train = train.map(
    process_data_to_model_inputs, 
    batched=True, 
    batch_size=batch_size, 
    remove_columns=["Text", "Summary"]
)
train.set_format(
    type="torch", columns=["input_ids", "attention_mask", "decoder_input_ids", "decoder_attention_mask", "labels"],
)

# Processing validation data
val = val.map(
    process_data_to_model_inputs, 
    batched=True, 
    batch_size=batch_size, 
    remove_columns=["Text", "Summary"]
)
val.set_format(
    type="torch", columns=["input_ids", "attention_mask", "decoder_input_ids", "decoder_attention_mask", "labels"],
)

print("---------------------Model Loading---------------------")
# Load Pretrained Model
roberta_shared = EncoderDecoderModel.from_encoder_decoder_pretrained("roberta-base", "roberta-base", tie_encoder_decoder=True)

# set special tokens
roberta_shared.config.decoder_start_token_id = tokenizer.bos_token_id                                             
roberta_shared.config.eos_token_id = tokenizer.eos_token_id

# sensible parameters for beam search
# set decoding params                               
roberta_shared.config.max_length = 40
roberta_shared.config.early_stopping = True
roberta_shared.config.no_repeat_ngram_size = 3
roberta_shared.config.length_penalty = 2.0
roberta_shared.config.num_beams = 4
roberta_shared.config.vocab_size = roberta_shared.config.encoder.vocab_size

print("Hello World")


# load rouge for validation
rouge = datasets.load_metric("rouge")

def compute_metrics(pred):
    labels_ids = pred.label_ids
    pred_ids = pred.predictions

    # all unnecessary tokens are removed
    pred_str = tokenizer.batch_decode(pred_ids, skip_special_tokens=True)
    labels_ids[labels_ids == -100] = tokenizer.pad_token_id
    label_str = tokenizer.batch_decode(labels_ids, skip_special_tokens=True)

    rouge_output = rouge.compute(predictions=pred_str, references=label_str, rouge_types=["rouge2"])["rouge2"].mid

    return {
        "rouge2_precision": round(rouge_output.precision, 4),
        "rouge2_recall": round(rouge_output.recall, 4),
        "rouge2_fmeasure": round(rouge_output.fmeasure, 4),
    }



training_args = Seq2SeqTrainingArguments(
    output_dir="./outputs",
    per_device_train_batch_size=batch_size,
    per_device_eval_batch_size=batch_size,
    predict_with_generate=True,
    do_train=True,
    do_eval=True,
    logging_steps=2, 
    save_steps=16, 
    eval_steps=500, 
    warmup_steps=500, 
    num_train_epochs=3.0,
    overwrite_output_dir=True,
    save_total_limit=1,
    fp16=True, 
)


# instantiate trainer
trainer = Seq2SeqTrainer(
    model=roberta_shared,
    args=training_args,
    compute_metrics=compute_metrics,
    train_dataset=train,
    eval_dataset=val,
)

trainer.train()