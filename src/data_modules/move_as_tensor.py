from torch.utils.data import Dataset
import torch
from board_representation.board_representation_2 import move_to_tensor
# from board_representation.sentimate import convert_move
import board_representation.sentimate as br_sentimate
import pandas as pd
import multiprocessing as mp


# def _move_to_tensor_tuple(move):
#     return move_to_tensor(move[0], move[1])


class MoveAsTensorDataset(Dataset):
    def __init__(self, moves_df: pd.DataFrame, position_col="position", move_col="move", sentiment_col="sentiment", convert_fn = br_sentimate.move_to_tensor):
        self.sentiments = [torch.tensor([s], dtype=torch.float16) for s in moves_df[sentiment_col]]
        self.moves_df = moves_df
        moves_tuples = list(zip(moves_df[position_col], moves_df[move_col]))
        # self.moves = list(map(_move_to_tensor_tuple, moves_tuples))
        self.moves = list(map(lambda move: convert_fn(move[0], move[1]), moves_tuples))


    def __getitem__(self, index):
        return self.moves[index], self.sentiments[index]

    def __len__(self):
        return len(self.sentiments)
    

class MoveAsTensorDatasetOnlineTransform(Dataset):
    def __init__(self, moves_df: pd.DataFrame, position_col="position", move_col="move", sentiment_col="sentiment", convert_fn = br_sentimate.move_to_tensor):
        self.sentiments = [torch.tensor([s], dtype=torch.float16) for s in moves_df[sentiment_col]]
        self.moves_df = moves_df
        self.moves_tuples = list(zip(moves_df[position_col], moves_df[move_col]))
        self.convert_fn = convert_fn

    def __getitem__(self, index):
        return self.convert_fn(self.moves_tuples[index][0], self.moves_tuples[index][1]), self.sentiments[index]

    def __len__(self):
        return len(self.sentiments)