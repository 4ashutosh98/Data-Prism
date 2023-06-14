#pip install transformers
#pip install sentence-transformers
#pip install protobuf==3.19.6

import pandas as pd
import transformers
from transformers import BartTokenizer, BartForConditionalGeneration

df = pd.read_excel('youtube_output_raw.xlsx')
df.head()
df.drop(['Unnamed: 0'], axis=1,inplace = True)

# Model of size 1.65 GB needs to be downloaded
tokenizer = BartTokenizer.from_pretrained('facebook/bart-large-cnn')
model = BartForConditionalGeneration.from_pretrained('facebook/bart-large-cnn')
    
# Takes about 6-7 hours 
summarised_cap = [] 
for i in range(len(df)):
    input_tensor = tokenizer.encode(df['Captions'][i], return_tensors="pt", max_length=512)
    outputs_tensor = model.generate(input_tensor, max_length=160, min_length=120, length_penalty=2.0, num_beams=4, early_stopping=True)
    summarised_cap.append(tokenizer.decode(outputs_tensor[0]))
        
s = pd.DataFrame(summarised_cap)
s.to_excel('youtube_output_caption_summary.xlsx')






