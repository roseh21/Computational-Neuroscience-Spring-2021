from sys import platform
from tkinter import *
import math
import numpy as np
import random
import Synapse_P02mm as Synapse
keepgoing = 0
white =     "#ffffff"
magenta =   "#ff99ff"
cyan =      "#00EEEE"
green =     "#C0FF3E"
yellow =    "#FFFF00"
orange =    "#FF8000"
blue =      "#00BFFF"
Na_Percent = 1.0
K_Percent = 1.0
h_Percent = 1.0
HoldVm = -80.0
StepVm = 0.0
################################################################################
class Window(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.MacOffset = 0
        self.simToRun = 1
        self.storage = 1
        self.doOnce = 0
        self.simSpeed = 1
        self.animate = 0
        self.skipPoints = 1
        self.animateSweep = 0
        self.mainWinwidth = 1000
        self.mainWinheight = 600 

        self.master = master
        self.simToRun = 1
        if platform == 'darwin':  # menu bars for Mac, they are fussy
            
            mymenubar = Frame(MW, relief='raised', bd=2)
            mymenubar.pack(fill=X)
            button1 = Menubutton(mymenubar, text='Sim Type')
            button1.pack(side=LEFT)
            mymenu1 = Menu(button1, tearoff=0)
            button1['menu'] = mymenu1
            mymenu1.add_radiobutton(label="My simulation", variable = self.simToRun, value = 1, command = lambda: self.changeSim(1))
            mymenu1.add_radiobutton(label="Squid action potential", variable = self.simToRun, value = 2, command = lambda: self.changeSim(2))
            mymenu1.add_radiobutton(label="Squid voltage clamp", variable = self.simToRun, value = 3, command = lambda: self.changeSim(3))
            mymenu1.add_radiobutton(label="Stomatogastric neuron", variable = self.simToRun, value = 4, command = lambda: self.changeSim(4))
            mymenu1.add_radiobutton(label="Inferior Olive Neuron", variable = self.simToRun, value = 5, command = lambda: self.changeSim(5))
            mymenu1.add_radiobutton(label="Izhekavich neuron", variable = self.simToRun, value = 6, command = lambda: self.changeSim(6))
            mymenu1.add_radiobutton(label="Leaky integrate-and-fire neuron", variable = self.simToRun, value = 7, command = lambda: self.changeSim(7))
            mymenu1.invoke(1)
            
            button2 = Menubutton(mymenubar,text='     Run Pause Stop   ' )
            button2.pack(side=LEFT)
            mymenu2 = Menu(button2, tearoff=0)
            button2['menu'] = mymenu2

            mymenu2.add_command(label="View params",command=self.View)
            mymenu2.add_command(label='Continuous/Pause', command = self.run)
            mymenu2.add_command(label='Run One', command=self.hold)

            button3 = Menubutton(mymenubar,text='     Store   Clear   ' )
            button3.pack(side=LEFT)
            mymenu3 = Menu(button3, tearoff=0)
            button3['menu'] = mymenu3
            mymenu3.add_command(label='Store Sweep', command = self.changeStorage)
            mymenu3.add_command(label='Clear',command=self.clearScreen)
        
            button5 = Menubutton(mymenubar,text='     Exit   ' )
            button5.pack(side=LEFT)
            mymenu5 = Menu(button5, tearoff=0)
            button5['menu'] = mymenu5
            mymenu5.add_command(label=' Exit ', command = self.exitProgram)  
            self.MacOffset=-10
        else:   #menu bars for PC and linux
            menu = Menu(self.master)
            self.master.config(menu=menu)
            simMenu = Menu(menu)
            menu.add_cascade(label="Sim Type", menu=simMenu)
            
            simMenu.add_radiobutton(label="My simulation", variable = self.simToRun, value = 1, command = lambda: self.changeSim(1))
            simMenu.add_radiobutton(label="Squid action potential", variable = self.simToRun, value = 2, command = lambda: self.changeSim(2))
            simMenu.add_radiobutton(label="Squid voltage clamp", variable = self.simToRun, value = 3, command = lambda: self.changeSim(3))
            simMenu.add_radiobutton(label="Stomatogastric neuron", variable = self.simToRun, value = 4, command = lambda: self.changeSim(4))
            simMenu.add_radiobutton(label="Inferior Olive Neuron", variable = self.simToRun, value = 5, command = lambda: self.changeSim(5))
            simMenu.add_radiobutton(label="Izhekavich neuron", variable = self.simToRun, value = 6, command = lambda: self.changeSim(6))
            simMenu.add_radiobutton(label="Leaky integrate-and-fire neuron", variable = self.simToRun, value = 7, command = lambda: self.changeSim(7))
            simMenu.invoke(1)
           
            menu.add_separator()
            menu.add_separator()
            menu.add_separator()
            menu.add_command(label="Continuous/Pause",command=self.run)
            menu.add_separator()
            menu.add_separator()
            menu.add_separator()
            menu.add_command(label="Run one",command=self.hold)
            menu.add_separator()
            menu.add_separator()
            menu.add_separator()
            menu.add_command(label="StoreSweep",command = self.changeStorage)
            menu.add_separator()
            menu.add_separator()
            menu.add_separator()
            menu.add_command(label="Clear",command=self.clearScreen)
            menu.add_separator()
            menu.add_separator()
            menu.add_separator()
            speedMenu = Menu(menu)
            menu.add_cascade(label="Speed", menu=speedMenu)
            speedMenu.add_radiobutton(label='auto',variable=self.simSpeed,value = 1, command = lambda:self.changeSpeed(0))
            speedMenu.add_radiobutton(label="1",variable=self.simSpeed, value = 2,command = lambda:self.changeSpeed(1))
            speedMenu.add_radiobutton(label="2",variable=self.simSpeed, value = 3,command = lambda:self.changeSpeed(2))
            speedMenu.add_radiobutton(label="3",variable=self.simSpeed, value = 4,command = lambda:self.changeSpeed(3))
            speedMenu.add_radiobutton(label="5",variable=self.simSpeed, value = 5,command = lambda:self.changeSpeed(5))
            speedMenu.add_radiobutton(label="10",variable=self.simSpeed, value = 6,command = lambda:self.changeSpeed(10))
            speedMenu.add_radiobutton(label="20",variable=self.simSpeed, value = 7,command = lambda:self.changeSpeed(20))
            speedMenu.add_radiobutton(label="35",variable=self.simSpeed, value = 8,command = lambda:self.changeSpeed(35))
            speedMenu.add_radiobutton(label="50",variable=self.simSpeed, value = 9,command = lambda:self.changeSpeed(50))
            speedMenu.add_radiobutton(label="75",variable=self.simSpeed, value = 10,command = lambda:self.changeSpeed(75))
            speedMenu.add_radiobutton(label="100",variable=self.simSpeed, value = 11,command = lambda:self.changeSpeed(100))
            speedMenu.add_radiobutton(label="150",variable=self.simSpeed, value = 12,command = lambda:self.changeSpeed(150))
            speedMenu.add_radiobutton(label="200",variable=self.simSpeed, value = 13,command = lambda:self.changeSpeed(200))
            speedMenu.add_radiobutton(label="250",variable=self.simSpeed, value = 14,command = lambda:self.changeSpeed(250))
            speedMenu.invoke(1)
            self.skipPoints = 0
            menu.add_separator()
            menu.add_separator()
            menu.add_separator()
            # animateMenu = Menu(menu)
            # menu.add_cascade(label="Animate", menu=animateMenu)
            # animateMenu.add_radiobutton(label='Animate Off', variable=self.animate, value = 0,command = lambda:self.changeAnimate(0))
            # animateMenu.add_radiobutton(label='Animate On', variable=self.animate, value=1,command = lambda:self.changeAnimate(1))
            # animateMenu.invoke(1)
            menu.add_separator()
            menu.add_separator()
            menu.add_separator()
            menu.add_command(label="Exit", command=self.exitProgram)
            menu.add_separator()
            menu.add_separator()
            menu.add_separator()
            menu.add_command(label="View params",command=self.View)
        MW.geometry("1000x600+0+0")
        MW.wm_title("Neuron Simulator for PC Mac and Linux")
        self.canvas = Canvas(MW, width=self.mainWinwidth, height=self.mainWinheight, bg="#000000")
        self.canvas.pack()
        self.img = PhotoImage(width=self.mainWinwidth, height=self.mainWinheight)
        self.canvas.create_image((self.mainWinwidth//2, self.mainWinheight//2), image=self.img, state="normal")
    def changeSim(self,newsim):
        self.simToRun = newsim
        # if newsim ==2 or newsim == 3:
        #     PW.deiconify()
    def run(self):
        global keepgoing
        keepgoing = 1 - keepgoing
        if keepgoing == 1: runSim()
    def hold(self):
        global keepgoing
        keepgoing = 1 
        self.doOnce = 1
        runSim()
    def clearScreen(self):
        self.canvas.delete("all")
    def changeStorage(self):
        self.storage = 1- self.storage
    def changeSpeed(self,speed):
        self.skipPoints = speed
    def changeAnimate(self,newVal): 
        self.animateSweep = newVal
    def exitProgram(self):
        global keepgoing
        keepgoing = 0
        exit()
    def simple(self,data):
        self.DrawSweep(data,0,0,0,white)
    def View(self):
        #viewParams()
        print('option disabled')

    def ParmView(self,data,sweepColor):
        #Max = 1.2
        #Min = -.2
        yOffset = 0
        numpoints = len(data)
        xscale = self.mainWinwidth/numpoints
        #if (Max == 0) and (Min ==0):
        mx = max(data)
        mn = min(data)
        inc = int((mx-mn)*.1)
        Max = mx + inc
        Min = mn - inc
        yscale = (self.mainWinheight)/(Max-Min)
        for x in range(1,numpoints):
            x1 = x * xscale
            r = 1
            yNew = int((Max-data[x])*yscale)+yOffset
            self.canvas.create_oval(x1-r,yNew-3,x1+r,yNew+r, width=2, outline = sweepColor, fill = sweepColor)
        mainWin.update()
       
    def DrawSweep(self,data,drawMode,Max,Min,sweepColor):
        yOffset = 0
        if (Max == 0) and (Min ==0):
            mx = max(data)
            mn = min(data)
            inc = int((mx-mn)*.1)
            Max = mx + inc
            Min = mn - inc
        yscale = (self.mainWinheight)/(Max-Min)
        if drawMode == 1: # top half
            yscale = yscale *.5
            yOffset = 0
        elif drawMode == 2:
            yscale = yscale * .5
            yOffset = int(self.mainWinheight/2)
        elif drawMode ==3:
            yscale = yscale *.33
            yOffset = 0
        elif drawMode ==4:
            yscale = yscale *.33
            yOffset = int(self.mainWinheight/3)
        elif drawMode ==5:
            yscale = yscale *.33
            yOffset = int(2*self.mainWinheight/3)
        numpoints = len(data)
        yOffset = yOffset+self.MacOffset
        if self.skipPoints==0:
            self.skipPoints = int(numpoints/self.mainWinwidth)-1
        if self.skipPoints<1:self.skipPoints=1
        xscale = self.mainWinwidth/numpoints
        yOld =  int((Max-data[0])*yscale)
        global keepgoing
        if self.storage == 0: 
            self.canvas.delete("all")
        
        if self.animateSweep == 0:
            for x in range(1,numpoints,self.skipPoints):
                x1 = x * xscale
                yNew = int((Max-data[x])*yscale)+yOffset
                self.canvas.create_line(x1-1,yOld,x1,yNew, fill = sweepColor)
                yOld = yNew
            if self.doOnce == 1:
                keepgoing = 0
                self.doOnce = 0
            mainWin.update()
        else:
            for x in range(1,numpoints,self.skipPoints):
                x1 = (x * xscale)
                yNew = int((Max-data[x])*yscale)+yOffset
                self.canvas.create_line(x1-1,yOld,x1,yNew, fill = sweepColor)
                yOld = yNew
                mainWin.update()
            if self.doOnce == 1:
                keepgoing = 0
                self.doOnce = 0
        mainWin.update()
        return Max,Min
    def DrawPoint(self,x,y,numpoints,drawMode,Max,Min,sweepColor):
        if self.storage == 0 and x == 1:
            self.clearScreen()
        yOffset = 0
        yscale = self.mainWinheight/(Max-Min)
        if drawMode == 1: # top half
            yscale = yscale *.5
            yOffset = 0
        elif drawMode == 2:
            yscale = yscale * .5
            yOffset = int(self.mainWinheight/2)
        elif drawMode ==3:
            yscale = yscale *.33
            yOffset = 0
        elif drawMode ==4:
            yscale = yscale *.33
            yOffset = int(self.mainWinheight/3)
        elif drawMode ==5:
            yscale = yscale *.33
            yOffset = int(2*self.mainWinheight/3)
        xscale = self.mainWinwidth/numpoints
        x1 = (x * xscale)

        yNew = int((Max-y)*yscale)+yOffset+self.MacOffset
        r = 1
        self.canvas.create_oval(x1,yNew,x1+r,yNew+r, width=1, outline = sweepColor, fill = sweepColor)
        global keepgoing
        if self.doOnce == 1:
            keepgoing = 0
            self.doOnce = 0
        mainWin.update()
    def DrawSpike(self,x,Vm,amp,numpoints,drawMode,Max,Min,sweepColor):
        yOffset = 0
        yscale = self.mainWinheight/(Max-Min)
        if drawMode == 1: # top half
            yscale = yscale *.5
            yOffset = 0
        elif drawMode == 2:
            yscale = yscale * .5
            yOffset = int(self.mainWinheight/2)
        elif drawMode ==3:
            yscale = yscale *.33
            yOffset = 0
        elif drawMode ==4:
            yscale = yscale *.33
            yOffset = int(self.mainWinheight/3)
        elif drawMode ==5:
            yscale = yscale *.33
            yOffset = int(2*self.mainWinheight/3)
        xscale = self.mainWinwidth/numpoints
        x1 = x * xscale
        V = int((Max-Vm)*yscale)+yOffset+self.MacOffset
        peak = int((Max-amp)*yscale)+yOffset
        self.canvas.create_line(x1,V,x1,peak, fill = sweepColor)

class ChildWindow():
    def __init__(self, master):
        master.title("Squid axon parameters")
        master.geometry("400x320+1000+100")
        self.NaPercent = 100
        self.Na_slider = Scale(master,from_=0, to=300, length=300,orient='horizontal', label='Sodium channel activation')
        self.Na_slider.set(100)
        self.Na_slider.pack()
        self.h_slider = Scale(master,from_=0, to=300, length=300,orient='horizontal', label='Sodium channel inactivation')
        self.h_slider.set(100)
        self.h_slider.pack()
        self.K_slider = Scale(master,from_=0, to=300, length=300,orient='horizontal', label= 'Potassium channel activation')
        self.K_slider.set(100)
        self.K_slider.pack()
        self.Hold_slider = Scale(master,from_=-100, to=100, length=300, orient='horizontal', label='Voltage clamp hold Vm',resolution=5)
        self.Hold_slider.set(-80)
        self.Hold_slider.pack()
        self.Step_slider = Scale(master,from_=-100, to=100, length=300,orient='horizontal', label='Voltage clamp step Vm',resolution=5)
        self.Step_slider.set(0)
        self.Step_slider.pack()  
    def updateSliders(self):
        global Na_Percent
        global K_Percent
        global h_Percent
        global HoldVm
        global StepVm

        Na_Percent = self.Na_slider.get()*.01
        h_Percent = self.h_slider.get()*.01
        K_Percent = self.K_slider.get()*.01
        HoldVm = self.Hold_slider.get()
        StepVm = self.Step_slider.get()

MW = Tk()
mainWin = Window(MW)
syn = Synapse.Synapse()
# TwoSynapses = []
# for i in range(0,2):
#     TwoSynapses.append(Synapse.Synapse())
# counter = 2
# # for syns in TwoSynapses:
# #     syns.DoSweep(2,3,.1,3)
# #     counter +=1
# #     mainWin.DrawSweep(syns.Vm,counter,-10,-80, white)
# for i in range(0,2):
#     TwoSynapses[i].DoSweep(2,3,.1,3)
#     counter +=1
#     mainWin.DrawSweep(TwoSynapses[i].Vm,counter,-10,-80, white)
##################################################################################   
def runSim():    ###### This runs your simulation
    random.seed()
    if mainWin.simToRun == 1:  # menu selection is "My Simulation"
        offset = 4 #6
        exp = 6 #50
        thr = .15
        peak = .35
        index = 4

        if index ==1:           # exponent sigmoidal
            argument1 = offset
            argument2 = exp
        elif index ==2:         # linear with a threshold
            argument1 = thr
            argument2 = peak
        elif index == 3:        # square root sigmoidal
            argument1 = 0.1
            argument2 = 3
        else:                   # linear
            argument1 = .5      # slope of release as a function of calcium
            argument2 = 0
        while keepgoing:
            # Run simulation and draw Vm, Calcium and Release Probability
            
            syn.DoSweep(0,index,argument1,argument2) 
            mainWin.DrawSweep(syn.Vm,4,-40,-80, white)
            #if i == 50:
            mainWin.DrawSweep(syn.CalciumEx,5,1,-.01, magenta)
            mainWin.DrawSweep(syn.ReleaseP_Ex,5,1,-.01, yellow)
            #mainWin.DrawSweep(syn.Docked,3,syn.maxDocked,0,white)
            # Draw release probability as a function of calcium

            release = syn.showRelease(index,argument1,argument2)
            mainWin.DrawSweep(release,3,1.1,0,yellow)
    ##############################################################################       
MW.mainloop()