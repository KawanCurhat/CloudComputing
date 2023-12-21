import warnings
warnings.filterwarnings("ignore")
import nltk
nltk.download('punkt')
nltk.download('wordnet')
from nltk.stem import WordNetLemmatizer
import json
import pickle
import numpy as np
import random
import functions_framework
from keras.models import load_model

model = load_model('chatbot.h5')
intents = json.loads(open("intents.json").read())
words = pickle.load(open('words.pkl','rb'))
classes = pickle.load(open('classes.pkl','rb'))

def clean_up_sentence(sentence):
  sentence_words = nltk.word_tokenize(sentence)
  sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
  return sentence_words

def bow(sentence, words, show_details=True):
  sentence_words = clean_up_sentence(sentence)
  bag = [0]*len(words)
  for s in sentence_words:
    for i, w in enumerate(words):
      if w == s:
        bag[i] = 1
        if show_details:
          print("found in bag: %s" %w)
  return(np.array(bag))

def predict_class(sentence, model):
  p = bow(sentence, words, show_details=False)
  res = model.predict(np.array([p]))[0]
  error = 0.25
  results = [[i, r] for i, r in enumerate(res) if r>error]

  results.sort(key=lambda x:[1], reverse=True)
  return_list= []

  for r in results:
    return_list.append({"intent": classes[r[0]], "probability": str(r[1])})
  return return_list

def getResponse(ints, intents_json):
  tag = ints[0]['intent']
  list_of_intents = intents_json['intents']
  for i in list_of_intents:
    if(i['tag']== tag):
      result = random.choice(i['responses'])
      break
  return result

@functions_framework.http
def chatbot_response(request):
  request_json = request.get_json(silent=True)

  ints = predict_class(request_json['text'], model)
  res = getResponse(ints, intents)
  return  (json.dumps({'response': res}), 200, {'Content-Type': 'application/json'})

# def start_chat():
#   print("Bot: Rhea is here! How can help you?.\n\n")
#   while True:
#     inp = str(input()).lower()
#     if inp.lower()=="end":
#       break
#     if inp.lower()== '' or inp.lower()== '*':
#       print('Please re-phrase your query!')
#       print("-"*50)
#     else:
#       print(f"Bot: {chatbot_response(inp)}"+'\n')
#       print("-"*50)