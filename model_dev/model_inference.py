import torch
import transformers

from transformers import RobertaTokenizerFast
from transformers import T5Tokenizer, T5ForConditionalGeneration
from transformers import EncoderDecoderModel
from transformers import BartTokenizer, BartForConditionalGeneration

from typing import Union, List
import argparse
import re
import logging
import time

PREFIX_STR = "summarize: "
logging.basicConfig(level = logging.INFO)
logger = logging.getLogger("[Model Inference]")

def t5_inference(model_type: str, model_path:str, input_str: str, \
        min_length:int, max_length:int, device: Union[torch.device, int]) -> str:
    
    model = T5ForConditionalGeneration.from_pretrained('t5-small')
    if not re.match(model_path, ""):
        model.load_state_dict(torch.load(model_path))
    model.eval()
    model.to(device)

    tokenizer = T5Tokenizer.from_pretrained('t5-small', model_max_length = max_length)

    inputs = tokenizer.encode(PREFIX_STR + input_str, return_tensors = "pt").to(device)
    summary = model.generate(inputs,
                            num_beams = 4,
                            no_repeat_ngram_size = 2,
                            length_penalty = 2.0,
                            min_length = min_length,
                            max_length = max_length,
                            early_stopping = True,
                            )
    summary = tokenizer.decode(summary[0], skip_special_tokens = True, clean_up_tokenization_spaces = True)
    return summary


def bart_inference(model_type: str, model_path:str, input_str: str, \
        min_length:int, max_length:int, device: Union[torch.device, int]) -> str:
    
    if re.match(model_type, "bart_cnn"):
        model = BartForConditionalGeneration.from_pretrained("sshleifer/distilbart-cnn-12-6")
        tokenizer = BartTokenizer.from_pretrained("sshleifer/distilbart-cnn-12-6")
    else:
        model = BartForConditionalGeneration.from_pretrained("facebook/bart-large-cnn")
        tokenizer = BartTokenizer.from_pretrained("facebook/bart-large-cnn", model_max_length = max_length)

    if not re.match(model_path, ""):
        model.load_state_dict(torch.load(model_path))

    model.eval()
    model.to(device)

    inputs = tokenizer.encode(input_str, return_tensors = "pt").to(device)
    summary = model.generate(inputs,
                            num_beams = 4,
                            no_repeat_ngram_size = 2,
                            length_penalty = 2.0,
                            min_length = min_length,
                            max_length = max_length,
                            early_stopping = True,
                            )
    
    summary = tokenizer.decode(summary[0], skip_special_tokens = True, clean_up_tokenization_spaces = True)
    return summary


MODEL_TYPES = {"t5_base": dict(
                func = t5_inference,
            ), 
            "t5_child": dict(
                func = t5_inference,
            ),
            "bart_base":dict(
                func = bart_inference,
            ),  
            "bart_child":dict(
                func = bart_inference,
            ), 
            "bart_cnn":dict(
                func = bart_inference,
            ), 
        }


def summarize(args):
    device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')
    logger.info("Running on device: {}".format(device))
    
    for model, dic in MODEL_TYPES.items():
        if re.match(model, args.model_type):
            func = dic["func"]
            return func(args.model_type, args.model_path, args.input_str, args.min_length, args.max_length, device)

    raise RuntimeError(f"Not supported: model type={args.model_type}")


def get_parser():
    parser = argparse.ArgumentParser(
        description="Model Inference for text-summarization Project Yubaba",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--model_type", 
        type = str, 
        default = "t5_base",
        help = "Model type to use for text summarization. Currently supports t5-small and roberta models \
                    Options: t5_base, bart, t5_child, bart_cnn, bart_child",
    )
    parser.add_argument(
        "--model_path",
        type = str,
        default = "",
        help = "Path to model .pth file to use a pretrained model",
    )
    parser.add_argument(
        "--max_length",
        type = int,
        default = 1024,
        help = "Maximum length limit of produced summarization",
    )
    parser.add_argument(
        "--min_length",
        type = int,
        default = 0,
        help = "Minimum length limit of produced summarization",
    )
    parser.add_argument(
        "--input_str",
        type = str,
        required = True,
        help = "Input String to summarize",
    )
    return parser


def main():
    parser = get_parser()
    args = parser.parse_args()
    start_time = time.time()    
    summary = summarize(args)
    logger.info("Time for Generating Summary : {:.4f} secs".format(time.time() - start_time))

    print(summary)


if __name__ == "__main__":
    main()
