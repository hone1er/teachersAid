from tkinter import *
import tkinter as tk
import tkinter.messagebox as tm


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
    
        




class LoginFrame(Frame):
    ''' popup that request username and password if there is none available or it is incorrect '''

    def __init__(self, master, setup):
        super().__init__(master)
        self.master = master
        self.setup = setup
        self.label_username = Label(self, text="Username")
        self.label_password = Label(self, text="Password")

        self.entry_username = Entry(self)
        self.entry_password = Entry(self, show="*")

        self.label_username.grid(row=0, sticky=E)
        self.label_password.grid(row=1, sticky=E)
        self.entry_username.grid(row=0, column=1)
        self.entry_password.grid(row=1, column=1)

        self.logbtn = Button(self, text="Login",
                             command=self._login_btn_clicked)
        self.logbtn.grid(columnspan=2)

        self.pack()

    def _login_btn_clicked(self):
        self.setup.username = self.entry_username.get()
        self.setup.pw = self.setup.driver_suite.encrypt(
            bytes(self.entry_password.get().encode('utf-8')))
        with open('user.py', 'w') as file:
            file.write(f'username = "{self.setup.username}"\n')
            file.write(f'pw = {self.setup.pw}\n')
        self.master.destroy()


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

