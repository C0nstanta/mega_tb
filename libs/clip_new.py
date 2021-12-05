import os
import torch
import numpy as np
import pandas as pd

from essential_generators import DocumentGenerator
from sentence_transformers import SentenceTransformer, util


class ClipEmbedding:
    def __init__(self):
        self.gen = DocumentGenerator()
        self.text_model = SentenceTransformer('sentence-transformers/clip-ViT-B-32-multilingual-v1')

        file_path = os.getcwd()
        self.vid_emb = pd.read_pickle(file_path + "/raw_data/vid_emb.pickle")
        self.you_ds = pd.read_csv(file_path + '/raw_data/ml-youtube.csv.zip')
        self.movie_title_df = pd.read_csv(file_path + '/raw_data/Movie_Id_Titles.csv')
        self.movie_rating_df = pd.read_csv(file_path + '/raw_data/Movie_Recommender_Dataset.csv.zip')

        self.target_vec, self.correction = self.df_processing()

    def df_processing(self):
        movie_title_df_tmp = pd.merge(self.movie_title_df, self.you_ds.drop(columns=['movieId']), on='title')

        self.vid_emb['youtubeId'] = self.vid_emb['video'].str.split('/').str[-1].str.replace(".mp4", "")
        self.vid_emb = self.vid_emb.merge(movie_title_df_tmp, on='youtubeId').drop(columns=['video'])
        self.vid_emb['corpus_id'] = list(range(self.vid_emb.shape[0]))
        # self.vid_emb.to_csv('data/vid_emb.csv', index=False)

        target_vec = torch.cat([torch.from_numpy(np.array([i])) for i in self.vid_emb.vid_emb.values])
        shit = [self.gen.word().lower() for i in range(5000)] + [self.gen.sentence().lower().replace(".", "")\
                                                                     .replace(",", "") for i in range(5000)]
        correction = self.text_model.encode(shit, show_progress_bar=True).mean(0)
        return target_vec, correction

    def get_recommend(self, input_text, top=5):
        input_vec = self.text_model.encode([input_text])

        df = pd.DataFrame(
            util.semantic_search(
                input_vec - self.correction,
                self.target_vec - self.correction,
                top_k=top)[0]).merge(self.vid_emb, on='corpus_id')

        df = df.loc[:, ['title', 'score', 'youtubeId']]
        return df