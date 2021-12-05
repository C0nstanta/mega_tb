import os
import torch
import numpy as np
import pandas as pd
from re import findall
from PIL import Image

from essential_generators import DocumentGenerator
from sentence_transformers import SentenceTransformer, util


class ClipEmbedding:
    def __init__(self):
        self.img_model = SentenceTransformer('clip-ViT-B-32')
        self.text_model = SentenceTransformer('sentence-transformers/clip-ViT-B-32-multilingual-v1')

        file_path = os.getcwd()
        self.vid_emb = pd.read_csv(file_path + "/raw_data/vid_emb.csv")

    def get_embedding(self, text):
        text_embeddings = self.text_model.encode([text]).mean(0).astype('double')

        if self.load_vid_emb():
            cos_sim_array = self.simple_compute_cos_sim(text_embeddings)
            cos_sim_array
        return text_embeddings

    def load_vid_emb(self):
        if self.vid_emb is not None:
            self.vid_emb['vid_emb'] = self.vid_emb['vid_emb'].apply(self.get_emb_arr)
        return True

    def get_emb_arr(self, s):
        return np.array([float(x) for x in s.replace("\n", "")[2:-2].split(" ") if x]).astype('double')

    def simple_compute_cos_sim(self, text_embeddings):
        cos_sim_list = []
        for img_embed in self.vid_emb['vid_emb']:
            cos_sim_list.append(util.cos_sim(img_embed, text_embeddings))
        max_idx = np.array(cos_sim_list).argmax()

        return max_idx





