import tkinter as tk
from tkinter import filedialog
from tkinter.font import Font

def file_opener(path_label):
   input = filedialog.askopenfile(initialdir="/")
   path_label.configure(text=input.name)

def submit(path,base,observer=None):
   if(not observer==None):
      observer.on_next(path)
      base.destroy()

def browse(source,scheduler):    
   base = tk.Tk()
   base.minsize(280,320)
   base.resizable(0,0)
   base.eval('tk::PlaceWindow . center')
   base.title("TFTP Upload Module")
   helv36 = Font(family="Helvetica",size=20,weight="bold")
   helv36_s = Font(family="Helvetica",size=10,weight="bold")
   helv36_bt = Font(family="Helvetica",size=10,weight="bold")
   heading=tk.Label(text='Upload to server',font=helv36)
   heading.grid(row=0,column=1,pady=10)
   path_label=tk.Label(text='path:',font=helv36_s)
   path_label.grid(row=1,column=1,pady=20)
   broswe_bt = tk.Button(base, text ='Browse',fg='white',bg='orange',font=helv36_bt,width=20, command = lambda:file_opener(path_label))
   broswe_bt.grid(row=2,column=1,padx=125,pady=20)
   submit_bt = tk.Button(base, text ='Upload',fg='white',bg='orange',font=helv36_bt,width=20, command = lambda:submit(path_label.cget('text'),base,source))
   submit_bt.grid(row=3,column=1,padx=125,pady=5)
   base.lift()
   base.mainloop()