#STEVE BUSCEMI FACE ENHANCER

#IMPORTING MODULES
from PIL import Image as ImagePIL
from PIL import ImageDraw
import numpy as np
import ImageTk
from Tkinter import *
import cv2



#DEFINING FUNCTIONS

#defining the findEyes function for finding eyes
def findEyes(filename):
    #Loading  the image
    img = cv2.imread(filename)
    #Turning it gray for eye detection to work
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    #Finding the face area in order to avoid confusion
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    for (x,y,w,h) in faces:
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = img[y:y+h, x:x+w]
        eyes = eye_cascade.detectMultiScale(roi_gray)
        for (ex,ey,ew,eh) in eyes: #working with the eyes in the face
            EyeCoordinates.append((ex+x,ey+y,ew,eh))
            cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)
    return img

#Selecting the biggest eye area
def biggestEye(eyeList):
    biggestWidth = 0 #using the width as a marker for the biggest eye area
    biggestWidthIndex = 0
    for i in range(len(eyeList)):
        (x,y,w,h) = eyeList[i]
        if w > biggestWidth:
            biggestWidth = w
            biggestWidthIndex = i
    biggestEye = eyeList[biggestWidthIndex]
    eyeList.remove(biggestEye)
    return biggestEye

#Figuring out wich eye is the left one and which is the right one
def orderEyesLeftRight(tuple1,tuple2):
    if tuple1[0] > tuple2[0]:
        return (tuple1,tuple2)
    else:
        return (tuple2,tuple1)

#INITIALIZING VARIABLES

#Initializing the detection cascades
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')
EyeCoordinates =[]

#Loading Steve Buscemi's eyes
gloriousLeftEye = ImagePIL.open('left.png')
gloriousRightEye = ImagePIL.open('right.png')


def main():
    filename = getfilename()
    
    img = findEyes(filename)    

    #Finding the two biggest eye areas and figuring out which one is left and which one is right
    eye1 = biggestEye(EyeCoordinates)
    eye2 = biggestEye(EyeCoordinates)
    (LeftEyeData,RightEyeData) = orderEyesLeftRight(eye1,eye2)

    #Finding the width and height of both eyes
    widthL = LeftEyeData[2] 
    widthR = RightEyeData[2]
    heightL = LeftEyeData[3]
    heightR = RightEyeData[3]

    #Scaling the eyes
    scaledLeftEye = gloriousLeftEye.resize((widthL+1,heightL+1))
    scaledRightEye = gloriousRightEye.resize((widthR+1,heightR+1))
    im = ImagePIL.open(filename)

    #drawing a new RGBA canvas based on the picture we opened
    canvas = ImagePIL.new('RGBA',(im.size[0],im.size[1]),color = 'black')
    for x in range(im.size[0]):
        for y in range(im.size[1]):
            (R,G,B) = im.getpixel((x,y))
            canvas.putpixel((x,y),(R,G,B))

    #getting coordinates
    (x1,y1,w1,h1) = LeftEyeData
    (x2,y2,w2,h2) = RightEyeData

    #pasting eyes
    canvas.paste(scaledLeftEye,(x1,y1),scaledLeftEye)
    canvas.paste(scaledRightEye,(x2,y2),scaledRightEye)

    canvas.save('A1A1A1A1.png')
               
    cv2.imshow('img',img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def getfilename():
   return str((e1.get()))


#Creating the GUI window
master = Tk()
master.geometry('1000x400')
Label(master, text="File Name  ")#.grid(row=0)
e1 = Entry(master)
#e1.grid(row=0, column=1)
e1.pack()
B = Button(master, text ='GIVE ME BEAUTIFUL EYES', command = main)#.grid(row=4, column=1, sticky=W,pady=4)
B.pack()

canvas = Canvas(master,width=1000,height=500)
canvas.pack()
PILImage = ImagePIL.open("him.jpg")
image = ImageTk.PhotoImage(PILImage)
imagesprite = canvas.create_image(500,200,image=image)




master.mainloop()




    
    
    
                
