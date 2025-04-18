from torch.utils.data import Dataset
from tqdm import tqdm
import numpy as np
import torch

class SentenceDataset(Dataset):
    """
    Our custom PyTorch Dataset, for preparing strings of text (sentences)
    What we have to do is to implement the 2 abstract methods:

        - __len__(self): in order to let the DataLoader know the size
            of our dataset and to perform batching, shuffling and so on...

        - __getitem__(self, index): we have to return the properly
            processed data-item from our dataset with a given index
    """
    MAX_LEN = 8

    def __init__(self, X, y, word2idx):
        """
        In the initialization of the dataset we will have to assign the
        input values to the corresponding class attributes
        and preprocess the text samples

        -Store all meaningful arguments to the constructor here for debugging
         and for usage in other methods
        -Do most of the heavy-lifting like preprocessing the dataset here


        Args:
            X (list): List of training samples
            y (list): List of training labels
            word2idx (dict): a dictionary which maps words to indexes
        """

        # EX2
        self.labels = y
        self.word2idx = word2idx

        # Basic tokenization: split each sentence by space
        print("\n[INFO] Tokenizing dataset...")
        self.data = [sentence.lower().split() for sentence in tqdm(X)]

        # Debug: print first 10 tokenized examples
        print("\n[INFO] First 10 tokenized examples:")
        for i in range(min(10, len(self.data))):
            print(self.data[i])

        print("\n[INFO] First 5 examples after encoding and padding:")
        for i in range(5):
            ex, lbl, ln = self.__getitem__(i)
            print(f"Original: {self.data[i]}")
            print(f"Encoded: {ex.tolist()}, Label: {lbl.item()}, Length: {ln.item()}\n")
    

    def __len__(self):
        """
        Must return the length of the dataset, so the dataloader can know
        how to split it into batches

        Returns:
            (int): the length of the dataset
        """

        return len(self.data)

    def __getitem__(self, index):
        """
        Returns the _transformed_ item from the dataset

        Args:
            index (int):

        Returns:
            (tuple):
                * example (ndarray): vector representation of a training example
                * label (int): the class label
                * length (int): the length (tokens) of the sentence

        Examples:
            For an `index` where:
            ::
                self.data[index] = ['this', 'is', 'really', 'simple']
                self.target[index] = "neutral"

            the function will have to return something like:
            ::
                example = [  533  3908  1387   649   0     0     0     0]
                label = 1
                length = 4
        """

        # EX3
        tokens = self.data[index]
        label = self.labels[index]

        # Get the index for unknown tokens
        unk_idx = self.word2idx.get("<unk>")  # it's guaranteed to exist by load_word_vectors()
        pad_idx = 0  # index 0 is always used for padding

        # Map each token to its index in word2idx
        indexed = [self.word2idx.get(word, unk_idx) for word in tokens]

        # Truncate or pad to MAX_LEN
        length = min(len(indexed), self.MAX_LEN)
        if len(indexed) < self.MAX_LEN:
            indexed += [pad_idx] * (self.MAX_LEN - len(indexed))
        else:
            indexed = indexed[:self.MAX_LEN]

        # Convert everything to tensors
        example = torch.tensor(indexed, dtype=torch.long)
        label = torch.tensor(label, dtype=torch.long)
        length = torch.tensor(length, dtype=torch.long)

        return example, label, length    
            
