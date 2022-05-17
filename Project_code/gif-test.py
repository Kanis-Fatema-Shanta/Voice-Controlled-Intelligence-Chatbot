from tkinter import *
import time
import os
root = Tk()

frames = [PhotoImage(file='chatgif.gif',format = 'gif -index %i' %(i)) for i in range(20)]

def update(ind):
    frame = frames[ind]
    ind += 1
    print(ind)
    if ind>19: #With this condition it will play gif infinitely
        ind = 0
    label.configure(image=frame)
    root.after(100, update, ind)

label = Label(root)
label.pack()
root.after(0, update, 0)
root.mainloop()
