import re
import sys
import random
import os.path
import datetime
from pathlib import Path
import nltk
import markovify
try:
    import simplejson as json
except:
    import json


path = os.path.dirname(os.path.realpath(__file__))
inputDir = path + '/static/texts/'
outputDir = path + '/static/models/'


def clean_text(text):

    # Strip and replace special characters
    cleaned = text.replace('"', '')
    cleaned = cleaned.replace('”', '"')
    cleaned = cleaned.replace('“', '"')
    cleaned = cleaned.replace('’', "'")
    cleaned = cleaned.replace('‘', "'")
    cleaned = cleaned.replace('#', "'")
    cleaned = cleaned.lower()
    return cleaned

def gen_model(person):
    # Get raw text as string.
    text = ''

    for file in os.listdir(inputDir + person + '/'):
        with open(inputDir + person + '/' + file) as f:
            text += '\n' + f.read()

    cleaned = clean_text(text)

    # Build the model, reject_reg rejects bracketed text
    text_model = markovify.Text(cleaned, state_size=2)#, reject_reg='\[.*?\][ \t\n]*')
    # Turn into json
    model_json = text_model.to_json()
    # Write model to json
    with open(outputDir + person + '_model.json', 'w+') as fpjson:
        json.dump(model_json, fpjson)
    
def load_model(person, word) -> str:
    # Load model from json
    with open(outputDir + person + '_model.json') as fprecon:
        recon_json = json.load(fprecon)
    recon_model = markovify.Text.from_json(recon_json)

    # TODO: testing user input with init_state
    response = recon_model.make_sentence(init_state=(word,''), tries=10, test_output=True, mot=15) # response = recon_model.make_sentence() 
    if response is None:
        out = {
            'username': person,
            'text': "I don't know what to say to that..."
        }
    else:
        out = {
            'username': person,
            'text': response
        }

    return json.dumps(out)
  
def get_text(person, word) -> str:
    myfile = Path(outputDir + person + '_' + 'model.json')
    if myfile.is_file():
        # print('"' + person + '_model.json" exists')
        return load_model(person, word)
    else:
        # print('"' + person + '_model.json" does not exist. Generating model.')
        gen_model(person)
        return load_model(person, word)

def nouns(query) -> str:
    """Grab nouns from query, randomly pick one to be topic.
    If none, return nothing. https://stackoverflow.com/a/33587889
    """
    is_noun = lambda pos: pos[:2] == 'NN'
    seed = str(datetime.datetime.now())[-6:]
    try:
        tokenized = nltk.word_tokenize(query)   # Do the nlp stuff
        nouns_in_query = [word for (word, pos) in nltk.pos_tag(tokenized) if is_noun(pos)]
        random.seed(a=seed)
        word = random.choice(nouns_in_query)
        return word
    except:
        # out = { 'text': "i don't know what to say to that..." }
        # print(json.dumps(out))
        return

def generate_message(person, query) -> str:
    if len(query) == 0:
        out = {
            'username': person,
            'text': 'anyone there? hello?'
        }
        return json.dumps(out)
        
    # Strip and replace special characters for nltk tokenizer
    query = query.replace("'", '')
    query = query.replace('"', '')
    query = query.replace('"', '')
    query = query.replace('”', '')
    query = query.replace('“', '')
    query = query.replace('’', "")
    query = query.replace('‘', "")
    query = query.replace('#', "")
    query = query.lower()
    word = nouns(query)

    if not os.path.exists(outputDir):
        os.mkdir(outputDir)
    try:
        return get_text(person, word)
    except Exception as e:
        print(e)
        return json.dumps({ 
                    "username": person,
                    "text": "Sorry, I'm having trouble understanding you..."
                })
    

def main():
    print(generate_message("iliza", "what do you think about men and women?"))

if __name__ == "__main__":
    main()