import torch
import transformers
# Tokenizer
from transformers import RobertaTokenizerFast
# Encoder-Decoder Model
from transformers import EncoderDecoderModel
from typing import Union, List

# Input string can be a string, or a list of strings
input_str = "Hello my name is Hyukjae Kwark. I am a CMU student who graduated in 2022 working on a chrome extension project for children using RoBERTa."
input_strs = [input_str, input_str, input_str, input_str]

model_path = "./models/"
device = "cuda" if torch.cuda.is_available() else "cpu"

def main(input_str: Union[str, List[str] ], model_path: str, device = "cpu"):

    model = EncoderDecoderModel.from_pretrained(model_path)
    tokenizer = RobertaTokenizerFast.from_pretrained("roberta-base")
    model.to(device)
    batch_size = 256

    inputs = tokenizer(input_str, padding="max_length", truncation=False, max_length=40, return_tensors="pt")
    input_ids = inputs.input_ids.to(device)
    attention_mask = inputs.attention_mask.to(device)
    outputs = model.generate(input_ids, attention_mask=attention_mask)
    # all special tokens including will be removed
    output_str = tokenizer.batch_decode(outputs, skip_special_tokens=True)
    
    print(output_str)




main(input_str, model_path, device)
