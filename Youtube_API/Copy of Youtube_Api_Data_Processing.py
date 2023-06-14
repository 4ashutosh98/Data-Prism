#pip install tensorflow
#pip install rake_nltk
#pip install gensim
#pip install wordcloud
#pip install spacy
#pip install nltk (nltk.download('punkt'),nltk.download('stopwords'))
#pip install https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-3.2.0/en_core_web_sm-3.2.0-py3-none-any.whl 
#conda install -c huggingface transformers 

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from rake_nltk import Rake
import spacy
import string
import re
from wordcloud import WordCloud
from gensim import corpora
import gensim
from gensim.similarities import MatrixSimilarity
from operator import itemgetter

# Tokenizing and Cleaning Function
def spacy_tokenizer(sentence):

    # Removing distracting single quotes
    sentence = re.sub('\'','',sentence)

    # Removing digits adnd words containing digits
    sentence = re.sub('\w*\d\w*','',sentence)

    # Replacing extra spaces with single space
    sentence = re.sub(' +',' ',sentence)

    # Removing unwanted lines starting from special charcters
    sentence = re.sub(r'\n: \'\'.*','',sentence)
    sentence = re.sub(r'\n!.*','',sentence)
    sentence = re.sub(r'^:\'\'.*','',sentence)

    # Removing non-breaking new line characters
    sentence = re.sub(r'\n',' ',sentence)

    # Removing punctunations
    sentence = re.sub(r'[^\w\s]',' ',sentence)

    # Creating token object
    tokens = spacy_nlp(sentence)

    # Lowercasing, striping and lemmatizing
    tokens = [word.lemma_.lower().strip() if word.lemma_ != "-PRON-" else word.lower_ for word in tokens]

    # Removing stopwords, and exclude words less than 2 characters
    tokens = [word for word in tokens if word not in stop_words and word not in punctuations and len(word) > 2]

    return tokens

# Semantic Search Function using NLP - Tf_Idf and LSI Model.
def search_similar_videos(search_term,df):
    
    summ = pd.DataFrame(df['Summary'])
    summ['caption_summary_tokenized'] = summ['Summary'].map(lambda x: spacy_tokenizer(x))
    summ1 = summ['caption_summary_tokenized']
    
    dictionary = corpora.Dictionary(summ1)
    # Filtering out terms which occurs in less than 4 documents and more than 20% of the documents.
    dictionary.filter_extremes(no_below=4, no_above=0.2) 
    
    corpus = [dictionary.doc2bow(desc) for desc in summ1]
               
    caption_tfidf_model = gensim.models.TfidfModel(corpus, id2word=dictionary)
    caption_lsi_model = gensim.models.LsiModel(caption_tfidf_model[corpus], id2word=dictionary, num_topics=300)

    gensim.corpora.MmCorpus.serialize('caption_tfidf_model_mm', caption_tfidf_model[corpus])
    gensim.corpora.MmCorpus.serialize('caption_lsi_model_mm',caption_lsi_model[caption_tfidf_model[corpus]])

    # Loading the indexed corpus
    caption_lsi_corpus = gensim.corpora.MmCorpus('caption_lsi_model_mm')

    caption_index = MatrixSimilarity(caption_lsi_corpus, num_features = caption_lsi_corpus.num_terms)

    query_bow = dictionary.doc2bow(spacy_tokenizer(search_term))
    query_tfidf = caption_tfidf_model[query_bow]
    query_lsi = caption_lsi_model[query_tfidf]

    caption_index.num_best = 10

    captions_list = caption_index[query_lsi]

    captions_list.sort(key=itemgetter(1), reverse=True)
    caption_videos = []

    for j, caption in enumerate(captions_list):
        caption_videos.append (
            {
                'Relevance': round((caption[1] * 100),2),
                'Title': df['Title'][caption[0]],
                'Likes':  df['Like_Count'][caption[0]],
                'Comments': df['Comments'][caption[0]],
                'Views': df['View_Count'][caption[0]],
                'Channel': df['Channel_Title'][caption[0]],
                'Link': df['Video_Link'][caption[0]],
                'Duration': df['Duration'][caption[0]],
                'Int_Duration': df['Int_Duration'][caption[0]],
                'Publish_Date': df['Publish_Time'][caption[0]],
                'Comment_Count': df['Comment_Count'][caption[0]],
                'Summary': df['Summary'][caption[0]]
            }

        )
        if j == (caption_index.num_best-1):
            break

    return pd.DataFrame(caption_videos, columns=['Relevance','Title','Likes', 'Comments','Views','Channel','Link','Duration','Int_Duration',
                                                'Publish_Date','Comment_Count','Summary'])

# Function for creating a WordCloud 
def wdcloud(summ):
    summ['caption_summary_tokenized'] = summ.iloc[:,0].map(lambda x: spacy_tokenizer(x))
    summ1 = summ['caption_summary_tokenized']
    series = pd.Series(np.concatenate(summ1)).value_counts()[:100]
    wordcloud = WordCloud(background_color='white').generate_from_frequencies(series)

    plt.figure(figsize=(10,8), facecolor = None)
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.show()


spacy_nlp = spacy.load('en_core_web_sm')

# Creating a list of punctuations and stopwords
punctuations = string.punctuation
stop_words = spacy.lang.en.stop_words.STOP_WORDS


if __name__ == '__main__':
    
    
    # Importing Youtube Video Data (Raw & Clean) obtained from Scraping. 
    df = pd.read_excel('youtube_output_raw.xlsx')
    print(df.head())

    df1 = pd.read_excel('youtube_output_cleaned.xlsx')
    print(df1.head())

    df.columns

    df.drop(['Unnamed: 0'], axis=1,inplace = True)
    df1.drop(['Unnamed: 0'], axis=1,inplace = True)


    # Importing Caption Summary obtained from Summary Generator.
    summ = pd.read_excel('youtube_output_caption_summary.xlsx')

    summ.drop(['Unnamed: 0'], axis=1,inplace = True)

    cc = summ.values.tolist()

    cc1 = []
    for i in range(len(cc)):
        x = ' '.join([str(x) for x in cc[i]])
        x1 = x[7:len(x) - 4]
        cc1.append(x1)

    summ = pd.DataFrame(cc1)
        

    # Converting Duration String to Integer Duration in Seconds.
    int_dur = []
    for x in df1['Duration']:
        pos = 0
        h = ""
        m = ""
        s = ""
        for i in range((len(x)-1),-1,-1):
            if x[i] != ':' and pos == 0:
                s =  s + x[i]
            elif x[i] != ':' and pos == 1: 
                m =  m + x[i]
            elif x[i] != ':' and pos == 2: 
                h =  h + x[i]
            else:
                pos = pos + 1
    
        if len(h) != 0:
            h = h[::-1]
            h1 = float(h) * 3600
        else:
            h1 = 0
        
        if len(m) != 0:
            m = m[::-1]
            m1 = float(m) * 60
        else:
            m1 = 0
        
        if len(s) != 0:
            s = s[::-1]
            s1 = float(s) 
        else:
            s1 = 0
        
        int_dur.append(h1+m1+s1)
        

    # Generating Tags/Keywords for the Videos based on Caption Summary.
    rake_nltk_var = Rake()

    tags = []
    for x in cc1:
        rake_nltk_var.extract_keywords_from_text(x)
        keyword_extracted = rake_nltk_var.get_ranked_phrases()[:10]
        keyword_extracted = list(set(keyword_extracted))
        tags.append(keyword_extracted)


    # Generating Video based on Video - ID.
    video_link = []
    link = "https://youtu.be/"
    for x in df['Video_ID']:
        video_link.append(link+x)
        

    # Adding and Exporting the new Columns in the Main Dataframes.
    df1['Summary'] = cc1
    df1['Video_Link'] = video_link
    df1['Tags'] = tags
    df1['Int_Duration'] = int_dur
    df['Summary'] = cc1
    df['Video_Link'] = video_link
    df['Tags'] = tags
    df['Int_Duration'] = int_dur
    
    df.to_excel('youtube_complete_data_raw.xlsx')
    df1.to_excel('youtube_complete_data_clean.xlsx')
    
    
    # Semantic Search using NLP.
    df2 = pd.DataFrame(df1['Summary'])
    wdcloud(df2)
    print(search_similar_videos('data science tutorials',df))

