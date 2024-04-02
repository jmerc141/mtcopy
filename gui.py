

import tkinter as tk
from tkinter import ttk, filedialog
import os, mtcopy, settings

window = tk.Tk()
tFrame = ttk.Frame(window)
ulFrame = ttk.Frame(tFrame)
urFrame = ttk.Frame(tFrame)
bFrame  = ttk.Frame(window, relief='sunken')
pbs = []
srcTxt = tk.StringVar()
dstTxt = tk.StringVar()

srcTxt.set('C:\\Users\\mercantj\\Downloads\\S1000D Issue 5.0\\S1000D Issue 5.0 Data Dictionary')
dstTxt.set('C:\\Users\\mercantj\\Desktop\\sandbox\\py\\mtcopy\\to')

def threadSelect(x: int):
        settings.s['threads'] = x
        if x == 'Auto':
            # Set default amount of threads to half of total
            x = os.cpu_count()//2
            settings.s['threads'] = x

        # Remove any packed bars
        for p in pbs:
            p.pack_forget()

        # Add selected amount
        for i in range(0, x, 1):
            pbs.append(ttk.Progressbar(urFrame, orient='horizontal', mode='determinate'))
            pbs[i].pack(padx=10, fill='x', pady=5) #value

def getSourceDir():
    settings.s['src'] = os.path.abspath(filedialog.askdirectory())
    srcTxt.set(settings.s['src'])

def getDestDir():
    settings.s['dst'] = os.path.abspath(filedialog.askdirectory())
    dstTxt.set(settings.s['dst'])


def startCopy():
     # check source and dest paths
     s = srcTxt.get()
     d = dstTxt.get()
     if os.path.exists(s) and os.path.exists(d):
        mtcopy.main(src=s, dest=d, threads=settings.s['threads'])


def mainGui():
    window.geometry('600x400')
    window.title('mtCopy')
    
    # Upper left area
    srcBtn = ttk.Button(ulFrame, text='Source', command=getSourceDir)
    dstBtn = ttk.Button(ulFrame, text='Destination', command=getDestDir)
    srcEnt = ttk.Entry(ulFrame, width=40, textvariable=srcTxt)
    dstEnt = ttk.Entry(ulFrame, width=40, textvariable=dstTxt)
    startBtn = ttk.Button(ulFrame, text='Start', command=startCopy)

    srcBtn.grid( row=0, column=0, padx=10, pady=5)
    srcEnt.grid(row=1, column=0, padx=10, pady=5, sticky='ew')
    dstBtn.grid( row=2, column=0, padx=10, pady=5)
    dstEnt.grid(row=3, column=0, padx=10, pady=5, sticky='ew')
    startBtn.grid(row=4, column=0, padx=10, pady=5)

    # Upper right area
    sel = tk.StringVar()
    lb = ttk.Label(urFrame, text='Threads to use:')
    ops = ['Auto']
    ops.extend(list(range(1, os.cpu_count()+1, 1)))
    ops.insert(0, 'Auto')
    ddThreads = ttk.OptionMenu(urFrame, sel, *ops, command=threadSelect)

    lb.pack()
    ddThreads.pack()
    
    # Bottom area
    log = tk.Text(bFrame, width=50, height=50)

    log.pack(fill='both')

    ulFrame.grid(row=0, column=0, sticky='nesw')
    urFrame.grid(row=0, column=1, sticky='nesw')
    tFrame.grid(row=0, column=0, sticky='nesw')
    bFrame.grid(row=1, column=0, sticky='nsew', padx=10, pady=10)

    # Top
    urFrame.columnconfigure(0, weight=1)
    ulFrame.columnconfigure(0, weight=1)
    tFrame.columnconfigure(0, weight=1)
    tFrame.columnconfigure(1, weight=1)

    # Sticky resizing
    window.columnconfigure(0, weight=1)
    window.rowconfigure(1, weight=1)
    
    threadSelect('Auto')

    window.mainloop()