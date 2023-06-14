#!/usr/bin/env python
# coding: utf-8

# In[ ]:
#import dfp_youtube_api_data_processing_final as dfpy
import Youtube_Api_Data_Processing as dfpy
import pandas as pd

#spacy_nlp = spacy.load('en_core_web_sm')
#create list of punctuations and stopwords
#punctuations = string.punctuation
#stop_words = spacy.lang.en.stop_words.STOP_WORDS

df = pd.read_excel('youtube_complete_data_clean.xlsx')
print(df.head())
df1 = pd.DataFrame(df['Summary'])
dfpy.wdcloud(df1)
yt_df=dfpy.search_similar_videos('data science tutorials',df)
print(yt_df)

print(yt_df.info())



