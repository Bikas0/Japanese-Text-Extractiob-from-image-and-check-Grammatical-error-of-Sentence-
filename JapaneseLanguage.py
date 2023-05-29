import re
import cv2 
import spacy
from PIL import Image
from termcolor import colored
from pytesseract import pytesseract
# Defining paths to tesseract.exe
path_to_tesseract = r"C:\Users\hp\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"
img = cv2.imread("images.jpeg")
img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
img = cv2.medianBlur(img, 5)
# Providing the tesseract executable location to pytesseract library
pytesseract.tesseract_cmd = path_to_tesseract
# Passing the image object to image_to_string() function
# This function will extract the text from the image
text = pytesseract.image_to_string(img, lang='jpn')    
#print(text)
with open('output.txt', 'w', encoding='utf-8') as file:
    file.write(text)
def extract_japanese_line(line):
    japanese_pattern = re.compile(r'[\u3040-\u309F\u30A0-\u30FF\u4E00-\u9FAF]+') 
    japanese_text = ''.join(japanese_pattern.findall(line)) # Extract only the Japanese characters
    return japanese_text
text_data = []
with open('output.txt', 'r', encoding='utf-8') as file:
    for line in file:
        japanese_text = extract_japanese_line(line)
        text_data.append(japanese_text)
        #print(japanese_text)
new_list = [x for x in text_data if x != '']
# Load the pre-trained Japanese language model
nlp = spacy.load('ja_core_news_sm')

# Define a function to detect grammatical errors in a sentence
def detect_errors(sentence):
    doc = nlp(sentence)
    errors = []
    for token in doc:
        # Check for incorrect particle usage
        if token.pos_ == 'ADP' and token.text not in ['が', 'を', 'に', 'へ', 'と', 'から', 'より']:
            errors.append(token.text)
        # Check for incorrect verb usage
        elif token.pos_ == 'VERB' and token.tag_ != 'Aux':
            errors.append(token.text)
        # Check for incorrect adjective usage
        elif token.pos_ == 'ADJ' and token.tag_ != 'aux':
            errors.append(token.text)
    return errors
sentence = new_list
error_words = []
for line in sentence:
    errors = detect_errors(line)
    error_words.append(errors)
    if errors:
        print(f"Errors found in '{line}': {', '.join(errors)}\n")
    else:
        print(f"No errors found in '{line}'.")
           
def underline_word(text, word):
    return text.replace(word, colored(word, 'red', attrs=['underline']))

# Test the function on a sample string and word
text= new_list
word = error_words
print("--------------------- Output Result --------------------\n")
for i in range(len(text)):
    for j in range(len(word)):
        new_text = underline_word(text[i], word[i][j])
        print(f'Error found in Text {i} : ', new_text)



