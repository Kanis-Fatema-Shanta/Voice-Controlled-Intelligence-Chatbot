import tkinter
import cv2
import PIL.Image, PIL.ImageTk
import imageio

def transition():
    '''img1_weight = 0
    reverse = False # this is used to reverse the wieght

    while 1:
        
        # continue to add or decrease weight 
        if reverse:
            img1_weight -= 0.1
        else:
            img1_weight += 0.1 
            
        # if img1_weight goes up then img2_weight goes down accordingly and vice versa.
        img2_weight = 1-img1_weight  
        
        dst = cv2.addWeighted(first_image, img1_weight , second_image, img2_weight , 0)
        
        # we will have a 0.15 transition between frames for a smooth transition
        time.sleep(0.15)    

        cv2.imshow('dst',dst)
        
        # if threshold is reached set reverse to True
        if img1_weight > 1: 
            
           # lets have 1 second wait before reversing
           time.sleep(1)     
           reverse =True
            
        # if  inverse threshold is reached set reverse to False
        elif img1_weight < 0:          
            time.sleep(1)
            reverse =False'''
    pass

 # Create a window
window = tkinter.Tk()
window.title("OpenCV and Tkinter")
  
 # Load an image using OpenCV
cv_img = cv2.cvtColor(cv2.imread("chatbot-image.png"), cv2.COLOR_BGR2RGB)
 
# Get the image dimensions (OpenCV stores image data as NumPy ndarray)
height, width, no_channels = cv_img.shape
 
# Create a canvas that can fit the above image
canvas = tkinter.Canvas(window, width = width, height = height)
canvas.pack()
 
# Use PIL (Pillow) to convert the NumPy ndarray to a PhotoImage
photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(cv_img))
 
# Add a PhotoImage to the Canvas
canvas.create_image(0, 0, image=photo, anchor=tkinter.NW)

gif = imageio.mimread("chatgif.gif")
nums = len(gif)
print("Total {} frames in the gif!".format(nums))

imgs = [cv2.cvtColor(img, cv2.COLOR_RGB2BGR) for img in gif]

btn_blur=tkinter.Button(window, text="Transition", width=50, command=transition)
btn_blur.pack(anchor=tkinter.CENTER, expand=True)
 
 # Run the window loop
window.mainloop()
