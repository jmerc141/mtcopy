

import tkinter as tk
from tkinter import ttk, filedialog
import os, mtcopy, settings, threading, math

window = tk.Tk()
s = ttk.Style()
s.configure('new.TFrame', background='blue')
tFrame = ttk.Frame(window)
ulFrame = ttk.Frame(tFrame)
urFrame = ttk.Frame(tFrame)
midFrame = ttk.Frame(window)
bFrame  = tk.Frame(window)
sbfs = []
pbs = []
lbls = []
srcTxt = tk.StringVar()
dstTxt = tk.StringVar()
threadnum = tk.IntVar()
threadnum.set(0)

srcTxt.set('C:\\Users\\mercantj\\Downloads\\S1000D Issue 5.0\\S1000D Issue 5.0 Data Dictionary')
dstTxt.set('C:\\Users\\mercantj\\Desktop\\sandbox\\py\\mtcopy\\to')

# copying thread
t = ''

log = ''


def threadSelect():
        x = threadnum.get()
        if x == '':
            # auto
            return
        
        settings.s['threads'] = x
        if x == 'Auto':
            # Set default amount of threads to half of total
            x = os.cpu_count()
            settings.s['threads'] = x
        if x <= 6 and x > 0:
            adjPB(x, 0, x)
        elif x > 6 and x <= 12:
            adjPB(x, 1, x-6)
        elif x > 12 and x <= 18:
            adjPB(x, 2, x-12)
        elif x > 18 and x <= 24:
            adjPB(x, 3, x-18)
        elif x > 24 and x <= 30:
            adjPB(x, 4, x-24)
        elif x > 30 and x <= 32:
            adjPB(x, 5, x-30)


def adjPB(x, c, r):
    if x > len(sbfs):
        bFrame.columnconfigure(c, weight=1)
        bFrame.rowconfigure(r, weight=1)
        subFrame = tk.Frame(bFrame, padx=5, pady=0)
        lbls.append(tk.StringVar())
        sbfs.append(subFrame)
        pbs.append(ttk.Progressbar(sbfs[x-1], orient='horizontal', mode='determinate'))
        pbs[x-1].pack(fill='x')
        tk.Label(sbfs[x-1], text='here', textvariable=lbls[x-1], borderwidth=5).pack()
        sbfs[x-1].grid(row=r, column=c, sticky='ew')
    elif x < len(sbfs):
        sbfs[x].grid_forget()
        lbls.pop()
        pbs.pop()
        sbfs.pop()


def updatePb(idx, val):
    pbs[idx]['value'] = val


def writeLog(txt: str):
    log.config(state='normal')
    log.insert('end', txt)
    log.config(state='disabled')


def getSourceDir():
    settings.s['src'] = os.path.abspath(filedialog.askdirectory())
    srcTxt.set(settings.s['src'])


def getDestDir():
    settings.s['dst'] = os.path.abspath(filedialog.askdirectory())
    dstTxt.set(settings.s['dst'])


def startCopy():
    s = srcTxt.get()
    d = dstTxt.get()
    th = threadnum.get()

    if os.path.exists(s) and os.path.exists(d):
        if os.path.isdir(s) and os.path.isdir(d):
            ret = mtcopy.init(src=s, dest=d, threads=settings.s['threads'])
            print('ret:', ret)
            if ret > 0:
                # Make a new thread otherwise gui main thread hangs during copy
                t = threading.Thread(target=mtcopy.startCopy)
                t.start()
            else:
                writeLog(f'Need at least {len(mtcopy.srcFiles)} threads\n')
        else:
            writeLog('Paths must be folders')
    else:
        writeLog('Paths do not exist')

def onClose():
    if isinstance(t, threading.Thread):
        if t.isalive():
            t.join()
    window.destroy()


def incThread():
    n = threadnum.get() + 1
    threadnum.set(n)
    print(threadnum.get(), n)
    

def mainGui():
    window.geometry('700x500')
    window.resizable(False, False)
    window.title('mtCopy')
    window.protocol("WM_DELETE_WINDOW", onClose)
    
    # Upper left area
    srcBtn = ttk.Button(ulFrame, text='Source', command=getSourceDir)
    dstBtn = ttk.Button(ulFrame, text='Destination', command=getDestDir)
    srcEnt = ttk.Entry(ulFrame, width=40, textvariable=srcTxt)
    dstEnt = ttk.Entry(ulFrame, width=40, textvariable=dstTxt)
    startBtn = ttk.Button(ulFrame, text='Start', command=startCopy)
    
    srcEnt.grid(row=0, column=0, padx=10, pady=5, sticky='ew')
    srcBtn.grid(row=0, column=1, padx=10, pady=5)
    dstEnt.grid(row=1, column=0, padx=10, pady=5, sticky='ew')
    dstBtn.grid(row=1, column=1, padx=10, pady=5)
    startBtn.grid(row=2, column=0, padx=10, pady=5, sticky='s')

    # Bottom area
    lb = ttk.Label(midFrame, text=f'Threads to use: ')
    thSpinbox = ttk.Spinbox(midFrame, textvariable=threadnum, values=list(range(1, 33, 1)), increment=1, width=5, command=threadSelect)

    ttk.Separator(midFrame, orient='horizontal').pack(fill='x', side='top')
    lb.pack()
    thSpinbox.pack()
    
    # Upper right area
    global log
    log = tk.Text(urFrame, width=10, height=10, state='disabled', wrap='word')

    log.pack(fill='x', padx=5, pady=5)

    tFrame.pack(fill='x')
    ulFrame.grid(row=0, column=0, sticky='nesw')
    urFrame.grid(row=0, column=1, sticky='nesw',)
    midFrame.pack(fill='x')
    bFrame.pack(fill='both', expand=False, padx=5, pady=5)
    

    # Top
    urFrame.columnconfigure(0, weight=1)
    ulFrame.columnconfigure(0, weight=1)
    tFrame.columnconfigure(0, weight=1)
    tFrame.columnconfigure(1, weight=1)
    
    #bFrame.grid_columnconfigure(0, weight=1)

    # Sticky resizing
    window.columnconfigure(0, weight=1)
    window.rowconfigure(1, weight=1)

    window.mainloop()