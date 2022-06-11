import nltk
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()
import pickle
import numpy as np

from keras.models import load_model
model = load_model('chatbot_model.h5')
import json
import random
intents = json.loads(open('intentsREV.json').read())
words = pickle.load(open('words.pkl','rb'))
classes = pickle.load(open('classes.pkl','rb'))


def clean_up_sentence(sentence):
    # tokenize the pattern - split words into array
    sentence_words = nltk.word_tokenize(sentence)
    # stem each word - create short form for word
    sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
    return sentence_words

# return bag of words array: 0 or 1 for each word in the bag that exists in the sentence

def bow(sentence, words, show_details=True):
    # tokenize the pattern
    sentence_words = clean_up_sentence(sentence)
    # bag of words - matrix of N words, vocabulary matrix
    bag = [0]*len(words)  
    for s in sentence_words:
        for i,w in enumerate(words):
            if w == s: 
                # assign 1 if current word is in the vocabulary position
                bag[i] = 1
                if show_details:
                    print ("found in bag: %s" % w)
    return(np.array(bag))

def predict_class(sentence, model):
    # filter out predictions below a threshold
    p = bow(sentence, words,show_details=False)
    res = model.predict(np.array([p]))[0]
    ERROR_THRESHOLD = 0.25
    results = [[i,r] for i,r in enumerate(res) if r>ERROR_THRESHOLD]
    # sort by strength of probability
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({"intent": classes[r[0]], "probability": str(r[1])})
    return return_list



def getResponse(ints, intentsREV_json):
    tag = ints[0]['intent']
    list_of_intents = intentsREV_json['intents']
    for i in list_of_intents:
        if(i['tag']== tag):
            result = random.choice(i['responses'])
            break
    return result

def chatbot_response(msg):
    ints = predict_class(msg, model)
    res = getResponse(ints, intents)
    return res


#Creating GUI with tkinter
import tkinter
import PIL
from tkinter import *
import webbrowser
from tkHyperlinkManager import HyperlinkManager
from functools import partial
from PIL import  Image, ImageTk

#-----------------------------

def callback(url):
   webbrowser.open_new_tab(url)


#--------------------------

def send():
    msg = EntryBox.get("1.0",'end-1c').strip()
    EntryBox.delete("0.0",END)
    
    ChatLog.config(state=NORMAL)
    ChatLog.insert(END, ' \n')

    if msg != '':
        ChatLog.config(state=NORMAL)
        ChatLog.insert(END, 'You: ' + msg + '  \n\n', 'userText')
        ChatLog.config(foreground="#442265", font=("Verdana", 12 ))
        
    
        res = chatbot_response(msg)
        #--------------------

        resSt = str(res)
        if(resSt.startswith('https:')):
            ChatLog.insert(END, "Bot: You should check ")
            hyperlink = HyperlinkManager(ChatLog)
            ChatLog.insert(END, "this link \n\n", hyperlink.add(partial(webbrowser.open, resSt)))

        elif(resSt.startswith('Academic Calender:')):
            wordList = resSt.split();
            resSt = wordList[-1];
            ChatLog.insert(END, "Bot: The academic calendar of Uskudar University can be found at ")
            hyperlink = HyperlinkManager(ChatLog)
            ChatLog.insert(END, "this link \n\n", hyperlink.add(partial(webbrowser.open, resSt)))
        elif(resSt.startswith('Timetable:')):
            wordList = resSt.split();
            resSt = wordList[-1];
            ChatLog.insert(END, "Bot: You can check all department's lecture schedule ")
            hyperlink = HyperlinkManager(ChatLog)
            ChatLog.insert(END, "in here :) \n\n", hyperlink.add(partial(webbrowser.open, resSt)))
        elif(resSt.startswith('Payment:')):
            wordList = resSt.split();
            resSt = wordList[-1];
            ChatLog.insert(END, "Bot: You can call the default university number (+90 216 400 2222) and ask of accounting department or ")
            hyperlink = HyperlinkManager(ChatLog)
            ChatLog.insert(END, "check the website. \n\n", hyperlink.add(partial(webbrowser.open, resSt)))
        elif(resSt.startswith('Price:')):
            wordList = resSt.split();
            resSt = wordList[-1];
            ChatLog.insert(END, "Bot: You can see all department's price policy at this ")
            hyperlink = HyperlinkManager(ChatLog)
            ChatLog.insert(END, "table. \n\n", hyperlink.add(partial(webbrowser.open, resSt)))
        elif(resSt.startswith('Menu:')):
            wordList = resSt.split();
            resSt = wordList[-1];
            ChatLog.insert(END, "Bot: We have delicious meal on menu today! Don't be late and check the ")
            hyperlink = HyperlinkManager(ChatLog)
            ChatLog.insert(END, "list! \n\n", hyperlink.add(partial(webbrowser.open, resSt)))
        else:
            ChatLog.insert(END, "Bot: " + res + '\n\n')    
        
            

        #-----------------------
 
        ChatLog.config(state=DISABLED)
        ChatLog.yview(END)
 

base = Tk()
base.title("Uskudar University ChatBot")
base.geometry("500x600")
base.resizable(width=FALSE, height=FALSE)

#Create Chat window
ChatLog = Text(base, bd=0, bg="white", height="8", width="50", font="Arial", wrap=WORD)

ChatLog.config(state=DISABLED)
ChatLog.tag_config('userText', foreground="green", justify=RIGHT)

#logo
image = ImageTk.PhotoImage(Image.open('C:\\Users\\Mert\\Desktop\\ChatBot\\images\\UUlogo.png'))
label1 = tkinter.Label(base, image=image)
label2 = tkinter.Label(base, text="Uskudar University ChatBot")
label1.pack()
label2.pack()

#Bind scrollbar to Chat window
scrollbar = Scrollbar(base, command=ChatLog.yview, cursor="heart")
ChatLog['yscrollcommand'] = scrollbar.set

#Create Button to send message
SendButton = Button(base, font=("Verdana",12,'bold'), text="Send", width="12", height=5,
                    bd=0, bg="#32de97", activebackground="#3c9d9b",fg='#ffffff',
                    command= send )

#Create the box to enter message
EntryBox = Text(base, bd=0, bg="white",width="29", height="5", font="Arial", wrap=WORD)
#EntryBox.bind("<Return>", send)


#Place all components on the screen
scrollbar.place(x=476,y=6, height=386)
ChatLog.place(x=0,y=115, height=380, width=470)
EntryBox.place(x=128, y=501, height=90, width=342)
SendButton.place(x=6, y=501, height=90)


base.mainloop()
