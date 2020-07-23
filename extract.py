import io
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.layout import LAParams
from pdfminer.converter import TextConverter
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
import os
from os import listdir
from os.path import isfile, join
import nltk  
import string
from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize
stop_words = set(stopwords.words('english')) 


def pdf_to_text(path):
    with open(path, 'rb') as fp:
        rsrcmgr = PDFResourceManager()
        outfp = io.StringIO()
        laparams = LAParams()
        device = TextConverter(rsrcmgr, outfp, laparams=laparams)
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        for page in PDFPage.get_pages(fp):
            interpreter.process_page(page)
    text = outfp.getvalue()
    return text 

def save_doc(lines, filename):
	data = '\n'.join(lines)
	file = open(filename, 'w')
	file.write(data)
	file.close()

def filter_stop_punctuation(input1):
    if (input1 in stop_words or len(input1)<2):
        return False
    if (not input1.isalpha()):
        return False
    return True

def paragraph_to_tokens(input_para):
    # replace '--' with a space ' '
	input_para = input_para.replace('--', ' ')
	# split into tokens by white space
	tokens = input_para.split()
	# remove punctuation from each token
	table = str.maketrans('', '', string.punctuation)
	tokens = [(w.translate(table)).lower() for w in tokens if filter_stop_punctuation(w.strip())]
	# remove remaining tokens that are not alphabetic
	# tokens = [word for word in tokens if word.isalpha()]
	# make lower case
	# tokens = [word.lower() for word in tokens if filter_stop_punctuation(word.strip())]
	return tokens

target = "pdfs"
final_sequence = list()
for root, dirs, files in os.walk(target, topdown=False):
    for i in files:
        path = root+'/'+i
        if i.endswith(".pdf"):
            pdf_text = pdf_to_text(path)
            tokens = paragraph_to_tokens(pdf_text)
            length = 50 + 1
            sequences = list()
            for i in range(length, len(tokens)):
                # select sequence of tokens
                seq = tokens[i-length:i]
                # convert into a line
                line = ' '.join(seq)
                # store
                sequences.append(line)
            final_sequence += sequences

out_filename = 'republic_sequences.txt'
save_doc(final_sequence, out_filename)