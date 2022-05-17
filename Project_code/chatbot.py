from tkinter import *
import tkinter.messagebox
import time
import datetime
import pyttsx3
import win32com.client as wincl
from pygame import mixer
import speech_recognition as sr
from threading import Thread
import requests
from bs4 import BeautifulSoup


def transition2():
    global img1
    global flag
    global frames
    global canvas
    for k in range(0,5000):
        for frame in frames:
            #canvas.delete(ALL)
            canvas.create_image(0, 0, image=frame, anchor=NW)
            canvas.update()
            time.sleep(0.1)
        if flag == False:
            canvas.create_image(0, 0, image=img1, anchor=NW)
            canvas.update()
            flag = True
            break


def web_scraping(qs):
    URL = 'https://www.google.com/search?q=' + qs
    page = requests.get(URL)

    soup = BeautifulSoup(page.content, 'html.parser')

    links = soup.findAll("a")
    all_links = []
    for link in links:
       link_href = link.get('href')
       if "url?q=" in link_href and not "webcache" in link_href:
           all_links.append((link.get('href').split("?q=")[1].split("&sa=U")[0]))
           

    flag= False
    for link in all_links:
       if 'https://en.wikipedia.org/wiki/' in link:
           wiki = link
           flag = True
           break


    div1 = soup.find_all("div", class_="Ap5OSd")
    div2 = soup.find_all("div", class_="nGphre")

    if len(div1) != 0:
       answer = div1[0].text+"\n"+div1[0].find_next_sibling("div").text
       #print(answer)
       #speak(answer)
       # print(div1[0].find_next_sibling("div").text)
    elif len(div2) != 0:
       answer = div2[0].find_next("span").text+"\n"+div2[0].find_next("div",class_="kCrYT").text
       #print(answer)
       #speak(answer)
       # print(div2[0].find_next("div",class_="kCrYT").text)
    elif flag==True:
       page2 = requests.get(wiki)
       soup = BeautifulSoup(page2.text, 'html.parser')

       title = soup.select("#firstHeading")[0].text
       # print(title)
       paragraphs = soup.select("p")
       for para in paragraphs:
           if bool(para.text.strip()):
               answer = title + "\n" + para.text
               #print(answer)
               #speak(answer)
               break
       # print(paragraphs)
       # just grab the text up to contents as stated in question
       # intro = '\n'.join([ para.text for para in paragraphs[0:2]])
       # print(intro)
    else:
       #print("Not Found")
       #engine.say("Not Found")
       #engine.runAndWait()
        answer = "Sorry. I could not find the desired results"
    p1=Thread(target=speak,args=(answer,))
    p1.start()
    p2 = Thread(target=transition2)
    p2.start()


def speak(text):
    global flag
    engine.say(text)
    engine.runAndWait()
    flag=False

def wishme():
    hour = datetime.datetime.now().hour

    if 0 <= hour < 12:
        text = "Good Morning sir"
    elif 12 <= hour < 18:
        text = "Good Afternoon sir"
    else:
        text = "Good Evening sir"

    p1=Thread(target=speak,args=("I am Genos. How can I Serve you?",))
    p1.start()
    p2 = Thread(target=transition2)
    p2.start()



def takecommand():
    global flag
    # it takes mic input from the user and return string output
    speak("I am listening.")
    flag= True
    r = sr.Recognizer()
    r.dynamic_energy_threshold = False
    r.energy_threshold = 400
    with sr.Microphone() as source:
        print("Listening...")
        #r.pause_threshold = 3
        audio = r.listen(source,timeout=4,phrase_time_limit=4)

    try:
        print("Recognizing..")
        query = r.recognize_google(audio, language='en-in')
        print(f"user Said :{query}\n")

    except Exception as e:
        print(e)

        speak("Say that again please")
        return "None"

    query=query.lower()
    web_scraping(query)



def main_window():
    wishme()
    


    #query = takecommand().lower()

    #web_scraping(query)

    


if __name__ == "__main__":
    
    flag = True
    engine = pyttsx3.init('sapi5') # Windows
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)
    root=Tk()
    root.title("Intelligent Chatbot")
    pad=3
    root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth()-pad, root.winfo_screenheight()-pad))
    img1= PhotoImage(file='chatgif5.gif')
    img2= PhotoImage(file='button.png')

    frames=[]
    for i in range(15):
        filename = "{}.gif".format(i)
        frames.append(PhotoImage(file=filename))
    canvas = Canvas(root, width = 1067, height = 600)
    canvas.pack()
    canvas.create_image(0, 0, image=img1, anchor=NW)
    question_button = Button(root,image=img2, bd=0, command=takecommand)
    question_button.pack(anchor=CENTER)
    
    task = Thread(target=main_window) # it has to be `,` in `(queue,)` to create tuple with one value
    task.start() # start thread
    root.mainloop()
    task.join()
