from tinytag import TinyTag
import os
from PIL import Image


def getcover(filename):
    filename1="D:\\music\\"+filename
    detail = TinyTag.get(filename1,image=True)
    print(detail)
    if detail.get_image() != None:
        with open(".\\cover\\"+filename+".PNG","wb") as f:
            f.write(detail.get_image())
            

mulist = os.listdir("D:\\music\\")

for i in mulist:
    getcover(i)
    

