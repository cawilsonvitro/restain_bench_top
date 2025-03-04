# import tkinter as tk

# # Create the main window
# root = tk.Tk()
# root.geometry("400x250")  # Set window size
# root.title("Welcome to My App")  # Set window title

# # Create a StringVar to associate with the label
# text_var = tk.StringVar()
# text_var.set("Hello, World!")

# # Create the label widget with all options
# label = tk.Label(root, 
#                  textvariable=text_var, 
#                  anchor=tk.CENTER,       
#                  bg="lightblue",      
#                  height=3,              
#                  width=30,              
#                  bd=3,                  
#                  font=("Arial", 16, "bold"), 
#                  cursor="hand2",   
#                  fg="red",             
#                  padx=15,               
#                  pady=15,                
#                  justify=tk.CENTER,    
#                  relief=tk.RAISED,     
#                  underline=0,           
#                  wraplength=250         
#                 )

# # Pack the label into the window
# label.pack(pady=20)  # Add some padding to the top


# # Run the main event loop
# root.mainloop()

#takes ten samples in dark then avgs it out

#for thing in # of iterations currently 10
# np.add 
#boxcar = 5 some odd number 

#np.convolve(overall avg, np.ones(boxcar), valid)/boxcar


#for normal measurement avg for same amount 
#np.convolve(overall avg, np.ones(boxcar), valid)/boxcar
#use of dark is np.substract( lgt avg,ark avg)



# import json

# with open("config.json") as f:
#     data = json.load(f)
#     specvar = data['Spectrometer']
#     print(specvar["model"])
#     x = 1



# test = None

# if not test:
#     print('daghsa')

import numpy as np

a = [1,1,1,1,1]
b = [1,1,1,1,1]

c = np.add(a,b)

print(c)
