

import tkinter as tk
from tkinter import ttk, filedialog
import os, mtcopy, settings, threading

window = tk.Tk()
tFrame = ttk.Frame(window)
ulFrame = ttk.Frame(tFrame)
urFrame = ttk.Frame(tFrame)
bFrame  = ttk.Frame(window)
pbs = []
srcTxt = tk.StringVar()
dstTxt = tk.StringVar()

srcTxt.set('C:\\Users\\mercantj\\Downloads\\S1000D Issue 5.0\\S1000D Issue 5.0 Data Dictionary')
dstTxt.set('C:\\Users\\mercantj\\Desktop\\sandbox\\py\\mtcopy\\to')

# copying thread
t = ''

log = ''

def threadSelect(x: int):
        settings.s['threads'] = x
        if x == 'Auto':
            # Set default amount of threads to half of total
            x = os.cpu_count()//2
            settings.s['threads'] = x

        # Remove any packed bars
        for p in pbs:
            p['value'] = 0
            p.pack_forget()

        # Add selected amount
        for i in range(0, x):
            pbs.append(ttk.Progressbar(bFrame, orient='horizontal', mode='determinate'))
            pbs[i].pack(padx=10, fill='x', pady=5) #value


def updatePb(idx, val):
    print(idx, val)
    pbs[idx]['value'] = val

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
        mtcopy.init(src=s, dest=d, threads=settings.s['threads'])
        t = threading.Thread(target=mtcopy.startCopy)
        t.start()


def onClose():
    if isinstance(t, threading.Thread):
        print('here')
        t.close()
    window.destroy()


def mainGui():
    window.geometry('600x500')
    window.title('mtCopy')
    window.protocol("WM_DELETE_WINDOW", onClose)
    
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

    # Bottom area
    sel = tk.StringVar()
    lb = ttk.Label(bFrame, text='Threads to use:')
    ops = ['Auto']
    ops.extend(list(range(1, os.cpu_count()+1, 1)))
    ops.insert(0, 'Auto')
    ddThreads = ttk.OptionMenu(bFrame, sel, *ops, command=threadSelect)

    ttk.Separator(bFrame, orient='horizontal').pack(fill='x', side='top')
    lb.pack()
    ddThreads.pack()
    
    # Upper right area
    global log
    log = tk.Text(urFrame, width=10, height=10, state='disabled')

    log.pack(fill='x', padx=5, pady=5)

    tFrame.grid(row=0, column=0, sticky='new')
    ulFrame.grid(row=0, column=0, sticky='nesw')
    urFrame.grid(row=0, column=1, sticky='nesw')
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