from tkinter import *
import time
from multiprocessing import Process
from threading import Thread
import sys
import pyttsx3

flag = True

def speak(text):
    global flag
    engine.say(text)
    engine.runAndWait()
    flag =False
    

def transition2():
    global img1
    global flag
    global frames
    global canvas
    for k in range(0,1000):
        for frame in frames:
            #canvas.delete(ALL)
            canvas.create_image(0, 0, image=frame, anchor=NW)
            canvas.update()
            time.sleep(0.3)
        if flag == False:
            canvas.create_image(0, 0, image=img1, anchor=NW)
            canvas.update()
            break
def main():
    speak("Hello everyone! How Are you, I am fine Thankyou. Take Care")
    transition2()
    
engine = pyttsx3.init('sapi5') # Windows
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
root = Tk()
root.title("Transition")
frames = [PhotoImage(file='chatgif.gif',format = 'gif -index %i' %(i)) for i in range(20)]
canvas = Canvas(root, width = 803, height = 596)
canvas.pack()
img1= PhotoImage(file='chatbot-image.png')
canvas.create_image(0, 0, image=img1, anchor=NW)

#btn=Button(root, text="Transition", width=50, command=transition2)
#btn.pack(anchor=CENTER, expand=True)
#task = Thread(target=main)
#task.start()
p1=Thread(target=speak,args=("Hello everyone! How Are you, I am fine Thankyou. Take Care",))
p1.start()
p2 = Thread(target=transition2)
p2.start()
#p1.join()
#p2.join()

root.mainloop()
#task.join()
