import tkinter
from tkinter import ttk
from tkinter import messagebox

import pyperclip

import sv_ttk
from ttkthemes import ThemedTk

def rot_n(str, n):
    for ci in range(len(str)):
        c = str[ci]
        if ord(c) >= ord('a') and ord(c) <= ord('z'):
            nc = ord(c) + n
            if nc > ord('z'):
                nc -= 26
            str[ci] = chr(nc)
        elif ord(c) >= ord('A') and ord(c) <= ord('Z'):
            nc = ord(c) + n
            if nc > ord('Z'):
                nc -= 26
            str[ci] = chr(nc)
    
    return ''.join(str)

def updateTitle(titleLabel, rotValue):
    rotNum = int(rotValue.get())
    titleLabel.config(text=f'Rot{rotNum}!')

def doRotate(srcValue, outValue, rotValue):
    rotNum = int(rotValue.get())
    res = rot_n(list(srcValue.get()), rotNum)
    outValue.set(res)

def valueToClipboard(value):
    pyperclip.copy(value.get())

def main():
    #root = tkinter.Tk()
    root = ThemedTk(theme="ubuntu")
    
    root.geometry('460x320')
    root.minsize(400, 320)
    #root.iconbitmap('./app.ico')
    
    root.title('Sun Valley Flavor')

    # Background (to fixed color inconsistent when some themes are applied)
    background = ttk.Frame(root)
    background.place(relx=0, rely=0, relwidth=1, relheight=1)

    # Title Label
    titleLabel = ttk.Label(root, font=('Cascadia Code', 24), text='', width=8)
    titleLabel.place(relx=0.05, rely=0.05) # Upper-left corner

    # Frame for Input Entries
    inputFrame = ttk.Frame(root)
    #inputFrame.pack(side='top', expand='yes', anchor='center')
    inputFrame.place(relx=0.1, rely=0.3)
    # Source Entry
    srcLabel = ttk.Label(inputFrame, text='Source:', width=8)
    srcLabel.grid(row=0, rowspan=1, column=0, columnspan=1)
    srcValue = tkinter.StringVar(value='Text here...')
    srcInput = ttk.Entry(inputFrame, width=30, textvariable=srcValue)
    srcInput.grid(row=0, rowspan=1, column=1, columnspan=3)
    # Empty Line #1
    line1 = ttk.Label(inputFrame, text='')
    line1.grid(row=1, rowspan=1, column=0, columnspan=4)
    # Output Entry
    outLabel = ttk.Label(inputFrame, text='Output:', width=8)
    outLabel.grid(row=2, rowspan=1, column=0, columnspan=1)
    outValue = tkinter.StringVar(value='')
    outInput = ttk.Entry(inputFrame, width=30, textvariable=outValue)
    outInput.grid(row=2, rowspan=1, column=1, columnspan=3)
    # Empty Line #2
    line2 = ttk.Label(inputFrame, text='')
    line2.grid(row=3, rowspan=1, column=0, columnspan=4)

    # Auto-update Checkbox
    updValue = tkinter.BooleanVar(value=True)
    updCheck = ttk.Checkbutton(inputFrame, text='Auto-Update', width=12,
            onvalue=True, offvalue=False, variable=updValue)
    updCheck.grid(row=4, rowspan=1, column=0, columnspan=2)
    
    # Rotate Value Spinbox
    rotLabel = ttk.Label(inputFrame, text='Rotate By', width=9)
    rotLabel.grid(row=4, rowspan=1, column=2, columnspan=1)
    rotValue = tkinter.StringVar(value=13)
    rotInput = ttk.Spinbox(inputFrame, width=2, from_=1, to=25, textvariable=rotValue)
    rotInput.grid(row=4, rowspan=1, column=3, columnspan=1)
    
    # Rotate Button
    button = ttk.Button(root, width=20, text='Rotate!', command=lambda: doRotate(srcValue, outValue, rotValue))
    button.place(relx=0.25, rely=0.8, relwidth=0.3)
    # Copy Output Button
    button = ttk.Button(root, width=20, text='Copy Output', command=lambda: valueToClipboard(outValue))
    button.place(relx=0.6, rely=0.8, relwidth=0.3)

    # Register Value Callbacks
    rotValue.trace('w', callback=lambda *args: updateTitle(titleLabel, rotValue))
    rotValue.trace('w', callback=lambda *args: doRotate(srcValue, outValue, rotValue) if updValue.get() else None)
    srcValue.trace('w', callback=lambda *args: doRotate(srcValue, outValue, rotValue) if updValue.get() else None)

    # Initialize Title
    updateTitle(titleLabel, rotValue)

    # Initialize Output
    doRotate(srcValue, outValue, rotValue)

    # This is where the magic happens
    #sv_ttk.set_theme('light')

    root.mainloop()

if __name__ == '__main__':
    main()
