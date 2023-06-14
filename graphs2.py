#!/usr/bin/env python
from matplotlib.ticker import NullFormatter  # useful for `logit` scale
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import PySimpleGUI as sg
import matplotlib

matplotlib.use('TkAgg')

"""
Demonstrates one way of embedding Matplotlib figures into a PySimpleGUI window.
Basic steps are:
 * Create a Canvas Element
 * Layout form
 * Display form (NON BLOCKING)
 * Draw plots onto convas
 * Display form (BLOCKING)

 Based on information from: https://matplotlib.org/3.1.0/gallery/user_interfaces/embedding_in_tk_sgskip.html
 (Thank you Em-Bo & dirck)
"""

# ------------------------------- PASTE YOUR MATPLOTLIB CODE HERE -------------------------------

# Goal is to have your plot contained in the variable  "fig"

# Fixing random state for reproducibility
np.random.seed(19680801)

# make up some data in the interval ]0, 1[
y = np.random.normal(loc=0.5, scale=0.4, size=1000)
y = y[(y > 0) & (y < 1)]
y.sort()
x = np.arange(len(y))

# plot with various axes scales
plt.figure(1)

# linear
plt.subplot(221)
plt.plot(x, y)
plt.yscale('linear')
plt.title('linear')
plt.grid(True)

# log
plt.subplot(222)
plt.plot(x, y)
plt.yscale('log')
plt.title('log')
plt.grid(True)

# symmetric log
plt.subplot(223)
plt.plot(x, y - y.mean())
plt.yscale('symlog')#, linthreshy=0.01)
plt.title('symlog')
plt.grid(True)

# logit
plt.subplot(224)
plt.plot(x, y)
plt.yscale('logit')
plt.title('logit')
plt.grid(True)
plt.gca().yaxis.set_minor_formatter(NullFormatter())
plt.subplots_adjust(top=0.92, bottom=0.08, left=0.10, right=0.95, hspace=0.25,
                    wspace=0.35)
fig = plt.gcf()



# fig = matplotlib.figure.Figure(figsize=(5, 4), dpi=100)
# t = np.arange(0, 3, .01)
# fig.add_subplot(111).plot(t, 2 * np.sin(2 * np.pi * t))


# ------------------------------- END OF YOUR MATPLOTLIB CODE -------------------------------

# ------------------------------- Beginning of Matplotlib helper code -----------------------

def draw_figure(canvas, figure):
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
    return figure_canvas_agg


# ------------------------------- Beginning of GUI CODE -------------------------------

# define the window layout
layout0 = [[sg.Text('Welcome to Data PRISM\nYour handy tool to get information about Data Science related books, jobs and tutorials\nPress "Next" button to continue')],]

layout1 = [[sg.Text('Plot test')],
          [sg.Canvas(key='-CANVAS-')]]

layout = [[sg.Column(layout0, key='-COL0-'),
           sg.Column(layout1, visible=False, key='-COL1-')],
          [sg.Button('Next'), sg.Button('Return to Start'), sg.Button('Exit')]]

# create the form and show it without the plot
window = sg.Window('Demo Application - Embedding Matplotlib In PySimpleGUI', layout, finalize=True,
                   element_justification='center', font='Helvetica 18')



layoutvar=0
while True:
    event, values = window.read()
    print( event, " : ", values)
    if event in (None, 'Exit'):
        break
    if event == 'Next':
        print(layoutvar)
        layoutvar += 1
        window[f'-COL0-'].update(visible=False)
        window[f'-COL{layoutvar}-'].update(visible=True)
        # add the plot to the window
        fig_canvas_agg = draw_figure(window['-CANVAS-'].TKCanvas, fig)
    elif event == 'Return to Start':
         window[f'-COL{layoutvar}-'].update(visible=False)
         window[f'-COL0-'].update(visible=True)
         layoutvar = 0


window.close()