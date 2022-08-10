import torch
import transformers

from transformers import RobertaTokenizerFast
from transformers import T5Tokenizer, T5ForConditionalGeneration
from transformers import EncoderDecoderModel

from typing import Union, List
import argparse
import re

PREFIX_STR = "summarize:"

def t5_inference(model_path:str, input_str:Union[str, List[str]], \
        min_length:int, max_length:int, device: Union[torch.device, int]) -> str:
    
    model = T5ForConditionalGeneration.from_pretrained('t5-small')
    if not re.match(model_path, ""):
        model.load_state_dict(torch.load(model_path))
    model.eval()
    model.to(device)

    t5_tokenizer = T5Tokenizer.from_pretrained('t5-small', model_max_length = max_length)
    inputs = t5_tokenizer.encode(PREFIX_STR + input_str, return_tensors = "pt").to(device)
    summary = model.generate(inputs,
                            num_beams = 4,
                            no_repeat_ngram_size = 4,
                            length_penalty = 2.0,
                            min_length = min_length,
                            max_length = max_length,
                            early_stopping = True,
                            )

    summary = t5_tokenizer.decode(summary[0], skip_special_tokens = True, clean_up_tokenization_spaces = True)
    return summary


def roberta_inference(model_path:str, input_str:Union[str, List[str]], \
        min_length:int, max_length:int, device: Union[torch.device, int]) -> str:
    
    model = EncoderDecoderModel.from_encoder_decoder_pretrained("roberta-base", "roberta-base", tie_encoder_decoder=True)
    if not re.match(model_path, ""):
        model = model.load_state_dict(torch.load(model_path))
    model.config.decoder_start_token_id = tokenizer.bos_token_id                                             
    model.config.eos_token_id = tokenizer.eos_token_id
    model.eval()
    model.to(device)

    tokenizer = RobertaTokenizerFast.from_pretrained("roberta-base")

    inputs = tokenizer(PREFIX_STR + input_str, return_tensors="pt").to(device)
    attention_mask = inputs.attention_mask.to(device)
    inputs = inputs.input_ids.to(device)

    summary = model.generate(inputs, 
                        num_beams = 4,
                        no_repeat_ngram_size = 4,
                        length_penalty = 2.0,
                        attention_mask = attention_mask,
                        min_length = min_length,
                        max_length = max_length,
                        early_stopping = True,
                        )
    summary = tokenizer.batch_decode(summary, skip_special_tokens = True, clean_up_tokenization_spaces = True)
    return summary


MODEL_TYPES = {"t5_base": dict(
                func = t5_inference,
            ), 
            "roberta":dict(
                func = roberta_inference,
            ), 
            "t5_child": dict(
                func = t5_inference,
            ), 
            "roberta_child":dict(
                func = roberta_inference,
            ), 
        }


def summarize(args):
    device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')
    
    for model, dic in MODEL_TYPES.items():
        if re.match(model, args.model_type):
            func = dic["func"]
            return func(args.model_path, args.input_str, args.min_length, args.max_length, device)

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
                    Options: t5_base, roberta, t5_child, roberta_child",
    )
    parser.add_argument(
        "--model_path",
        type = str,
        default = "",
        help = "Path to model .pth file",
    )
    parser.add_argument(
        "--max_length",
        type = int,
        default = 500,
        help = "Maximum length limit of produced summarization",
    )
    parser.add_argument(
        "--min_length",
        type = int,
        default = 20,
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
    summary = summarize(args)

    print(summary)


if __name__ == "__main__":
    main()
