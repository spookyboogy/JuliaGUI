if __name__ == '__main__': print('Importing...')
import numpy as np
from numpy import absolute as mod
from numpy.random import uniform as uni
from PIL.ImageTk import PhotoImage
from PIL import Image as Im
from threading import Thread
from tkinter import *
from tkinter import messagebox
from tkinter.ttk import *
import os
if __name__ == '__main__': print('Done.')


'''
A GUI for creating, displaying, exploring and saving julia set images.
'''


class julia(Frame):

    '''A widget for dynamically displaying julia sets.'''

    def __init__(self, master, a, b):
        
        Frame.__init__(self, master)
        self.pack(expand = True, fill = BOTH)

        if type(b) == complex:
            b = b.imag

        self.a, self.b = a, b
        self.w = 500; self.h = 500
        
        self.re_min, self.re_max = -2, 2
        self.im_min, self.im_max = -2, 2
        
        self.re_range = np.linspace(self.re_min, self.re_max,
                                  self.w)
        self.im_range = np.linspace(self.im_min, self.im_max,
                                  self.h)

        self.canvas = Canvas(self, height = self.h, width = self.h)
        self.canvas.pack(expand = True, fill = BOTH)

        self.filenum = 0
        self.fname = '{}.'.format(self.filenum)

        root.geometry('{}x{}+225+10'.format(self.w, self.h))
        root.update_idletasks()

        self.ImageEnvironment(newc=False)
        self.ControlPanel()
        try:
            self.image = PhotoImage(file = self.fname + '.pgm')
        except:
            self.generate(init=True)
        self.canvas.create_image((self.h/2, self.w/2), 
                                 image = self.image,
                                 tags = 'julia')


    def ControlPanel(self):

        
        self.side = Toplevel(root)
        self.side.title('Ctrl')
        self.side.geometry('165x265+45+10')
        self.instructions = Label(self.side,
                                  text = 'Change a and b values and hit\n'\
                                  'redraw to generate a \ndifferent set.\n'\
                                  '\nChoose values where \nabs(value) < 2'\
                                  '\n\n c = a + bi')
        self.instructions.grid(row = 0, columnspan = 2)
        
        self.alabel = Label(self.side, text = 'a =')
        self.blabel = Label(self.side, text = 'b =')
        self.alabel.grid(row = 1, column = 0)
        self.blabel.grid(row = 2, column = 0)
        
        self.acoord = Combobox(self.side,
                               textvariable = self.a,
                               values = [],
                               postcommand = self.coordlist,
                               width = 9)
        self.bcoord = Combobox(self.side,
                               textvariable = self.b,
                               values = [],
                               postcommand = self.coordlist,
                               width = 9)
        self.acoord.insert(0, self.a); self.bcoord.insert(0, self.b)
        self.acoord.propagate(flag=False);self.bcoord.propagate(flag=False)
        self.acoord.grid(row = 1, column = 1)
        self.bcoord.grid(row = 2, column = 1)
        self.acoords = []; self.bcoords = [] #for dropdown menu
        
        self.Redraw = Button(self.side,
                             text = 'redraw',
                             command = self.redraw)
        self.Zoom = Button(self.side,
                                 text = 'ZOOMBOX',
                                 command = self.zoombox)
        self.Resize = Button(self.side,
                             text = 'resize',
                             command = self.resize)
        self.SquareZoom = Button(self.side,
                             text = 'safe(r)zoom',
                             command = lambda: self.zoombox(square=True))
        
        self.Redraw.grid(row = 3, column = 0)        
        self.Zoom.grid(row = 3, column = 1)
        self.Resize.grid(row = 4, column = 0)
        self.SquareZoom.grid(row = 4, column = 1)

        self.back = Button(self.side, text = '<---',
                           command = lambda: self.filenav('back'))
        self.forward = Button(self.side, text = '--->',
                              command = lambda: self.filenav('forward'))
        self.back.grid(row = 5, column = 0)
        self.forward.grid(row = 5, column = 1)
        
        self.Randomizer = Button(self.side, text = 'Random',
                                 command = self.randomizer)
        self.Export = Button(self.side, text = 'Export',
                             command = self.export)
        self.Randomizer.grid(row = 6, column = 0)
        self.Export.grid(row = 6, column = 1)
    
    
    def coordlist(self):
        
        self.acoords.append(self.a); self.bcoords.append(self.b)
        self.acoords = list(set(self.acoords))
        self.bcoords = list(set(self.bcoords))
        
        self.acoord['values'] = self.acoords
        self.bcoord['values'] = self.bcoords
        self.acoord.update_idletasks; self.bcoord.update_idletasks

        
    def reset_defaults(self, resizing=False):
        
        print('In reset_defaults...')
        self.acoord.delete(0, END); self.acoord.insert(0, self.a)
        self.bcoord.delete(0, END); self.bcoord.insert(0, self.b)
        if not resizing:
            print('resizing = False')
            self.re_min, self.re_max = -2, 2
            self.im_min, self.im_max = -2, 2    
        else:
            print('resizing = True')
            # maybe create a separate folder
            self.re_min, self.re_max = self.re_range[0], self.re_range[-1]
            self.im_min, self.im_max = self.im_range[0], self.im_range[-1]

        self.filenum = 0
        
        self.re_range = np.linspace(self.re_min, self.re_max,
                                  self.w)
        self.im_range = np.linspace(self.im_min, self.im_max,
                                  self.h)
            
    
    def redraw(self):

        try:
            if type(eval(self.acoord.get())) == complex:
                x = eval(self.acoord.get()).real
            else:
                x = eval(self.acoord.get())
            
            if type(eval(self.bcoord.get())) == complex:
                y = eval(self.bcoord.get()).imag
            else:
                y = eval(self.bcoord.get())
        
            
            if self.a == x and self.b == y:
                print('no change in c')
                self.reset_defaults()
                self.fname = str(self.filenum) + self.fname[1:]
                self.newdisplay(nav=True)
            else:
                print('newc')
                self.a, self.b = x, y
                self.reset_defaults()
                self.fname = str(self.filenum) + self.fname[1:] # potent. problematic
                self.coordlist()
                self.ImageEnvironment(newc=True) 
                self.generate(init=True) #init prevents generate from incrementing filenum
                                    # ; an ugly and potentially problematic method
  
        except:
            messagebox.showinfo(title = 'Error',
                                message = 'Invalid coordinate entries.'\
                                ' Try again.')
            self.acoord.delete(0,END); self.bcoord.delete(0, END)
            self.acoord.insert(0, self.a); self.bcoord.insert(0, self.b)
            self.acoord.update_idletasks(); self.bcoord.update_idletasks()
            print('oooops\n(itsok)')

         
    def zoombox(self, square=False):
        '''Handles zoomstart and mousemovements and passes coords to s.zoom.'''

        self.Zoom.config(state = 'disabled')
        self.SquareZoom.config(state = 'disabled')
        
        self.x0, self.y0 = 0, 0
        self.x1, self.y1 = 0, 0
        self.canvas.create_rectangle(self.x0, self.y0,
                                     self.x1, self.y1, tags = 'box')
        
        def pivot(event):
            
            self.x0, self.y0 = event.x, event.y
            print('\nx0, y0: {}, {}'.format(self.x0, self.y0))

        def boxdraw(event):
            
            self.canvas.coords('box', self.x0, self.y0, event.x, event.y)

        def squaredraw(event):
            
            self.sidelength = abs(event.x - self.x0)
            
            if self.y0 >= event.y:
                ypixel = self.y0 - self.sidelength
            else:
                ypixel = self.y0 + self.sidelength
                
            self.canvas.coords('box', self.x0, self.y0, event.x, ypixel)
            
        def finish(event):

            self.x1 = event.x
            if not square:
                self.y1 = event.y
            else:
                if self.y0 >= event.y:
                    self.y1 = self.y0 - self.sidelength
                else:
                    self.y1 = self.y0 + self.sidelength
            
            print('x1, y1: {}, {}'.format(self.x1, self.y1))
            
            self.canvas.unbind('<Button-1>')
            self.canvas.unbind('<Button1-Motion>')
            self.canvas.unbind('<ButtonRelease-1>')
            self.zoom(self.x0, self.y0, self.x1, self.y1)

        self.canvas.bind('<Button-1>', pivot)
        if not square:
            self.canvas.bind('<Button1-Motion>', boxdraw)
        else:
            self.canvas.bind('<Button1-Motion>', squaredraw)
        self.canvas.bind('<ButtonRelease-1>', finish)


    def zoom(self, x0, y0, x1, y1):
        '''Redefines re_range and im_range according to zoom coordinates.'''

        if x0 > x1:
            print('\nbackwards xbox')
            x0, x1 = x1, x0    
        else:
            if x0 == x1: x1 += 2

        if y0 > y1:
            print('also backwards')
            y0, y1 = y1, y0 
        else:
            if y0 == y1: y1 += 2
        
        r0, r1 = self.re_range[x0], self.re_range[x1]
        i0, i1 = self.im_range[-y1], self.re_range[-y0]

        rrange = self.re_range = np.linspace(r0, r1, self.w)
        irange = self.im_range = np.linspace(i0, i1, self.h)

        print('\nzoom area:\nre_range = [{}, {}]\nim_range = [{}, {}]'
              .format(rrange[0], rrange[-1], irange[0], irange[-1]))

        self.generate()


    def resize(self):

        EntryWindow = Toplevel(root)
        EntryWindow.title('Enter Dimensions')
        #consider having a set geometry for EntryWindow
        caution = Label(EntryWindow,
                        text = '\nWarning:\n The larger the window,'\
                        ' the longer the render time.\n Sqaure resolutions'\
                        ' are strongly recommended.\nAlso, it\'s probably'\
                        ' best not to enter resolutions\ngreater than that'\
                        ' of your own screen.\n')
        caution.grid(row = 0, columnspan = 2)
        
        widthlabel = Label(EntryWindow, text = 'Width =')
        heightlabel = Label(EntryWindow, text = 'Height =')
        widthlabel.grid(row = 1, column = 0)
        heightlabel.grid(row = 2, column = 0)

        new_width = Entry(EntryWindow); new_height = Entry(EntryWindow)
        new_width.insert(0, self.w); new_height.insert(0, self.h)
        new_width.grid(row=1, column=1); new_height.grid(row=2, column=1)
        
        def finalize(*kwargs):

            try:
                self.w = int(eval(new_width.get()))
                self.h = int(eval(new_height.get()))
            except:
                messagebox.showinfo(title = 'Error',
                                    message = 'Invalid Dimension Entries')
                EntryWindow.lift()
                return

            #unnecessarily (safe/) complicated way of creating geometry string
            s = old_geometry = root.geometry()
            self.new_geometry = s[:s.index('x')]\
                                .replace(s[:s.index('x')], str(self.w))\
                                + 'x' + s[s.index('x') + 1:s.index('+')]\
                                .replace(s[s.index('x') + 1:s.index('+')],\
                                         str(self.h))\
                                + s[s.index('+'):]

            EntryWindow.destroy()
            self.reset_defaults(resizing = True)
            self.generate(resizing = True)
        
        done = Button(EntryWindow, text = 'Done', command = finalize)
        done.grid(row = 3, column = 1)
        EntryWindow.bind('<Return>', finalize)
        
        # encourage or enforce square resolution
        # if not square consider extending accordingly
        # the ranges to fill the canvas
    
    def randomizer(self):

        self.acoord['values'] += (self.a,)
        self.bcoord['values'] += (self.b,)
        self.a = np.round(uni(-1.3, 1.3), decimals = 5)
        self.b = np.round(uni(-1.3, 1.3), decimals = 5)
        self.ImageEnvironment(newc=True)
        self.reset_defaults()
        self.generate(init=True)
        
    
    def generate(self, init=False, resizing=False):
        '''Creates the pgm file to be displayed.'''
        
        c = complex(self.a, self.b)
        boundary = max(mod(c), 3)
        data = []

        self.pgBar = Progressbar(self.side,
                            mode = 'determinate',
                            orient = 'horizontal',
                            maximum = len(self.re_range),
                            length = 165)
        self.pgBar.grid(row = 7, columnspan = 2)

        self.side.geometry('165x285+45+10')        
        root.title('Working...'); print('\nWorking...')
        
        for im in self.im_range[::-1]:
            self.pgBar.step(1); self.pgBar.update_idletasks()
            for re in self.re_range:
                n = 255
                z = complex(re, im)
                while n >= 5 and mod(z) < boundary:
                    z = z**2 + c
                    n -= 5
                data.append(n)
                
        root.title('tk'); print('Done.')
        self.side.geometry('165x265+45+10')

        if not init:
            self.filenum += 1
            self.fname = str(self.filenum) + self.fname[1:]
        else:
            pass
        
        print('writing pgm file with\nwidth = {}\nheight = {}'
              .format(self.w, self.h))
        print('\nzoom area:\nre_range = [{}, {}]\nim_range = [{}, {}]'
              .format(self.re_range[0], self.re_range[-1],
                      self.im_range[0], self.im_range[-1]))

        writeP5pgm(data, self.fname, self.w, self.h)
        

        print('\nfname = {}'.format(self.fname))

        if not resizing:
            self.newdisplay()
        else:
            self.newdisplay(resizing=True)

        
    def newdisplay(self, resizing=False, nav=False):

        try:
            self.pgBar.destroy()
        except:
            pass
        
        self.image = PhotoImage(file = self.fname + '.pgm')

        #ugly logic scheme
        if not resizing:
            if not nav: # from zoom
                self.canvas.delete('box')
                self.Zoom.config(state = 'enabled')
                self.SquareZoom.config(state = 'enabled')
                self.Redraw.config(state = 'enabled')
                self.canvas.itemconfigure('julia', image = self.image)
            else: #from nav
                self.canvas.itemconfigure('julia', image = self.image)
        else:
            self.canvas.delete('julia')
            self.canvas.create_image((self.h/2, self.w/2),
                                 image = self.image,
                                 tags = 'julia')
            try:
                root.geometry(self.new_geometry)
                root.update_idletasks()
            except:
                pass
            

    def export(self):
        
        #have a dialog box open asking for:
        #    -desired resolution
        #    -desired save location
        #eventually allow for different format conversion
        pass
    
    
    def ImageEnvironment(self, newc=False):

        if not newc: #init
            
            if not 'Julia Set Images' in os.listdir(os.getcwd()):
                os.mkdir('Julia Set Images')
            else:
                pass
            os.chdir('Julia Set Images')
            
            if not 'c = {} + {}j'.format(self.a, self.b) in os.listdir(os.getcwd()):
                print('c folder yet to be created. creating.')
                os.mkdir('c = {} + {}j'.format(self.a, self.b))
            else:
                pass
            os.chdir('c = {} + {}j'.format(self.a, self.b))
                
        else: #newc
            print('newc')
            os.chdir('..')
            if not 'c = {} + {}j'.format(self.a, self.b) in os.listdir(os.getcwd()):
                print('new c folder to be created')
                os.mkdir('c = {} + {}j'.format(self.a, self.b))
                print('new c folder created')
            os.chdir('c = {} + {}j'.format(self.a, self.b))

        
    def filenav(self, direction):
        '''not accounting for double digit filenumbers'''
        if direction == 'back':
            if eval(self.fname[0]) == 0:
                return
            else:
                self.filenum -= 1
                self.fname = str(self.filenum) + self.fname[1:]
                self.newdisplay(nav = True)
        else:
            for item in os.listdir(os.getcwd()):
                if eval(item[0]) - 1 == self.filenum:
                    print('item[0] = {}'.format(item[0]))
                    self.filenum += 1
                    self.fname = str(self.filenum) + self.fname[1:] 
                    self.newdisplay(nav=True)
                    return
                else:
                    pass
        
        
        

def writeP5pgm(data, fname, width, height):
    '''
    Creates a binary pgm image from julia set pixel data.
    '''
    
    with open(fname + '.pgm', 'w') as fout:
        fout.write('P5\n')
        fout.write('{} {}\n'.format(width, height))
        fout.write('255\n ')
    with open(fname + '.pgm', 'ab') as fout:
        fout.write(np.array(data, dtype ='uint8').tostring())

        
if __name__ == '__main__':

    root = Tk()
    j = julia(root, -1.25, .07j)
    
    j.pack()
    root.mainloop()
    

#### Notes ####

# - figure out why image generation is not working on small scales,
# - Make a forward and back function by:
####   having filenames be generated with numbers at the end
####   and having back/forward display the previous or next image
####   OR:
####   develop a file class holding all file info and a queue manager...
####   maybe make a full file system explorer
####   OR:
####   Use nested lists and recursion
# - Make a pgm -> png export function, possibly with file system gui;
#   Get familiar with and implement pythonmagick for that
# - Build an exe and app from source when finished
# - learn the potential for compression and bundling when installing versus
#   making an executable with spare dll's
