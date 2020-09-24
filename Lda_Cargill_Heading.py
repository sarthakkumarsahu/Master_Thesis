from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.tokenize import sent_tokenize
import string
import pandas as pd
import os
import re
import gensim
from gensim import corpora
os.chdir("C:\\Users\\sarth\\PycharmProjects\\Big_Data_Analysis_Project\\Master_Thesis")

stop = set(stopwords.words('english'))
exclude = set(string.punctuation)
lemma = WordNetLemmatizer()
def clean(doc):
    stop_free = " ".join([i for i in doc.lower().split() if i not in stop])
    punc_free = ''.join(ch for ch in stop_free if ch not in exclude)
    num_free = ''.join([num for num in punc_free if not num.isdigit()])
    normalized = " ".join(lemma.lemmatize(word) for word in num_free.split())
    return normalized

input_file = pd.read_excel(r'master_file_cargill.xlsx')

lda_output = pd.DataFrame()
lda_output['Id'] = ""
lda_output['Date'] = ""
lda_output['Url'] = ""
lda_output['Topic_Heading'] = ""


for i in range(len(input_file)):
    input_text = [input_file.iloc[i,3]]
    print(input_file.iloc[i,0])
    #input_text = input_text.replace(u'\xa0', u' ')

    doc_clean = [clean(doc).split() for doc in input_text]
    if len(doc_clean)==0:
        continue
    print(input_text)
    # Importing Gensim


    # Creating the term dictionary of our courpus, where every unique term is assigned an index.
    dictionary = corpora.Dictionary(doc_clean)

    # Converting list of documents (corpus) into Document Term Matrix using dictionary prepared above.
    doc_term_matrix = [dictionary.doc2bow(doc) for doc in doc_clean]

    # Creating the object for LDA model using gensim library
    Lda = gensim.models.ldamodel.LdaModel

    # Running and Trainign LDA model on the document term matrix.
    ldamodel = Lda(doc_term_matrix, num_topics=1, id2word = dictionary, passes=10, per_word_topics=True)

    topics = ldamodel.print_topics(num_topics=1, num_words=1)

    for topic in topics:
        topic = ' '.join(re.findall(r'"(.*?)"', topic[1]))
        #print(topic)
        temp_dic = {'Id':input_file.iloc[i,0],'Date':input_file.iloc[i,2],'Url':input_file.iloc[i,1],'Topic_Heading':topic}
        lda_output = lda_output.append(temp_dic, ignore_index=True)

#lda_output.to_csv(r"lda_output_head_cargill.csv",index=None, header=True)
lda_output.to_excel(r"lda_output_head_cargill.xlsx",index=None, header=True)