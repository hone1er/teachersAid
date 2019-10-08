from Tkinter import *
import Tkinter as tk



class Setup:
    ''' setup for user and web driver '''

    def __init__(self, title, text):
        # Pop up and buttons asking if student is in class, not in class, or attending remotely
        self.popup = tk.Tk()
        self.popup.wm_title(title)
        label = tk.Label(
            self.popup, text=text, font=("Verdana", 10))
        label.pack(side="top", fill="x", pady=10)
        B1 = tk.Button(self.popup, text="Continue", command=self.continued)
        B1.pack()
        self.popup.mainloop()


    def continued(self):
        self.popup.destroy()
        return True
    
class Popup:
    ''' popup for warnings and success messages '''

    def __init__(self, msg):
        self.popup = tk.Tk()
        self.popup.wm_title("Check-in Status")
        label = tk.Label(self.popup, text=msg, font=("Verdana", 10))
        label.pack(side="top", fill="x", pady=10)
        B1 = tk.Button(self.popup, text="Okay", command=self.buttoncmd)
        B1.pack()
        self.popup.mainloop()

    def buttoncmd(self):
        self.popup.destroy()

