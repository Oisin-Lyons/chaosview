"""Version 2 - Distribution"""

from numpy import *
from numpy.random import rand
from tkinter import filedialog
from tkinter import *
from PIL import Image, ImageDraw
from pickle import dump, load
from imageio import mimsave

root = Tk()

savedict = {}
T = 0.0
A = 5
canvdim = 650
rad = 0.1
tint = 0.1
p1,p2 = (0,0),(0,0)
n = 500
playing = False
blobcount = 0
selecting = False
selector = None
colour = StringVar(); colour.set("black")
resetpoints = []
colours = []
animating = False
frames = []

#Advection funcs

def pmod(p):
    while p[0] > pi:
        p[0] -= 2*pi
    while p[0] < -1*pi:
        p[0] += 2*pi
    while p[1] > pi:
        p[1] -= 2*pi
    while p[1] < -1*pi:
        p[1] += 2*pi
    return p

def Tmodulus(T):
    while T >= 1:
        T -= 1
    while T < 0:
        T += 1    
    return T

def adv(p, axis, t):
    if axis == 'x':
        vx = A*sin(p[1])
        p[0] += vx*t
    elif axis == 'y':
        vy = A*sin(p[0])
        p[1] += vy*t
    return pmod(p)

def cycle(p, count):
    if count >= 0:
        for i in range(count):
            p = adv(p,'x',0.5)
            p = adv(p,'y',0.5)
    elif count < 0:
        for i in range(-1*count):
            p = adv(p,'y',-0.5)
            p = adv(p,'x',-0.5)
    return p

def evolve0(p,t):
    if t == round(t):
        p = cycle(p,int(t))
    else:
        if t >= 0:
            count = 0
            while t > 1:
                t -= 1
                count += 1
            p = cycle(p,count)
            if t < 0.5:
                p = adv(p,'x',t)
            else:
                p = adv(p,'x',0.5)
                p = adv(p,'y',t-0.5)
            
        elif t < 0:
            count = 0
            while t < -1:
                t += 1
                count -= 1
            p = cycle(p,count)

            if t >= -0.5:
                p = adv(p,'y',t)
            else:
                p = adv(p,'y',-0.5)
                p = adv(p,'x',t+0.5)
    return p

def evolvepoint(p, t):
    Tmod = Tmodulus(T)
    
    if Tmod == 0:
        return evolve0(p,t)
    
    elif Tmod < 0.5 and t >= 0:
        if Tmod + t < 0.5:
            p = adv(p,'x',t)
            
        elif Tmod + t < 1:
            p = adv(p,'x',0.5-Tmod)
            p = adv(p,'y',Tmod+t-0.5)

        elif Tmod + t >= 1:
            p = adv(p,'x',0.5-Tmod)
            p = adv(p,'y',0.5)
            t -= (1 - Tmod)
            p = evolve0(p,t) 
            
    elif Tmod < 1 and t >= 0:
        if Tmod + t < 1:
            p = adv(p,'y',t)
            
        elif Tmod + t >= 1:
            p = adv(p,'y',1-Tmod)
            t -= (1 - Tmod)
            p = evolve0(p,t)
    
    elif Tmod < 0.5 and t < 0:
        if Tmod + t >= 0:
            p = adv(p,'x',t)
        elif Tmod + t < 0:
            p = adv(p,'x',-1*Tmod)
            t += Tmod
            p = evolve0(p,t)
        
    elif Tmod < 1 and t < 0:
        if Tmod + t >= 0.5:
            p = adv(p,'y',t)
        elif Tmod + t >= 0:
            p = adv(p,'y',0.5-Tmod)
            p = adv(p,'x',t+(Tmod-0.5))
        elif Tmod + t < 0:
            p = adv(p,'y',0.5-Tmod)
            p = adv(p,'x',-0.5)
            t += Tmod
            p = evolve0(p,t)
    return p

def getpoints(p1, p2, n):
    x = (p1[0] + (p2[0]-p1[0])*rand(n)).reshape(n,1)
    y = (p1[1] + (p2[1]-p1[1])*rand(n)).reshape(n,1)
    points = column_stack((x,y))
    return points

def evolve(pts,t):
    global T
    for p in pts:
        p = evolvepoint(p,t)
    T += t
    return pts

points = getpoints(p1,p2,0)

#GUI funcs

def setA(*args):
    global A
    A = A_scale.get()
    
def settint(*args):
    global tint
    tint = tint_scale.get()
    
def update():
    Time.config(text="T = "+str(round(T,2)))
    animate()

def paint(p,colour):
    x = (p[0]+pi)*canvdim/(2*pi)
    y = (pi-p[1])*canvdim/(2*pi)
    canvas.create_rectangle(x-rad,y-rad,x+rad,y+rad,outline=colour)
    
def paintpts(*args):
    canvas.delete("all")
    for i in range(blobcount):
        for p in points[i*n:(i+1)*n]:
            paint(p,colours[i])
            
def forward(*args):
    global points
    points = evolve(points, tint)
    paintpts()
    update()
    
def backward(*args):
    global points
    points = evolve(points, -1*tint)
    paintpts()
    update()
    
def start():
    global playing
    playing = True
    fplay.config(text="Stop")
    
def stop():
    global playing
    playing = False
    fplay.config(text="Play")
    
def reset():
    global T, points
    stop()
    T = 0.0; update()
    points = getpoints((0,0),(0,0),0)
    for i in [2*i for i in range(blobcount)]:
        points = vstack((points,getpoints(resetpoints[i],resetpoints[i+1],n)))
    paintpts()
    
def zero():
    global points
    stop()
    points = evolve(points, -1*T)
    paintpts()
    update()

def clear():
    global T, points, blobcount, resetpoints, colours
    stop()
    T = 0.0; update()
    points = getpoints((0,0),(0,0),0)
    blobcount = 0
    resetpoints = []
    colours = []
    paintpts()
    
def play():
    if playing:
        forward()
        root.after(100,play)
    
def forwardplay(*args):
    if playing:
        stop()
    else:
        start()
    play()

def update_selector(event):
    global selector
    canvas.delete(selector)
    if selecting:
        x1 = (p1[0]+pi)*canvdim/(2*pi)
        y1 = (pi-p1[1])*canvdim/(2*pi)
        selector = canvas.create_rectangle((x1,y1),(event.x,event.y),outline=colour.get())
        
def createblob(event):
    global selecting, resetpoints
    x = (event.x*2*pi/canvdim)-pi
    y = pi-(event.y*2*pi/canvdim)
    if str(event.type) == "ButtonPress":
        global p1
        p1 = (x,y)
        selecting = True
        resetpoints.append(p1)
    elif str(event.type) == "ButtonRelease":
        global p2, points, blobcount, colours
        p2 = (x,y)
        points = vstack((points,getpoints(p1,p2,n)))
        blobcount += 1
        selecting = False
        resetpoints.append(p2)
        colours.append(colour.get())
        paintpts()

def makeimage():
    image = Image.new("RGB",(canvdim,canvdim),"white")
    draw = ImageDraw.Draw(image)
    for i in range(blobcount):
        for p in points[i*n:(i+1)*n]:
            x = (p[0]+pi)*canvdim/(2*pi)
            y = (pi-p[1])*canvdim/(2*pi)
            draw.rectangle([x-rad,y-rad,x+rad,y+rad], colours[i])
    return image
     
def save():
    image = makeimage()
    filename = filedialog.asksaveasfilename(initialdir="/",title="Save Image",
                                            filetypes=[("gif","*.gif"),("jpeg","*.jpg"),("png","*.png")])
    image.save(filename)
    
def quit():
    stop()
    def no(*args):
        window.destroy()
        root.destroy()
    def yes(*args):
        window.destroy()
        global savedict
        savedict['A'] = A
        savedict['T'] = T
        savedict['tint'] = tint
        savedict['points'] = points
        savedict['blobcount'] = blobcount
        savedict['resetpoints'] = resetpoints
        savedict['colours'] = colours
        savedict['colour'] = colour.get()
        filename = filedialog.asksaveasfilename(initialdir="/",title="Save",defaultextension=".pickle")
        with open(filename,'wb') as f:
            dump(savedict, f)
        root.destroy()
        
    def cancel(*args):
        window.destroy()
                
    window = Toplevel(root)
    Label(window,text="Save Progress?",bg=grey2).grid(columnspan=3)
    Button(window,text="No",padx=10,command=no).grid(row=1)
    Button(window,text="Yes",padx=10,command=yes).grid(row=1,column=1)
    Button(window,text="Cancel",padx=10,command=cancel).grid(row=1,column=2)
    window.bind("<n>",no)
    window.bind("<y>",yes)
    window.bind("<c>",cancel)
    
def progload():
    global A, T, tint, points, blobcount, resetpoints, colours, colour
    filename = filedialog.askopenfilename(initialdir="/",filetypes=[("pickle file","*.pickle")])
    with open(filename,'rb') as f:
        loaddict = load(f)
    A = loaddict['A']
    T = loaddict['T']
    tint = loaddict['tint']
    points = loaddict['points']
    blobcount = loaddict['blobcount']
    resetpoints = loaddict['resetpoints']
    colours = loaddict['colours']
    colour.set(loaddict['colour'])
    
    A_scale.set(A)
    tint_scale.set(tint)
    paintpts()
    update()
    
def animate():
    if animating:
        global frames
        frame = makeimage()
        frames.append(array(frame.getdata()).reshape(canvdim, canvdim, 3))
    
def animation():
    global animating
    if not animating:
        animating = True
        abutton.config(text="End Animation",padx=14)
        animate()
    else:   
        animating = False
        abutton.config(text="Create Animation",padx=5)
        global frames
        filename = filedialog.asksaveasfilename(initialdir="/",title="Save Animation",defaultextension=".gif")
        mimsave(filename, frames)
        frames = []
    
def helpwindow():
    window = Toplevel(root)
    T = Label(window,width=75,justify=LEFT)
    T.grid()
    T.config(text='Help not currently available')
    Button(window,text="OK",command=window.destroy).grid(row=1)
    
#GUI
   
grey1 = "#cccccc"
grey2 = "#eeeeee"

root.title("Chaos Simulator")
root.bind("<space>",forwardplay)
root.bind("<Right>",forward)
root.bind("<Left>",backward)

Label(root,text="Control Panel",font="Lucida 14 bold",bg=grey1,padx=50).grid(row=0,columnspan=2,padx=(10,0),pady=10)

Frame(height=100,width=180,bd=5,relief=RAISED).grid(row=1,columnspan=2,padx=(10,0),pady=(0,15))
Frame(height=100,width=180,bd=5,relief=RAISED).grid(row=2,columnspan=2,padx=(10,0),pady=(0,15))
Frame(height=100,width=180,bd=5,relief=RAISED).grid(row=3,columnspan=2,padx=(10,0),pady=(0,10))
Frame(height=100,width=180,bd=5,relief=RAISED).grid(row=4,columnspan=2,padx=(10,0),pady=(0,10))

Label(root,text="Flow amplitude",bg=grey2,relief=RAISED).grid(row=1,columnspan=2,sticky=N)
A_scale = Scale(root,from_=0.5,to=20,orient=HORIZONTAL,length=150,resolution=0.5,tickinterval=19.5,command=setA)
A_scale.set(5)
A_scale.grid(row=1,columnspan=2)

Label(root,text="Frame duration",bg=grey2,relief=RAISED).grid(row=2,columnspan=2,sticky=N)
tint_scale = Scale(root,from_=0.01,to=1,orient=HORIZONTAL,length=150,resolution=0.01,tickinterval=0.99,command=settint)
tint_scale.set(0.1)
tint_scale.grid(row=2,columnspan=2)

Label(root,text="Playback",bg=grey2,relief=RAISED).grid(row=3,columnspan=2,sticky=N)
fplay = Button(root,text="Play",command=forwardplay,padx=10)
fplay.grid(row=3,columnspan=2,pady=(0,20))
Button(root,text=">>",command=forward,padx=5).grid(row=3,column=1,pady=(0,20))
Button(root,text="<<",command=backward,padx=5).grid(row=3,column=0,pady=(0,20))
Time = Label(root,text="T = 0",bg=grey2,relief=SUNKEN)
Time.grid(row=3,columnspan=2,pady=(50,0))

Label(root,text="Colour selection",bg=grey2,relief=RAISED).grid(row=4,columnspan=2,sticky=N)
colourmenu = OptionMenu(root,colour,'black','red','green','blue','yellow','cyan','magenta','white')
colourmenu.grid(row=4,columnspan=2)

Label(root,text="Click and drag to set regions",bg=grey2).grid(row=0,column=2,columnspan=2,sticky=N)
canvas = Canvas(root,width=canvdim,height=canvdim,bg="#f4f4f4")
canvas.grid(row=0,rowspan=6,column=2,columnspan=2,padx=20,pady=20)
canvas.bind("<Button-1>",createblob)
canvas.bind("<ButtonRelease-1>",createblob)
canvas.bind("<Motion>",update_selector)

Button(root,text="Reset",command=reset,padx=5,pady=5).grid(row=5,sticky=S)
Button(root,text="Zero",command=zero,padx=5,pady=5).grid(row=5,columnspan=2,sticky=S)
Button(root,text="Clear",command=clear,padx=5,pady=5).grid(row=5,column=1,sticky=S)
Button(root,text="Save Image",command=save,pady=5).grid(row=5,column=2,sticky=S)
abutton = Button(root,text="Create Animation",command=animation,padx=5,pady=5); abutton.grid(row=5,column=2,sticky=SW)
Button(root,text="Help",command=helpwindow).grid(row=5,column=3,sticky=SE)
Button(root,text="Load",command=progload,padx=5,pady=5).grid(row=5,column=3,sticky=SW)
Button(root,text="Quit",command=quit,padx=5,pady=5).grid(row=5,column=3,sticky=S)

root.mainloop()
