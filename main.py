import tkinter as tk
from tkinter import Misc
import tkinter.ttk as ttk
from spec_controller import *
from gui import *



class resistain_app:
    def __init__(self):
        '''
        intit. class for use
        '''
        self.spec = oceanoptic_controller(init_time = 212000,model='HR2000PLUS')
        self.quit = False

    def startApp(self):
        '''
        starts tk application
        '''
        self.root = tk.Tk()
        self.root.title("Resistain App")
        self.root.geometry("400x480")
        self.root.resizable(width=False,height=False)
        self.root.bind("<Escape>", self.endApp)
        self.root.mainloop()


    def endApp(self, event):
        '''
        ends application
        '''

        self.quit = True
        self.root.quit()



if __name__ == "__main__":
    temp = resistain_app()

    temp.startApp()