import os
import numpy as np
import pandas as pd
import torch
import torch.nn.functional as F


from transformers import T5Tokenizer, T5ForConditionalGeneration, BartTokenizer, BartForConditionalGeneration
from torch import cuda
from nlp import load_dataset
from datasets.wikihow import Wikihow

import yaml
import argparse
import re

def get_t5_tokenizer(max_length):
    return T5Tokenizer.from_pretrained('t5-small', model_max_length = max_length)

def get_bart_tokenizer(max_length):
    # TODO: implement BART tokenizer
    return BartTokenizer.from_pretrained('bart', model_max_length = max_length)

def wikihow_dataset(cfg: dict, tokenizer):
    dataset = load_dataset("wikihow", "all", data_dir = cfg["data_dir"])
    dataset = Wikihow(dataset["train"], tokenizer, cfg["portion"])
    return dataset

def t5_train(cfg: dict, train_loader, num_workers: int, device: str) -> None:
    model = T5ForConditionalGeneration.from_pretrained('t5-small')
    model.train()
    model = model.to(device)

    if not re.match(cfg["model_path"], ""):
        model.load_state_dict(torch.load(model_path))

    optimizer = torch.optim.AdamW(model.parameters(), lr = cfg["learning_rate"], eps = cfg["eps"], weight_decay = cfg["weight_decay"])
    scheduler = torch.optim.lr_scheduler.ExponentialLR(optimizer, gamma = 0.9)
    steps = 0
    num_epochs = cfg["num_epochs"]
    optimizer.zero_grad()
    for epoch in range(num_epochs):
        for i, batch in enumerate(train_loader):
            output = model(input_ids = batch["source_ids"].to(device), 
                attention_mask = batch["source_mask"].to(device),
                labels =  batch["target_ids"].to(device),
                decoder_attention_mask = batch['target_mask'].to(device),
            )
            loss = output[0]
            loss.backward()
            steps += 1
            
            if (cfg["gradient_accum_steps"] is not None and steps >= cfg["gradient_accum_steps"]):
                steps = 0
                optimizer.step()
                optimizer.zero_grad()
        
        lr_scheduler.step()
    
def bart_train(cfg: dict, train_loader, num_workers: int, device: str) -> None:
    # TODO implement bart train
    return


MODEL_TYPES = {"t5_base": dict(
                train_func = t5_train,
                tokenizer = get_t5_tokenizer,
            ), 
            "bart":dict(
                train_func = bart_train,
                tokenizer = BartTokenizer,
            ), 
            "t5_child": dict(
                train_func = t5_train,
                tokenizer = T5Tokenizer,
            ), 
            "bart_child":dict(
                train_func = bart_train,
                tokenizer = BartTokenizer,
            ), 
        }

DATASETS = {'wikihow': dict(
                func = wikihow_dataset,
            ),
        }


def data_loader(cfg: dict, tokenizer, batch_size):
    for dataset, dic in DATASETS.items():
        if re.match(dataset, cfg["name"]):
            func = dic["func"]
            dataset = func(cfg, tokenizer)
            return torch.utils.data.DataLoader(dataset, batch_size = batch_size, shuffle = True)

    raise RuntimeError(f"Not supported: dataset type={cfg.dataset}")


def get_parser():
    parser = argparse.ArgumentParser(
        description="Model Trainer for text-summarization Project Yubaba",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--config_path", 
        type = str, 
        default = "./configs/wikihow_t5.yaml",
        help = "Model type to use for text summarization. Currently supports t5-small and roberta models \
                    Options: t5_base, roberta, t5_child, roberta_child",
    )
    parser.add_argument(
        "--num_workers", 
        type = int, 
        default = 1,
        help = "Number of gpu/cpu workers available for training",
    )
    return parser

def main():
    parser = get_parser()
    args = parser.parse_args()

    with open(args.config_path, "r") as f:
        config = yaml.load(f, Loader=yaml.FullLoader)
        
    device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')
    
    for model, dic in MODEL_TYPES.items():
        if re.match(model, config["model"]["name"]):
            train_func = dic["train_func"]
            get_tokenizer = dic["tokenizer"]
            train_loader = data_loader(config["dataset"], 
                                        get_tokenizer(config["tokenizer"]["max_length"]), 
                                        config["train"]["batch_size"], 
                                    )
            train_func(config["train"], train_loader, args.num_workers, device)



if __name__ == "__main__":
    main()
