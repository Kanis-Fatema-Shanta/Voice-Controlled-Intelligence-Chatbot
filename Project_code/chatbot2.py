from tkinter import *
#from PIL import Image
#import tkinter.messagebox
import time
import datetime
import pyttsx3
from win32com.client import Dispatch
#import win32com.client as wincl
#from pygame import mixer
import speech_recognition as sr
from threading import Thread
import requests
from bs4 import BeautifulSoup
from gtts import gTTS
import os
import random
from playsound import playsound


def shut_down():
    p1=Thread(target=speak,args=("Shutting down. Thankyou For Using Our Sevice. Take Care, Good Bye.",))
    p1.start()
    p2 = Thread(target=transition2)
    p2.start()
    time.sleep(7)
    root.destroy()

def transition2():
    global img1
    global flag
    global flag2
    global frames
    global canvas
    local_flag = False
    for k in range(0,5000):
        for frame in frames:
            if flag == False:
                canvas.create_image(0, 0, image=img1, anchor=NW)
                canvas.update()
                flag = True
                return
            else:
                canvas.create_image(0, 0, image=frame, anchor=NW)
                canvas.update()
                time.sleep(0.1)
        


def web_scraping(qs):
    global flag2

    URL = 'https://www.google.com/search?q=' + qs
    page = requests.get(URL)

    soup = BeautifulSoup(page.content, 'html.parser')
    print(soup)
    
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

    div0 = soup.find_all('div',class_="kvKEAb")
    div1 = soup.find_all("div", class_="Ap5OSd")
    div2 = soup.find_all("div", class_="nGphre")
    div3  = soup.find_all("div", class_="BNeawe iBp4i AP7Wnd")

    if len(div0)!=0:
        answer = div0[0].text
    elif len(div1) != 0:
       answer = div1[0].text+"\n"+div1[0].find_next_sibling("div").text
       #print(answer)
       #speak(answer)
       # print(div1[0].find_next_sibling("div").text)
    elif len(div2) != 0:
       answer = div2[0].find_next("span").text+"\n"+div2[0].find_next("div",class_="kCrYT").text
       #print(answer)
       #speak(answer)
       # print(div2[0].find_next("div",class_="kCrYT").text)
    elif len(div3)!=0:
        answer = div3[1].text
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
    canvas2.create_text(10, 225, anchor=NW, text=answer, font=('Candara Light', -25,'bold italic'),
                        fill="white", width=350)
    flag2 = False
    global loading
    loading.destroy()
    p1=Thread(target=speak,args=(answer,))
    p1.start()
    p2 = Thread(target=transition2)
    p2.start()


def speak(text):
    global flag
    engine.say(text)
    engine.runAndWait()
    flag=False

'''def speak(textToSpeak):
    try:
        r2 = random.randint(1, 10000000)
        myobj = gTTS(text=textToSpeak, lang='en')
        path = str("voices\conVoice" + str(r2) + ".mp3")
        myobj.save(path)
        playsound(path)
        os.remove(path)
    except:
        raise InterruptedError'''

def wishme():
    hour = datetime.datetime.now().hour

    if 0 <= hour < 12:
        text = "Good Morning sir. I am Jarvis. How can I Serve you?"
    elif 12 <= hour < 18:
        text = "Good Afternoon sir. I am Jarvis. How can I Serve you?"
    else:
        text = "Good Evening sir. I am Jarvis. How can I Serve you?"

    canvas2.create_text(10,10,anchor =NW , text=text,font=('Candara Light', -25,'bold italic'), fill="white",width=350)
    p1=Thread(target=speak,args=(text,))
    p1.start()
    p2 = Thread(target=transition2)
    p2.start()


def takecommand():
    global loading
    global flag
    global flag2
    global canvas2
    global query
    global img4
    if flag2 == False:
        canvas2.delete("all")
        canvas2.create_image(0,0, image=img4, anchor="nw")

    # it takes mic input from the user and return string output
    speak("I am listening.")
    flag= True
    r = sr.Recognizer()
    r.dynamic_energy_threshold = False
    r.energy_threshold = 4000
    with sr.Microphone() as source:
        print("Listening...")
        #r.pause_threshold = 3
        audio = r.listen(source,timeout=4,phrase_time_limit=4)

    try:
        print("Recognizing..")
        query = r.recognize_google(audio, language='en-in')
        print(f"user Said :{query}\n")
        query = query.lower()
        canvas2.create_text(490, 120, anchor=NE, justify = RIGHT ,text=query, font=('fixedsys', -30),
                            fill="white", width=350)
        #display_canvas2(query)
        global img3
        loading = Label(root, image=img3, bd=0)
        loading.place(x=900, y=622)
        #time.sleep(1)
        #web_scraping(query)


    except Exception as e:
        print(e)

        speak("Say that again please")
        return "None"




def main_window():
    global query
    wishme()
    while True:
        if query != None:
            if 'shutdown' in query or 'quit' in query or 'stop' in query or 'goodbye' in query:
                shut_down()
                break
            else:
                web_scraping(query)
                query = None
    


    #query = takecommand().lower()

    #web_scraping(query)

    


if __name__ == "__main__":
    loading = None
    query = None
    flag = True
    flag2 = True
    engine = pyttsx3.init('sapi5') # Windows
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)
    rate = engine.getProperty('rate')
    engine.setProperty('rate', rate-10)
    root=Tk()
    root.title("Intelligent Chatbot")
    pad=3
    root.geometry('1360x690+-5+0')
    root.configure(background='white')
    #root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth()-pad, root.winfo_screenheight()-pad))
    img1= PhotoImage(file='chatbot-image.png')
    img2= PhotoImage(file='button-green.png')
    img3= PhotoImage(file='icon.png')
    img4= PhotoImage(file='terminal.png')
    #bg = Image.open("terminal-bg.png")
    #bg = bg.resize((1360, 620), Image.ANTIALIAS)    #im = ImageTk.PhotoImage(Image.open("terminal-bg.png").resize((500,900)))
    f = Frame(root,width = 1360, height = 690)
    f.place(x=0,y=0)
    f.tkraise()
    front_image = PhotoImage(file="front2.png")
    #front_label = Label(f,image = front_image)
    #front_label.pack()
    #front_label.pack_forget()
    #f.after(4000, f.destroy)
    okVar = IntVar()
    btnOK = Button(f, image=front_image,command=lambda: okVar.set(1))
    btnOK.place(x=0,y=0)
    f.wait_variable(okVar)
    f.destroy()    

    background_image=PhotoImage(file="last.png")
    background_label = Label(root, image=background_image)
    background_label.place(x=0, y=0)


    frames = [PhotoImage(file='chatgif.gif',format = 'gif -index %i' %(i)) for i in range(20)]
    canvas = Canvas(root, width = 800, height = 596)
    canvas.place(x=10,y=10)
    canvas.create_image(0, 0, image=img1, anchor=NW)
    question_button = Button(root,image=img2, bd=0, command=takecommand)
    question_button.place(x=200,y=625)

    
    frame=Frame(root,width=500,height=596)
    frame.place(x=825,y=10) #.grid(row=0,column=0)
    canvas2=Canvas(frame,bg='#FFFFFF',width=500,height=596,scrollregion=(0,0,500,900))
    #hbar=Scrollbar(frame,orient=HORIZONTAL)
    #hbar.pack(side=BOTTOM,fill=X)
    #hbar.config(command=canvas.xview)
    vbar=Scrollbar(frame,orient=VERTICAL)
    vbar.pack(side=RIGHT,fill=Y)
    vbar.config(command=canvas2.yview)
    canvas2.config(width=500,height=596, background="black")
    canvas2.config(yscrollcommand=vbar.set)
    canvas2.pack(side=LEFT,expand=True,fill=BOTH)
    canvas2.create_image(0,0, image=img4, anchor="nw")
    #canvas2.create_text(10,10,anchor =NW , text="I am Jarvis. How can I Serve you?",font=('Impact', -30), fill="white",width=350)
    #T = Text(canvas2, height=4, width=10, background="yellow")
    #T.place(x=100,y=10)

    
    task = Thread(target=main_window) # it has to be `,` in `(queue,)` to create tuple with one value
    task.start() # start thread
    root.mainloop()
