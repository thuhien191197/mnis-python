
import digitPrediction as DP
import numpy as np
import cv2
from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageDraw
from tkinter import messagebox
import os
import PIL.ImageOps 

import os.path

import pickle
from skimage import io
####################################### BROWSE ###########################################
root = Tk() 
def  browsefunc():
    global filename 
    ftypes = [('Image file', '.jpg'), ('PNG file', '.png'), ('All files', '*')]
        
    filename = filedialog.askopenfilename(filetypes=ftypes, defaultextension='.jpg')    
    global img
    img = cv2.imread(filename,0)
    print("filename:" , filename)
    
     


f = Frame(root, height=200, width=400, background="white") # a frame is created for GUI
f.pack() # pack is used to display on the screen

browsebutton = Button(f, text="Browse", background="white",fg="black", command=browsefunc) 
browsebutton.pack(side=LEFT) #position of the button

label = Label(root)
label.pack()


##################################### Draw the image #######################################
class ImageGenerator:
    def __init__(self,parent,posx,posy,*kwargs):
        self.parent = parent
        self.posx = posx
        self.posy = posy
        self.sizex =200
        self.sizey = 200
        self.b1 = "up"
        self.xold = None
        self.yold = None 
        self.coords= []
        self.drawing_area=Canvas(self.parent,width=self.sizex,height=self.sizey)
        self.drawing_area.place(x=self.posx,y=self.posy)
        self.drawing_area.bind("<Motion>", self.motion)
        self.drawing_area.bind("<ButtonPress-1>", self.b1down)
        self.drawing_area.bind("<ButtonRelease-1>", self.b1up)
        self.button=Button(self.parent,text="Done!",width=10,bg='white',command=self.save)
        self.button.pack(side=LEFT)
        self.button1=Button(self.parent,text="Clear!",width=10,bg='white',command=self.clear)
        self.button1.pack(side=LEFT)      

        self.image=Image.new("RGB",(200,200),(0,0,0))
        # self.image = self.image.resize((28, 28))
        self.draw=ImageDraw.Draw(self.image)
#################################### saving the image ###############################
    def save(self):
        filename2 = filedialog.asksaveasfile()
        self.image.save(filename2)
        ftypes = [('Image file', '.jpg'), ('All files', '*')]
            
        picture = filedialog.askopenfilename(filetypes=ftypes, defaultextension='.jpg')
        col = Image.open(picture)
        col.save("temp.jpg")
        image = Image.open('temp.jpg')
        inverted_image = PIL.ImageOps.invert(image)
        inverted_image.save('result.jpg')

#################################### clear the paintbox ###############################
    def clear(self):
        self.drawing_area.delete("all")
        self.image=Image.new("RGB",(200,200),(0,0,0))
        self.draw=ImageDraw.Draw(self.image)

    def quit(root):
        root.destroy()

    def b1down(self,event):
        self.b1 = "down"

    def b1up(self,event):
        self.b1 = "up"
        self.xold = None
        self.yold = None    

    def motion(self,event):
        if self.b1 == "down":
            if self.xold is not None and self.yold is not None:
                event.widget.create_line(self.xold,self.yold,event.x,event.y,smooth='true',width=5,fill='white')
                self.coords.append((self.xold,self.yold))
                self.draw.line(((self.xold,self.yold),(event.x,event.y)),(255,255,255),width=5)

        self.xold = event.x
        self.yold = event.y

if __name__ == "__main__":
    root.wm_geometry("%dx%d+%d+%d" % (400, 400, 10, 10))
    root.config(bg='white')
    ImageGenerator(root,40,40)

########################################### Dilate ######################################
def dilate():
    global filename
    print("filename_dddd:", filename)
    img = cv2.imread(filename, 0)
    kernel = np.ones((5,5),np.float32)

    # img_erosion = cv2.erode(img, kernel, iterations=1)
    img_dilation = cv2.dilate(img, kernel, iterations=1)
    print('Dilation', img_dilation)
    # cv2.imshow('Input', img)
    # cv2.imshow('Erosion', img_erosion)
    # cv2.imshow('Dilation', img_dilation)
    file = os.path.relpath(filename, "/home/teo/STUDY/digit_prediction/images_test")
    print("filename_ddddkdfjdslfjdl:", filename)
    cv2.imwrite("/home/teo/STUDY/digit_prediction/images_test/"+"dilate_"+ file,img_dilation)
    cv2.waitKey(0)

########################################### Predict Image ######################################
def image_predict_image():
    global img
    img = cv2.resize(img,(28, 28)).astype(np.float32)
    print("img:",img)
    img = np.expand_dims(img, axis=0)
    img = np.expand_dims(img, axis=3)
    logo = img
    if type(img) is str:
        logo = io.imread(img, as_grey=True)

    print("logo:", logo)
    classifier = pickle.load(open("handwrite_model", 'rb'))
    logo_train = (logo).reshape(1, -1)
    print("logo_train:", logo_train)
    total_pixel = 28*28
    logo_train_chia = [[0 for _ in range(total_pixel)]]
    
    for i in range(total_pixel):
        logo_train_chia[0][i] = logo_train[0][i] / 256
    print("logo_train_chia:", logo_train_chia)
    show_image(logo)
    result = classifier.predict(logo_train_chia)
    print("The predicted number is :")
    print(result[0])

    w = Message(root, background="white", text=result[0])
    w.pack(side=BOTTOM)

    m = Message(root, background="white",text="The predicted number is:")
    m.pack(side=BOTTOM)


############################################3 Show image on Console ##############################
def show_image(img):
    logo = img.reshape(28, 28)
    print(logo.shape)
    print(len(logo[0]))
    for i in range(logo.shape[0]):
        for j in range(logo.shape[1]):
            if logo[i][j] > 0.0:
                print("@", end="");
            else:
                print("-", end="");
        print()



training_data, test_data = DP.loadMnistData()
dilateButton = Button(f, text="Dilate", background= "white",fg="red", command=dilate)
dilateButton.pack(side=LEFT)
button=Button(f,text="Prediciton!",width=40,bg='white',command=image_predict_image)
button.pack(side=LEFT)
quitButton = Button(f, text="Quit", background= "white",fg="red", command=f.quit)
quitButton.pack(side=LEFT)

root.geometry("550x550")
root.mainloop()