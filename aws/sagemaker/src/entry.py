import logging
import torch
from transformers import T5ForConditionalGeneration, T5Tokenizer
from datasets import load_from_disk

import os
import argparse
import sys

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler(sys.stdout))

def get_parser():
    parser = argparse.ArgumentParser(
        description="Model Trainer for text-summarization Project Yubaba",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    parser.add_argument("--num_epochs", type=int, default=3)
    parser.add_argument("--learning_rate", type=str, default=5e-5)
    parser.add_argument("--weight_decay", type=str, default=1e-3)
    parser.add_argument("--eps", type=str, default=1-8)
    parser.add_argument("--gradient_accum_steps", type=int, default=8)
    parser.add_argument("--batch_size", type=int, default=2)
    
    # Data, model, and output directories
    parser.add_argument("--output-data-dir", type=str, default=os.environ.get("SM_OUTPUT_DATA_DIR", None))
    parser.add_argument("--model_name", type=str)
    parser.add_argument("--model-dir", type=str, default=os.environ.get("SM_MODEL_DIR", None))
    parser.add_argument("--training_dir", type=str, default=os.environ.get("SM_CHANNEL_TRAIN", None))
    parser.add_argument("--test_dir", type=str, default=os.environ.get("SM_CHANNEL_TEST", None))

    return parser

def save_model(model, model_dir):
    logger.info("Saving the model.")
    path = os.path.join(model_dir, "model.pth")
    # recommended way from http://pytorch.org/docs/master/notes/serialization.html
    torch.save(model.cpu().state_dict(), path)

def t5_train(train_dataset, device: str) -> None:
    model = T5ForConditionalGeneration.from_pretrained('t5-small')
    model.train()
    model = model.to(device)
    save_model(model, args.model_dir)
    
    
    
if __name__ == "__main__":
    parser = get_parser()
    args = parser.parse_args()

        
    device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')
    train_dataset = load_from_disk(args.training_dir)
    data_loader = torch.utils.data.DataLoader(train_dataset, batch_size=args.batch_size, shuffle = True)

    t5_train(train_dataset, device)
