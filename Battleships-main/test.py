import tkinter as tk
from random import choice

def getRandomColor():
    return choice(['red','blue','green','yellow','white','goldenrod'])

def click(event):
    print(vars(event))
    item = event.widget.find_withtag('current')
    event.widget.itemconfig(item,fill=getRandomColor())

root = tk.Tk()
root.grid()

c = tk.Canvas(root,width=300,height=300,bg='black')
c.grid()
c.create_polygon(0,0,100,0,50,100,fill='blue',tag='tri_1')
c.create_polygon(100,0,50,100,150,100,fill='yellow',tag='tri_2')
c.bind('<Button-1>',click)

root.mainloop()