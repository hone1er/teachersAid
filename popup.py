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


class LoginFrame(Frame):
    ''' popup that request username and password if there is none available or it is incorrect '''

    def __init__(self):   
        self.master = tk.Tk()
        tk.Label(self.master, 
                text="Short Name").grid(row=0)
        tk.Label(self.master, 
                text="Assign Date").grid(row=1)

        self.e1 = tk.Entry(self.master)
        self.e2 = tk.Entry(self.master)

        self.e1.grid(row=0, column=1)
        self.e2.grid(row=1, column=1)

        tk.Button(self.master, 
                text='Quit', 
                command=self.master.quit).grid(row=3, 
                                            column=0, 
                                            sticky=tk.W, 
                                            pady=4)
        tk.Button(self.master, 
                text='Show', command=self.show_entry_fields).grid(row=3, 
                                                            column=1, 
                                                            sticky=tk.W, 
                                                            pady=4)
        tk.mainloop()

    def show_entry_fields(self):
        print("First Name: %s\nLast Name: %s" % (self.e1.get(), self.e2.get()))
        


if __name__ == "__main__":
    log = LoginFrame()
