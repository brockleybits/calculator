# NAME: calculator.py
# VERSION: 6.0
# DATE: 23 Nov 2020
# BY: Todd Brotze
# DESCRIPTION: This program creates a rudimentary, interactive
#              calculator using TK Interface. NOTE: Cannot
#              process large integers or lengthy decimals!

import tkinter as tk
import re

# ~~~~~~~~~  WINDOW INITIALIZATION & GLOBAL VARIABLES  ~~~~~~~~~

window1 = tk.Tk()
window1.title('Calculator')
window1.columnconfigure(0, weight=1)
window1.rowconfigure(0, weight=1)

inputState = tk.StringVar()
ready2Calc = tk.BooleanVar()
memoryOn = tk.BooleanVar()
totalDigits = tk.IntVar()
newNum = tk.StringVar()
memNum = tk.StringVar()
arg1 = tk.StringVar()
operator = tk.StringVar()

inputState.set('INITIAL')
#               INITIAL - initial numerical entry
#               CONTINUE - continued numerical (or operator) entry
#               INITIAL_NON_CLEARED - initial numerical (or operator) entry following non-cleared result
ready2Calc.set(False)  # True: ready to complete calculation
memoryOn.set(False)  # True: single value stored in calculator's memory
totalDigits.set(9)  # Total number of digits to display in calculator (9 max)


# ~~~~~~~~~  CALLBACKS & FUNCTIONS  ~~~~~~~~~

# Takes keyboard input and sends to appropriate function
# RETURNs (none)
def key_press(event):
    key = event.char
    if key.isnumeric() or key == '.': updateDisplay(key)
    if key in ('+', '-', '*', '/', '='): performOp(key)
    if key in ('c', 'C'): clearDisplay()
    if key in ('m', 'M'): toggleMemory()
    if key in ('n', 'N'): changeNeg()
    return

# Highlights operator button on calculator when pressed
# RETURNs (none)
def enableOperator(b):
    if b == '+': plus.configure(state=tk.ACTIVE)
    if b == '-': minus.configure(state=tk.ACTIVE)
    if b == '*': multiply.configure(state=tk.ACTIVE)
    if b == '/': divide.configure(state=tk.ACTIVE)
    return

# Removes highlight from operator button when pressed
# RETURNs (none)
def disableOperator():
    plus.configure(state=tk.NORMAL)
    minus.configure(state=tk.NORMAL)
    multiply.configure(state=tk.NORMAL)
    divide.configure(state=tk.NORMAL)
    return

# Updates display with input from user if conditions are met
# RETURNs (none)
def updateDisplay(x):
    disableOperator()
    if inputState.get() == 'CONTINUE':
        if x == '.' and x in displayLabel['text']: return
        if len(displayLabel['text']) == int(totalDigits.get()): return
    if inputState.get() in ('INITIAL', 'INITIAL_NON_CLEARED'):
        if clear['text'] == 'AC': clear['text'] = 'C'
        if x == '.' and displayLabel['text'] == '-':
            displayLabel['text'] = '-0'
        elif x == '.':
            displayLabel['text'] = '0'
        elif displayLabel['text'] == '-':
            pass
        else:
            displayLabel['text'] = ''
    display = displayLabel['text'] + x
    displayLabel['text'] = display
    inputState.set('CONTINUE')
    return

# Toggles the negative (-) sign on and off depending on conditions
# RETURNs (none)
def changeNeg():
    if displayLabel['text'] == '-':
        displayLabel['text'] = '0'
        inputState.set('INITIAL')
        return
    if inputState.get() == 'CONTINUE' and '-' in displayLabel['text'] and not re.search('[^-0.]', displayLabel['text']):
        displayLabel['text'] = '0'
        inputState.set('INITIAL')
        return
    if inputState.get() == 'INITIAL':
        displayLabel['text'] = '-'
        return
    if inputState.get() == 'INITIAL_NON_CLEARED':
        if displayLabel['text'][0] == '-':
            display = displayLabel['text'][1:]
        else:
            display = '-' + displayLabel['text']
        inputState.set('CONTINUE')
    elif '-' in displayLabel['text']:
        display = displayLabel['text'][1:]
    else:
        display = '-' + displayLabel['text']
    displayLabel['text'] = display
    return

# Called by cleanEntry(). Eliminates unecessary leading zeros from input
# RETURNs cleaned number
def cleanZeros(x):
    if x[0] == '0': cleanZeros(x[1:])
    else: newNum.set(x)
    return newNum.get()

# Properly formats input prior to evaluating expression
# RETURNs properly formatted input
def cleanEntry(x):
    if x[-1] == '.': x = x[:-1]
    if not re.search('[^-0.]', x): return '0'
    elif re.search(r'^(-00)\d*\.\d+', x): return '-0' + cleanZeros(x[1:])
    elif re.search(r'^(00)\d*\.\d+', x): return '0' + cleanZeros(x[1:])
    elif re.search(r'^(-0)\d+', x): return '-' + cleanZeros(x[1:])
    elif re.search(r'^(0)\d+', x): return cleanZeros(x)
    else: return x

# Stores displayed value in memory, or retrieves value from memory
# RETURNs (none)
def toggleMemory():
    if memoryOn.get():
        displayLabel['text'] = memNum.get()
        memory['fg'] = 'black'
        memoryOn.set(False)
        disableOperator()
        inputState.set('CONTINUE')
        if clear['text'] == 'AC': clear['text'] = 'C'
    else:
        if inputState.get() == 'INITIAL': return
        memNum.set(cleanEntry(displayLabel['text']))
        print(f'{memNum.get()} in memory.')
        memory['fg'] = '#F38B06'
        memoryOn.set(True)
    return

# Clears calculator display (and memory if condition is met)
# RETURNs (none)
def clearDisplay():
    if clear['text'] == 'AC':
        toggleMemory()
        clear['text'] = 'C'
        print('MEMORY', end=' ')
    displayLabel['text'] = '0'
    inputState.set('INITIAL')
    ready2Calc.set(False)
    disableOperator()
    print('CLEARED')
    if memoryOn.get(): clear['text'] = 'AC'
    return

# Takes result from performOp() and cleans lengthy numbers
# RETURNs cleaned result
def testResult(r):
    print(f'Testing result: {r}')
    if 'e' in str(r) or (len(str(r)) > int(totalDigits.get()) and r - int(r) == 0):
        return '%.3e' % r
    elif r - int(r) == 0:
        return int(r)
    elif len(str(r)) > int(totalDigits.get()) and '.' in str(r):
        origRLen = len(str(r))
        decLen = len(str(r)[str(r).find('.') + 1:])
        roundLen = int(totalDigits.get()) - (origRLen - decLen)
        if roundLen >= 0:
            return round(r, roundLen)
        else:
            return '%.3e' % r
    else:
        return r

# Takes operator input from calculator and A) stores initial part of
# expression, or B) calculates the full expression
# RETURNs (none)
def performOp(o):
    if (o == '=' and not ready2Calc.get()) or inputState.get() == 'INITIAL': return
    enableOperator(o)
    if ready2Calc.get():
        arg2 = cleanEntry(displayLabel['text'])
        print(f'Calculating: {arg1.get()} {operator.get()} {arg2}')
        if not re.search('[^-0.]', arg2):
            displayLabel['text'] = 'div by zero'
            inputState.set('INITIAL')
            disableOperator()
            ready2Calc.set(False)
            return
        result = testResult(eval(arg1.get() + operator.get() + arg2))
        displayLabel['text'] = str(result)
        print(f'Result: {result}')
        if o == '=':
            inputState.set('INITIAL_NON_CLEARED')
            ready2Calc.set(False)
        else:
            operator.set(o)
            arg1.set(result)
            print(f'Preparing for operation: {result} {operator.get()} ...')
            inputState.set('INITIAL')
            ready2Calc.set(True)
    else:
        arg1.set(cleanEntry(displayLabel['text']))
        operator.set(o)
        print(f'Preparing for operation: {arg1.get()} {operator.get()} ...')
        inputState.set('INITIAL')
        ready2Calc.set(True)
    return


# ~~~~~~~~~  PROPERTIES & METHODS FOR WINDOW, FRAMES, LABEL AND BUTTONS  ~~~~~~~~~

window1.bind('<Key>', key_press)

mainFrame = tk.Frame(window1, bg='dark grey')

displayLabel = tk.Label(mainFrame, text='0', width=12, height=1, bg='#478AB8', fg='#71FAFC', relief='sunken', font=('Helvetica','36'), anchor='e')

buttonFrame = tk.Frame(mainFrame, width=270, height=46)

num1 = tk.Button(buttonFrame, text = '1', width=5, font=('Helvetica','22','bold'), command=lambda: updateDisplay('1'))
num2 = tk.Button(buttonFrame, text = '2', width=5, font=('Helvetica','22','bold'), command=lambda: updateDisplay('2'))
num3 = tk.Button(buttonFrame, text = '3', width=5, font=('Helvetica','22','bold'), command=lambda: updateDisplay('3'))
num4 = tk.Button(buttonFrame, text = '4', width=5, font=('Helvetica','22','bold'), command=lambda: updateDisplay('4'))
num5 = tk.Button(buttonFrame, text = '5', width=5, font=('Helvetica','22','bold'), command=lambda: updateDisplay('5'))
num6 = tk.Button(buttonFrame, text = '6', width=5, font=('Helvetica','22','bold'), command=lambda: updateDisplay('6'))
num7 = tk.Button(buttonFrame, text = '7', width=5, font=('Helvetica','22','bold'), command=lambda: updateDisplay('7'))
num8 = tk.Button(buttonFrame, text = '8', width=5, font=('Helvetica','22','bold'), command=lambda: updateDisplay('8'))
num9 = tk.Button(buttonFrame, text = '9', width=5, font=('Helvetica','22','bold'), command=lambda: updateDisplay('9'))
num0 = tk.Button(buttonFrame, text = '0', width=5, font=('Helvetica','22','bold'), command=lambda: updateDisplay('0'))
decimal = tk.Button(buttonFrame, text = '.', width=5, font=('Helvetica','22','bold'), command=lambda: updateDisplay('.'))
plus = tk.Button(buttonFrame, text = '+', width=5, font=('Helvetica','22','bold'), activeforeground='#F38B06', command=lambda: performOp('+'))
minus = tk.Button(buttonFrame, text = '-', width=5, font=('Helvetica','22','bold'), activeforeground='#F38B06', command=lambda: performOp('-'))
multiply = tk.Button(buttonFrame, text = '*', width=5, font=('Helvetica','22','bold'), activeforeground='#F38B06', command=lambda: performOp('*'))
divide = tk.Button(buttonFrame, text = '/', width=5, font=('Helvetica','22','bold'), activeforeground='#F38B06', command=lambda: performOp('/'))
equals = tk.Button(buttonFrame, text = '=', width=10, font=('Helvetica','22','bold'), command=lambda: performOp('='))
clear = tk.Button(buttonFrame, text = 'C', width=5, font=('Helvetica','22', 'bold'), command=lambda: clearDisplay())
memory = tk.Button(buttonFrame, text = 'M', width=5, font=('Helvetica','22', 'bold'), command=lambda: toggleMemory())
negative = tk.Button(buttonFrame, text = '±', width=5, font=('Helvetica','22', 'bold'), command=lambda: changeNeg())


# ~~~~~~~~~  CALCULATOR LAYOUT   ~~~~~~~~~

mainFrame.grid(row=0, column=0, rowspan=6, columnspan=4)
mainFrame['padx'] = '0'
mainFrame['pady'] = '0'

displayLabel.grid(row=0, column=0, columnspan=4)

buttonFrame.grid(row=1, column=0, rowspan=5, columnspan=4)

clear.grid(row=0, column=0)
memory.grid(row=0, column=1)
negative.grid(row=0, column=2)
plus.grid(row=0, column=3)
num7.grid(row=1, column=0)
num8.grid(row=1, column=1)
num9.grid(row=1, column=2)
minus.grid(row=1, column=3)
num4.grid(row=2, column=0)
num5.grid(row=2, column=1)
num6.grid(row=2,  column=2)
multiply.grid(row=2, column=3)
num1.grid(row=3, column=0)
num2.grid(row=3, column=1)
num3.grid(row=3, column=2)
divide.grid(row=3, column=3)
decimal.grid(row=4, column=0)
num0.grid(row=4, column=1)
equals.grid(row=4, column=2, columnspan=2, sticky='EW')


# ~~~~~~~~~  MAINLOOP()  ~~~~~~~~~

window1.mainloop()
