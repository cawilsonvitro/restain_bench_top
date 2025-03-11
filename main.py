#region Imports
import tkinter as tk
from tkinter import Misc
import tkinter.ttk as ttk
from spec_controller import *
from gui import *
import json
import os
import time 
import numpy as np
import csv
from datetime import datetime as dt
import matplotlib.pyplot as plt
#endregion 

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
        self.dark_intens = None
        self.dark = False

        #light sample
        self.light_intens = None

        #config storage
        self.config = None
        self.spec_config = None

        #avgs 
        self.light_avg = None
        self.dark_avg = None
        self.dark_intens_avg = None
        self.light_intens = None
        self.boxcar = None
        self.adjust = None

        #data management
        self.startPt = None
        self.stopPt = None
        self.dataPath = r"data/"

    def startApp(self):
        '''
        starts tk application
        '''
        self.root = tk.Tk()
        self.root.title("Resistain App")
        self.root.geometry("480x400")
        self.root.resizable(width=False,height=False)
        self.root.bind("<Escape>", self.endApp)
        self.root.protocol("WM_DELETE_WINDOW",self.endProto)
        self.process_display = tk.StringVar() 
        self.process_display.set("Booting")
        self.buildGUI(self.root)
        self.root.mainloop()
    
    def endProto(self):
        '''
        wrapper to endApp
        '''
        self.endApp(None)
    
    def endApp(self, event):
        '''
        ends application
        '''
        self.quit = True
        self.root.quit()
        self.spectrometer.quit()
        
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
            command = self.take_dark
        ).place(x = 30,y = 25)

        StandardButtons(
            "Light_Sample",
            root,
            image = TkImage("Light_Sample", r"images/Light_Sample.png").image,
            command = self.take_light
        ).place(x = 30,y = 85)
        
        StandardButtons(
            "Save",
            root,
            image = TkImage("Save", r"images/Save.png").image,
            command = self.save
        ).place(x = 30, y = 145)




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
                "BoxCar": "5",
                "startPt":"300",
                "stopPt":"1550"
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
        self.adjust = int(self.boxcar/2)
        self.startPt = int(self.spec_config["startPt"])
        self.stopPt = int(self.spec_config["stopPt"])
        


        try:
            self.spectrometer = oceanoptic_controller(self.integration_time, self.model)
            self.spectrometer.init_spec()
            self.spectrometer.get_spectra()
            self.process_display.set("Spectrometer Ready")
            self.wl = self.spectrometer.wl
            self.wl_adj = self.wl[self.adjust:-self.adjust]
            print(self.wl_adj)
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
        self.root.update_idletasks()
        self.dark = False
        try:
            i = 0 
            dark_temp = 0
            self.dark_intens = 0
            while i < self.dark_avg:
                self.spectrometer.get_spectra()
                dark_temp = self.spectrometer.intens
                self.dark_intens = np.add(self.dark_intens, dark_temp)
                # if i == 0:
                #     self.dark_intens = dark_temp
                # else:
                #     self.dark_intens= np.add(self.dark_intens, dark_temp)
                print(i)
                i += 1
            
            self.dark_intens_avg = self.dark_intens/self.dark_avg
            self.dark_intens_avg = np.convolve(self.dark_intens_avg, np.ones(self.boxcar), 'valid')/self.boxcar

            StandardLabel(
            "Dark_Room_Status",
            self.root,
            image = TkImage("status_Bad",r"images/Status_Good.png").image,
                    ).place(x = 150, y = 20)
            
            self.process_display.set("dark sample completed")
            self.dark = True

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

        if not self.dark:
            self.process_display.set(" Please take dark sample first")
        else:
            self.process_display.set("taking light sample")
            self.root.update_idletasks()
            
            try:
                i = 0
                light_temp = 0
                self.light_intens = 0
                while i < self.light_avg:
                    self.spectrometer.get_spectra()
                    light_temp = self.spectrometer.intens
                    self.light_intens = np.add(self.light_intens, light_temp)
                    # if i == 0:
                    #     self.light_intens = self.spectrometer.intens
                    # else:
                    #    self.light_intens = np.add(self.light_intens, light_temp)
                    print(self.light_intens[1],light_temp[1])
                    i += 1
                
                self.light_intens_avg = self.light_intens/self.light_avg
                print(self.light_intens_avg[1])
                self.light_intens_avg = np.convolve(self.light_intens_avg, np.ones(self.boxcar), 'valid')/self.boxcar
                print(self.light_intens_avg[1])
                self.process_display.set("Light Sample taken")
                self.graph()

            except Exception as e:
                self.process_display.set(e)
                print(e)
            

    #endregion

    #region Data handling

    def graph(self):
        print(self.light_intens_avg[self.startPt],self.dark_intens_avg[self.startPt])
        self.sp = np.subtract(self.light_intens_avg, self.dark_intens_avg)
        print(self.sp[self.startPt])

       # out_data = np.stack((self.wl_adj, self.dark_intens_avg, self.light_intens_avg, self.sp), axis = 0)
        #out_data = out_data.T
        
        #getting date and time
        
        self.dt = dt.now().strftime("%m/%d/%Y, %H:%M:%S")
        plt.plot(self.wl_adj[self.startPt:self.stopPt],self.sp[self.startPt:self.stopPt])
        plt.ylabel("Intensity")
        plt.xlabel("Wavelength")
        
        plt.title(self.dt)
        plt.show()
    
    def save(self):
        try:
            self.dt = dt.now().strftime("%m-%d-%Y, Hour %H Min %M Sec %S")
            file = self.dataPath + self.dt + r".csv"
            header = ["Wavelength", "Light", "Dark", "Intensity"]
            with open(file, "w+", newline = "\n") as f:
                writer = csv.writer(f)
                writer.writerow(header)
                i = 0
                
                for wl in self.wl_adj:
                    row = [wl, 
                            self.light_intens_avg[i],
                            self.dark_intens_avg[i],  
                            self.sp[i]]
                    writer.writerow(row)
                    i += 1
        except AttributeError:
            self.process_display.set("Please take samples first")
            self.root.update_idletasks()
        except Exception as e:
            self.process_display.set(e)

    #endregion

if __name__ == "__main__":
    temp = resistain_app()

    temp.startApp()