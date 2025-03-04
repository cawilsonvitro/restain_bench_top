import tkinter as tk
from tkinter import Misc
import tkinter.ttk as ttk
from spec_controller import *
from gui import *
import json
import os
import time 
import numpy as np

class resistain_app:

    #region Application control
    def __init__(self):
        '''
        intit. class for use
        '''
        self.quit = False
        self.process_display = None

        #spectometer
        self.spectrometer = None
        self.integration_time = None
        self.model = None

        #dark sample
        self.dark_wl = None
        self.dark_intens = None

        #light sample
        self.light_wl = None
        self.light_intens = None

        #config storage
        self.config = None
        self.spec_config = None

        #avgs 
        self.light_avg = None
        self.dark_avg = None
        self.boxcar = None

    def startApp(self):
        '''
        starts tk application
        '''
        self.root = tk.Tk()
        self.root.title("Resistain App")
        self.root.geometry("480x400")
        self.root.resizable(width=False,height=False)
        self.root.bind("<Escape>", self.endApp)
        self.process_display = tk.StringVar() 
        self.process_display.set("Booting")
        self.buildGUI(self.root)
        self.root.mainloop()

    def endApp(self, event):
        '''
        ends application
        '''

        self.quit = True
        self.root.quit()
    #endregion

    #region GUI building
    

    def buildGUI(self,root):
        '''
        builds gui for user interaction
        '''
        Button.remove(None)
        StandardInput.remove(None)
        Label.remove(None)
        StandardLabel.remove(None)

        StandardButtons(
            "Dark_Sample",
            root,
            image = TkImage("Dark_Sample", r"images/Dark_Sample.jpg").image,
            command = self.take_dark,
        ).place(x = 30,y = 25)

        StandardButtons(
            "Light_Sample",
            root,
            image = TkImage("Ligh_Sample", r"images/Light_Sample.png").image,
            command = self.take_light,
        ).place(x = 30,y = 85)




        Label(
            "Process_Status", 
            root,
            textvariable = self.process_display,
            anchor=tk.W,           
            height=1,              
            width=30,              
            bd=1,                  
            font=("Arial", 10), 
            cursor="hand2",   
            fg="black",                           
            justify = tk.LEFT,  
            wraplength=100   
            ).place(x = 300, y = 200, width = 180,height = 200)
        
        StandardLabel(
            "Dark_Room_Status",
            root,
            image = TkImage("status_Bad",r"images/Status_Bad.png").image,
                    ).place(x = 150, y = 20)
        

        self.process_display.set("GUI built, initalizing Spectrometer")
        self.load_spec()



    #endregion

    #region spectro init
    def load_spec(self):
        self.process_display.set("loading Config")
        if not os.path.isfile('config.json'): #checking if file exists if not making one
            self.process_display.set("Config not found creating Default Config")
            default_spec = {
                "Spectrometer": {
                "integrationtime": "100000",
                "model": "HR2000PLUS",
                "darkAvgs": "10",
                "lightAvgs": "10",
                "BoxCar": "5"  
                                }
                        }
            with open('config.json','w+') as f:
                json.dump(default_spec, f)#if file not found creates file with default configs
        with open('config.json') as f:
            self.config = json.load(f)
            self.spec_config = self.config["Spectrometer"]
        
        self.process_display.set("Config loaded Initalizing Spectrometer")

        self.model = self.spec_config["model"]
        self.integration_time = int(self.spec_config["integrationtime"])
        self.dark_avg = int(self.spec_config["darkAvgs"])
        self.light_avg = int(self.spec_config["lightAvgs"])
        self.boxcar = int(self.spec_config["BoxCar"])


        try:
            self.spectrometer = oceanoptic_controller(self.integration_time, self.model)
            self.spectrometer.init_spec()
            self.process_display.set("Spectrometer Ready")
        except Exception as e:
            error = "failed: " + str(e)
            self.process_display.set(error)
            



    
    #endregion

    #region Spectro usage



    def take_dark(self):
        '''
        takes dark sample to normalize against
        '''
        self.process_display.set("taking dark room sample")

        try:
            i = 0 

            dark_temp = 0
            self.dark_intens = 0
            while i < self.dark_avg:
                self.spectrometer.get_spectra()
                self.dark_wl = self.spectrometer.wl
                dark_temp = self.spectrometer.intens
                np.add(self.dark_intens,dark_temp)
                i += 1
            
            self.dark_intens_avg = self.dark_intens/self.dark_avg
            self.dark_intens_avg = np.convolve(self.dark_intens_avg, np.ones(self.boxcar), 'valid')/self.boxcar



            StandardLabel(
            "Dark_Room_Status",
            self.root,
            image = TkImage("status_Bad",r"images/Status_Good.png").image,
                    ).place(x = 150, y = 20)
            
            self.process_display.set("dark sample completed")

        except Exception as e:
            
            
            StandardLabel(
            "Dark_Room_Status",
            self.root,
            image = TkImage("status_Bad",r"images/Status_Bad.png").image,
                    ).place(x = 150, y = 20)
            
            self.process_display.set(e)
        
    def take_light(self):
        '''
        takes light sample
        '''

        #if 

        self.process_display.set("taking light sample")
        print("taken light")

    #endregion

    #region Data handling

    

    #endregion

if __name__ == "__main__":
    temp = resistain_app()

    temp.startApp()