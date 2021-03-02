# Author JANITHA SANDARUWAN
from tkinter import *
from tkinter import font
import pyscreenshot as ImageGrab
import uuid
import base64
import os

class main:
    def __init__(self, master):
        self.master = master  # for making  sure the window executed properly
        self.color_fg = 'black'  # pen color
        self.color_bg = 'white'  # background color of the canvas

        # X,Y coordinates of the pen using in the canvas cell
        self.coord_x = None
        self.coord_y = None

        self.canvas_width = 480
        self.canvas_height = 200
        self.pen_width = 3  # default width of the pen
        self.drawWidgets()

        # draw shapes for the motion of mouse
        self.c.bind('<B1-Motion>', self.paint,self.c.config(cursor="hand2"))  # key binding and mouse binding for motion of the mouse
        self.c.bind('<ButtonRelease-1>', self.reset)  # button press release

        # Create Horizontal line
        self.c.create_line(0, 220, self.canvas_width, 220, fill="#476042")
        self.write_active = False

    # moving of the pen in the canvas
    def paint(self, e):
        self.write_active = True
        if self.coord_x and self.coord_y:
            self.c.create_line(self.coord_x, self.coord_y, e.x, e.y, width=self.pen_width, fill=self.color_fg,capstyle=ROUND, smooth=True)

        # coordinates matching
        self.coord_x = e.x
        self.coord_y = e.y

    # erase all the drawings in the canvas
    def reset(self, e):
        self.coord_x = None
        self.coord_y = None

    def clear(self):
        self.c.delete(ALL)
        self.c.create_line(0, 220, self.canvas_width, 220, fill="#476042")
        self.write_active = False
        

    def drawWidgets(self):
        self.controls = Frame(self.master, padx=1, pady=5)
        # Create the message on top
        Label(self.controls, fg="black", text='Put your signature below',
              font=font.Font(family='Helvetica', size=12)).grid(row=0, column=0)
        self.controls.pack(side=TOP)

        self.c = Canvas(self.master, width=self.canvas_width, height=self.canvas_height, bg=self.color_bg, )
        self.c.pack(fill=BOTH, expand=True)

        btn1 = Button(root, text="Clear", font=('Arial 12'), command=self.clear, bg='gray', fg='black', height=1,width=23)
        btn1.pack(side=LEFT)

        btn2 = Button(root, text="Submit", font=('Arial 12'), command=self.screenshot, bg='gray', fg='black', height=1,width=26)
        btn2.pack(side=RIGHT)

    def exit(event):
        root.destroy()

    def screenshot(self):
        if self.write_active:
            x = root.winfo_rootx() + self.c.winfo_x()
            y = root.winfo_rooty() + self.c.winfo_y()
            xx = x + self.c.winfo_width()
            yy = y + self.c.winfo_height()
            image_name = "Images/%s.jpg" % (str(uuid.uuid1().int))
            ImageGrab.grab(bbox=(x, y, xx, yy)).save(image_name)

            #Create the binary Image
            with open(image_name, "rb") as image_file:
                data = base64.b64encode(image_file.read())
            f = open("sign.txt", "wb")
            f.write(data)
            f.close()
            #os.remove(image_name)
            self.clear()


if __name__ == '__main__':
    root = Tk()
    main(root)
    root.title('Signaure App')
    root.attributes('-fullscreen', True)
    root.wm_attributes('-topmost', 1)
    root.bind('<Escape>', exit)
    root.mainloop()
