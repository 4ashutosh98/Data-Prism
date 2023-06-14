import pandas as pd
import books_semanticsearch as bk
import PySimpleGUI as sg
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


books_found_df = bk.search_similar_books('Testing')
books_found_df['Rating Count'] = books_found_df['Rating Count'].str.strip()
books_found_df['Rating Count'] = books_found_df['Rating Count'].str.replace(',', '')
books_found_df['Rating Count'] = books_found_df['Rating Count'].astype(int)
print(books_found_df)


def create_plot_bar():
    no_of_values = len(books_found_df)
    num_books = [i for i in range(1, no_of_values+1)]
    barplot = plt.bar(num_books, books_found_df['Rating Count'], color='Red')
    plt.title('Books vs Ratings for each book', fontsize=14)
    plt.xlabel('Books', fontsize=14)
    plt.ylabel('Rating of Books', fontsize=14)
    plt.bar_label(barplot, labels=books_found_df['Rating Count'], label_type="edge")
    plt.show()


create_plot_bar()

# layout = [
#     [sg.Text("Line Plot")],
#     [sg.Canvas(size=(1000, 1000), key='-CANVAS-')]
#     # [sg.Canvas(size=(1000, 1000), key='-CANVAS2-')]
# ]
#
#
# def draw_figure(canvas, figure):
#     figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
#     figure_canvas_agg.draw()
#     figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
#     return figure_canvas_agg
#
#
# window = sg.Window("PLOT", layout, finalize=True, element_justification='center')
# draw_figure(window['-CANVAS-'].TKCanvas, create_plot_bar(locations, num))
# # draw_figure(window['-CANVAS2-'].TKCanvas, create_plot_line(job_id, min_ex))
#
# while True:
#     event, values = window.read()
#     if event == sg.WIN_CLOSED:
#         break
#
#     window.close()
