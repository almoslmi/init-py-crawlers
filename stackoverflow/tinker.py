from Tkinter import *
from tkFileDialog import askopenfilename
from tkMessageBox import showwarning, showinfo
from  matplotlib import  pyplot as pl
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg
from matplotlib.figure import Figure

class App(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.filename = None
        button1 = Button(self, text="Browse for a file", command=self.askfilename)
        button2 = Button(self, text ="plot the data", command=self.plot)
        button3 = Button(self, text="Exit", command=master.destroy)
        button1.grid()
        button2.grid()
        button3.grid()
        self.grid()
    def askfilename(self):
        filename = askopenfilename()

        self.filename = filename

    def plot(self):
        global pl
        if self.filename:
            with open(self.filename) as fp:
                pl.plot(fp)
        else:
            showwarning('No file selected', 'Select a file first')


root = Tk()
root.title("graph plotter")
root.geometry("150x150")
app = App(root)
root.mainloop()