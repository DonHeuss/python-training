from tkinter import *

class Application(Frame):
    def __init__(self,master):
        super(Application,self).__init__(master)
        self.grid()
        self.create_widgets()

    def create_widgets(self):
        self.label1 = Label(self,text="Welcome to my window!")
        self.label1.grid(row=0,column=0,sticky=W)
        self.button1 = Button(self, text='Click me!')
        self.button1.grid(row=1, column=0,sticky=W)

root=Tk()
root.title('Test Application window with label')
root.geometry("300x100")        
app=Application(root)
app.mainloop()