import tkinter as tk
from tkinter import Misc
import tkinter.ttk as ttk
from spec_controller import *
from gui import *



class resistain_app:

    #region Application control
    def __init__(self):
        '''
        intit. class for use
        '''
        self.spec = oceanoptic_controller(init_time = 212000,model='HR2000PLUS')
        self.quit = False
        self.dark_wl = None
        self.dark_intens = None
        self.process_display = None

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
            wraplength=250   
            ).place(x = 300, y = 340, width = 180,height = 40)
        
        StandardLabel(
            "Dark_Room_Status",
            root,
            image = TkImage("status_Bad",r"images/Status_Bad.png").image,
                    ).place(x = 150, y = 20)
        

        self.process_display.set("awaiting command")

    #endregion

    #region Spectro usage


    
    def take_dark(self):
        '''
        takes dark sample to normalize against
        '''
        print(" I have taken dark")
        self.process_display.set("taking dark room sample")

        try:
            



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
        


    #endregion


if __name__ == "__main__":
    temp = resistain_app()

    temp.startApp()