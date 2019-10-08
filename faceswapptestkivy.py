import kivy
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from photos_face_swapping import FaceswappTest as fst
from realtime_face_swapping import VideoFaceswapp as vfs
from kivy.uix.screenmanager import ScreenManager,Screen
from kivy.uix.popup import Popup
from kivy.core.camera import Camera
from kivy.properties import ObjectProperty
from kivy.uix.filechooser import FileChooserIconView
from PIL import Image
import shutil
import time

class FaceswappedVideo(BoxLayout):
    vfswappedImage = None

    def openFsvPp(self):
 
        self.pup = Popup(title="Result",content=self)
        self.pup.open()
        pass
    def closeFsvPp(self):
        self.pup.dismiss()
        pass
    def saveImage(self):
        print("Not Yet Implemented")
        pass

class FaceswappedImage(BoxLayout):
    fswappedImage = None

    def openFsPp(self, img):
        self.fswappedImage = img
        self.ids['swappedImg'].source = self.fswappedImage
        self.ids['swappedImg'].reload()
        
        self.pup = Popup(title="Result",content=self)
        self.pup.open()
        pass
    def closeFsPp(self):
        self.pup.dismiss()
        pass
    def saveImage(self):
        TheFileChooser().openPP("save",self.fswappedImage)
        pass
    pass

class TheFileChooser(BoxLayout):
    label = ObjectProperty(None)
    fciv = ObjectProperty(None)
    cl_fc = ObjectProperty(None)

    def openPP(self,function,img):
        if function == "load":
            self.cl_fc.text = "Open Image"
        elif function == "save":
            self.cl_fc.text = "Save Image"
            self.final_image = img
        self.show = self
        self.popUpFch = Popup(title="File Chooser", content = self.show)
        self.popUpFch.open()
    def closePP(self):
        self.popUpFch.dismiss()


    def select(self, *args):
        try: 
            self.label = args[1][0]
            self.label.text = self.label
            
        except: pass
    def doStuff(self):
        if self.cl_fc.text == "Open Image":
            try: 
                if tL.getImgSelector() == 1:
                    tL.img1_path= self.label
                    tL.updateImage()
                elif tL.getImgSelector() == 2:
                    tL.img2_path= self.label
                    tL.updateImage()
                elif tL.getImgSelector() == 3:
                    vW.img_path = self.label
                    vW.updateImage()
                self.closePP()
            except:
                self.closePP()

        elif self.cl_fc.text == "Save Image":
            try:
                timestr = time.strftime("%Y%m%d_%H%M%S")
                shutil.copy2('swapped.jpg',self.fciv.path + "/IMG_{}.jpg".format(timestr))
                print("Succesfully Saved")
                self.closePP()
            except:
                print("Something went wrong")
                self.closePP()




class PI(GridLayout):
    
    def openFcPopup(self):
        TheFileChooser().openPP("load",None)
   
    def openCamPopup(self):        
        CameraClick().openCamPP()
    

class CameraClick(BoxLayout):

    def openCamPP(self):
        self.show = self
        self.popUpWindow1 =  Popup(title= "Camera", content = self.show)
        self.popUpWindow1.open()
    def closeCamPP(self):
        self.popUpWindow1.dismiss()

    def updateImageCam(self):
        if tL.getImgSelector() == 1:
            tL.img1_path= "IMG1Captured.jpg"
            tL.updateImage()
        elif tL.getImgSelector() == 2:
            tL.img2_path= "IMG2Captured.jpg"
            tL.updateImage()
        elif tL.getImgSelector() == 3:
            vW.img_path= "IMG3Captured.jpg"
            vW.updateImage()
        
        pass
     
    
    def capture(self):
        '''
        Function to capture the image.
        '''
        camera = self.ids['camera']
        if tL.getImgSelector() == 1:
            camera.export_to_png("IMG1Captured.jpg")
        elif tL.getImgSelector() == 2:
            camera.export_to_png("IMG2Captured.jpg")
        elif tL.getImgSelector() == 3:
            camera.export_to_png("IMG3Captured.jpg")
        
        camera.play = False
        camera.stopped = True
        
        
        print("Captured")
    
       
        self.updateImageCam()
        self.closeCamPP()
        
   
        

    
class TestLayout(Screen):
    img1_path = 'bradley_cooper.jpg'
    img2_path = 'jim_carrey.jpg'
    img_selector = None
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        global tL
        tL= self
   
    

    def swapImagesPlace(self):
        temp = self.img1_path
        self.img1_path = self.img2_path
        self.img2_path = temp
        self.ids['img1'].source = self.img1_path
        self.ids['img2'].source = self.img2_path
        self.ids.img1.reload()
        self.ids.img2.reload()
    
    def getImgSelector(self):
        return self.img_selector
    
    def setImgSelector(self,num):
        self.img_selector = num

    def updateImage(self):
        
        if self.img_selector == 1:
            self.ids['img1'].source = self.img1_path
            self.ids.img1.reload()
        elif self.img_selector ==2:
            self.ids['img2'].source = self.img2_path
            self.ids.img2.reload()
        pass

    def btnShowHint(self):
        HintPopup().openPP()

    def btnImg1(self):
        show =  PI()
        self.img_selector = 1
        pupWindow1 = Popup(title= "Image 1", content = show, size_hint=(.75,.25), pos_hint={"x":0.15 , "top":.30})
        pupWindow1.open()
        

    def btnImg2(self):
        show =  PI()
        self.img_selector = 2
        pupWindow2 = Popup(title= "Image 2", content = show, size_hint=(.75,.25), pos_hint={"x":0.15 , "top":.30})
        pupWindow2.open()
        

    def btnFaceswapp(self):
        
        f = fst()
        
        try:
            swappedImg = f.faceswapp(self.img1_path, self.img2_path)
            FaceswappedImage().openFsPp(swappedImg)
        except:
            pass
    
    

class VideoWindow(Screen):
    img_path = 'jim_carrey.jpg'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        global vW
        vW= self

    def updateImage(self):
        self.ids['img_vid'].source = self.img_path
        self.ids.img_vid.reload()

    def btnImg(self): 
        show =  PI()
        tL.setImgSelector(3)
        
        pupWindow3 = Popup(title= "Image", content = show, size_hint=(.75,.25), pos_hint={"x":0.15 , "top":.30})
        pupWindow3.open()
        
    def vidFaceswapp(self):
        vf = vfs()
        
        try:
            swappedTexture = vf.video_faceswapp(self.img_path)
            pass
        except:
            print("Something Went Wrong")
            pass

class HintPopup(BoxLayout):
    def openPP(self):
        self.popup = Popup(title= "Instructions", content = self)
        self.popup.open()
    def closePP(self):
        self.popup.dismiss()
class ScreenManager(ScreenManager):
    pass
    
    
kv = Builder.load_file("faceswapptestkv.kv")    
class FaceswappKivy(App):
    def build(self):
        return kv
        
        
if __name__ == "__main__":
    FaceswappKivy().run()