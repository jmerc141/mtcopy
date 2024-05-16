'''
WARNING this is much slower than regular tk and slower still than cli and quick
'''

import TKinterModernThemes as TKMT
from TKinterModernThemes.WidgetFrame import Widget
from tkinter import ttk, filedialog
import tkinter as tk
import settings, os, mtcopy, threading

# List of progressbars, static for use with mtcopy
pbs  = [0,]
# List of labels, static for use with mtcopy
lbls = [0,]
# List of labels that show percent next to progressbar
lpercent = [0,]
# Global Source Button definition
srcBtn = ''
# Global Destination Button definition
dstBtn = ''
# Global Start Button definition
stbtn = ''
# Global SpinBox definition
sbox = ''
# Global copy thread
t = ''

yn = ''

'''
    Sets the value of the indexed progressbar and the corresponding label
    i: index of pbs
    v: value to set progressbar to
'''
def setPb(i: int, v: float) -> None:
    pbs[i]['value'] = v
    lpercent[i].set(f'{round(v, 2):05}%')


'''
    Sets the value of the indexed label (filename)
    i: index of lbls
    t: text to set it to
'''
def setLbl(i: int, t: str):
    lbls[i].set(t)


'''
    Make a small pop-up window appear with a message and ok button
    msg: text of the popup window
'''
def popup(msg=''):
    win = tk.Toplevel()
    win.wm_title("Info")
    w = 250
    h = 100
    ws = win.winfo_screenwidth()
    hs = win.winfo_screenheight()
    x = (ws/2) - (w/2)
    y = (hs/2) - (h/2)
    win.geometry('%dx%d+%d+%d' % (w,h,x,y))
    fr = ttk.Frame(win, padding=10)
    fr.pack(fill='both', expand=True)
    l = ttk.Label(fr, text=msg)
    l.grid(row=0, column=0)

    b = ttk.Button(fr, text="Okay", command=win.destroy)
    b.grid(row=1, column=0)

    fr.columnconfigure(0, weight=1)
    fr.rowconfigure(0, weight=1)
    fr.rowconfigure(1, weight=1)



'''
    Make a small pop-up window appear with a message and ok button
    msg: text of the popup window
'''
def popupYN(msg=''):
    global choice
    win = tk.Toplevel()
    win.wm_title("Info")

    def retry():
        global choice
        win.destroy()
        choice = True
    
    def no():
        global choice
        win.destroy()
        choice = False

    w = 400
    h = 100
    ws = win.winfo_screenwidth()
    hs = win.winfo_screenheight()
    x = (ws/2) - (w/2)
    y = (hs/2) - (h/2)
    win.geometry('%dx%d+%d+%d' % (w,h,x,y))
    fr = ttk.Frame(win, padding=10)
    fr.pack(fill='both', expand=True)
    l = ttk.Label(fr, text=msg)
    l.grid(row=0, column=0, columnspan=2)

    y = ttk.Button(fr, text="Yes", command=retry)
    n = ttk.Button(fr, text='No', command=no)
    y.grid(row=1, column=0)
    n.grid(row=1, column=1)

    fr.columnconfigure(0, weight=1)
    fr.rowconfigure(0, weight=1)
    fr.rowconfigure(1, weight=1)

    return choice


'''
    Disable ui elements, usually during a copy
'''
def disableButtons():
    sbox.config(state='disabled')
    srcBtn.config(state='disabled')
    dstBtn.config(state='disabled')
    stbtn.config(state='disabled')


'''
    Enable ui elements, after copy is done
'''
def enableButtons():
    sbox.config(state='enabled')
    srcBtn.config(state='enabled')
    dstBtn.config(state='enabled')
    stbtn.config(state='enabled')


'''
    Main GUI class
'''
class App(TKMT.ThemedTKinterFrame):
    '''
        Initiate a seperate thread from the gui that starts the multi-threaded copy
    '''
    def startCopy(self):
        s = self.srcTxt.get()
        d = self.dstTxt.get()
        th = self.threadnum.get()

        if os.path.exists(s) and os.path.exists(d):
            if os.path.isdir(s) and os.path.isdir(d):
                ret = mtcopy.init(src=s, dest=d, safe=self.safe.get(), threads=settings.s['threads'])
                if ret > 0:
                    # Make a new thread otherwise gui main thread hangs during copy
                    t = threading.Thread(target=mtcopy.startCopy)
                    t.start()
                else:
                    popup(f'Need at least {len(mtcopy.srcFiles)} threads')
            else:
                popup('Paths must be folders')
        else:
            popup('Paths do not exist')


    '''
        Called when Enter is is pressed on Spinbox, x is event (not needed)
        Removes all subframes and loops to set the amount put into the spinbox
    '''
    def threadSelectR(self, x):
        settings.s['threads'] = self.threadnum.get()
        for _ in range(1, len(self.sbfs)):
            # Remove all subframes
            self.removeSubFrame()

        for p in range(0, self.threadnum.get()):
            # Offset by 1 to account for sbfs = [0,]
            self.calcGrid(p+1)


    '''
        Called on spinbox buttons, determines whether to add or remove a subframe
    '''
    def threadSelect(self):
        x = self.threadnum.get()

        # Set threads to default for system and call threadSelectR
        if x == 0:
            x = os.cpu_count()
            self.threadSelectR(x)
            return
        
        settings.s['threads'] = x

        if x < len(self.sbfs):
            self.removeSubFrame()
        else:
            self.calcGrid(x)
        
    '''
        Calculate where to place the subframe based on how many exist
        x: number of threads chosen
    '''
    def calcGrid(self, x):
        if x <= 8 and x > 0:
            self.addSubFrame(x, x, 0)
        elif x > 8 and x <= 16:
            self.addSubFrame(x, x-8, 1)
        elif x > 16 and x <= 24:
            self.addSubFrame(x, x-16, 2)
        elif x > 24 and x <= 32:
            self.addSubFrame(x, x-24, 3)

    '''
        Adds a subframe to bFrame
        x: number of threads
        r: row to place
        c: column to place
    '''
    def addSubFrame(self, x, r, c):
        #print(x, len(self.sbfs))
        self.bFrame.master.columnconfigure(c, weight=1)
        subf = ttk.Frame(self.bFrame.master, padding=0)
        
        lbls.append(tk.StringVar())
        lpercent.append(tk.StringVar())
        self.sbfs.append(subf)
        subf.columnconfigure(0, weight=1)

        pb = ttk.Progressbar(self.sbfs[x], mode='determinate')
        percent = ttk.Label(self.sbfs[x], text='100%', textvariable=lpercent[x])
        
        l = ttk.Label(self.sbfs[x], text='here', anchor='center', textvariable=lbls[x])
        
        pbs.append(pb)

        pb.grid(row=0, column=0, sticky='ew')
        percent.grid(row=0, column=1, sticky='ew', padx=5)
        l.grid(row=1, column=0, sticky='ew')
        subf.grid(row=r, column=c, padx=10, pady=10, sticky='ew')

    '''
        Removes the last subframe
    '''
    def removeSubFrame(self):
        self.sbfs[-1].grid_forget()
        lbls.pop()
        pbs.pop()
        self.sbfs.pop()

    '''
        Runs on closing the main window
        waits for copy thread to finish before exiting
    '''
    def onClose(self):
        if isinstance(t, threading.Thread):
            if t.isalive():
                print('joining thread')
                t.join()
        self.master.destroy()

    '''
        Opens a window to select a source folder
    '''
    def getSourceDir(self):
        f = filedialog.askdirectory()
        if f != '':
            settings.s['src'] = os.path.abspath(f)
            self.srcTxt.set(settings.s['src'])

    '''
        Opens a window to select a destination folder
    '''
    def getDestDir(self):
        f = filedialog.askdirectory()
        if f != '':
            settings.s['dst'] = os.path.abspath(f)
            self.dstTxt.set(settings.s['dst'])


    '''
        Initialize all GUI elements
    '''
    def __init__(self, theme, mode, usecommandlineargs=True, usethemeconfigfile=True):
        super().__init__("MtCopy", theme, mode, usecommandlineargs, usethemeconfigfile)

        self.master.protocol("WM_DELETE_WINDOW", self.onClose)
        
        global srcBtn
        global dstBtn
        global stbtn
        global sbox

        # 0th spot will be empty so subFrames match spinbox value
        self.sbfs = [0,]
        # Stringvar to hold source path
        self.srcTxt = tk.StringVar()
        # Stringvar to hold destination path
        self.dstTxt = tk.StringVar()
        # Intvar to hold number of threads chosen
        self.threadnum = tk.IntVar()
        self.threadnum.set(0)
        
        # Set the size of the main window
        self.root.geometry('800x600')

        # Main frame
        self.mainFrame = self.addFrame('main', row=0, col=0, sticky='new', padx=5, pady=5)
        # Strech Folder select frame
        self.mainFrame.master.columnconfigure(0, weight=1)

        self.tFrame = self.mainFrame.addLabelFrame('Folders', row=0, col=0, padx=5, pady=5)
        # Center entries and buttons
        self.tFrame.master.columnconfigure(0, weight=1)
        
        srcEnt = self.tFrame.Entry(self.srcTxt, row=0, col=0, pady=5, sticky='ew')
        srcBtn = self.tFrame.Button('Source', self.getSourceDir, row=0, col=1, pady=5, sticky='e')
        dstEnt = self.tFrame.Entry(self.dstTxt, row=1, col=0, sticky='ew')
        dstBtn = self.tFrame.Button('Destination', self.getDestDir, row=1, col=1, pady=5, sticky='e')
        
        # Thread select frame
        self.midFrame = self.mainFrame.addLabelFrame('Thread select', row=0, col=1, pady=5, padx=5)       
        
        sbox = self.midFrame.NumericalSpinbox(0, 32, 1, self.threadnum, row=0, col=0, sticky='n', colspan=2,
                                              widgetkwargs={'cursor': 'hand2', 'command': self.threadSelect})
        # Bind enter button to threadSelectR to clear and set amount of progressbars
        sbox.bind('<Return>', self.threadSelectR)

        stbtn = self.midFrame.AccentButton('Start', self.startCopy, row=1, col=0, pady=5, sticky='n')
        self.safe = tk.BooleanVar()
        safeBtn = self.midFrame.Checkbutton('Safe', self.safe, row=1, col=1)

        # Center spinbox and start button
        self.midFrame.master.columnconfigure(0, weight=1)

        # Bottom frame
        self.bFrame = self.mainFrame.addLabelFrame('Threads', row=1, col=0, colspan=2, pady=(5,10), padx=5, widgetkwargs={'height': 50})
        
        # Make only the bottom frame resizable, otherwise frames jump when adding a progressbar
        self.bFrame.makeResizable(True, True)
        self.makeResizable(False, False)
        
        #self.debugPrint()
        self.run(cleanresize=False)

