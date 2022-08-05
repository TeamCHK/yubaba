from torch.utils.data import Dataset, DataLoader, RandomSampler, SequentialSampler


class Wikihow(Dataset):
    def __init__(self, dataset, tokenizer, portion = 1.0):
        self.tokenizer = tokenizer
        self.train_size = int(len(dataset) * portion)
        self.dataset = dataset[:self.train_size]

    def __len__(self):
        return len(self.dataset["text"])

    def __getitem__(self, index):
        inputs = self.dataset['text'][index]
        inputs = inputs.strip().replace("\n","")
        
        labels = self.dataset['headline'][index]

        inputs = self.tokenizer.batch_encode_plus([inputs], truncation = True, padding = "max_length", return_tensors = "pt")
        targets = self.tokenizer.batch_encode_plus([labels], truncation = True, padding = "max_length", return_tensors = "pt")

        return {"source_ids": inputs["input_ids"], 
                "source_mask": inputs["attention_mask"],
                "target_ids": targets["input_ids"],
                "target_mask": targets["attention_mask"],
                }

