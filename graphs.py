import PySimpleGUI as sg
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd

df = pd.read_csv('jobs_cleaned_data.csv')


def get_tag_values(tag):
    # df=pd.read_csv('jobs_cleaned_data.csv')

    neww = []
    for i in range(len(df)):
        df['Tags'][i] = df['Tags'][i].lower()
        if tag == None:
            break
        if tag.lower() in df['Tags'][i]:
            neww.append(df.iloc[i])

    a = pd.DataFrame(neww)
    return a


x = get_tag_values('Machine Learning')
x = x.drop(['Unnamed: 0'], axis=1)
x.reset_index(inplace=True)

y = x.head(10)

groups = y.groupby(['Location'])['Location'].count()
# z=groups.first()

locations = []
num = []
for i in groups.iteritems():
    locations.append(i[0])
    num.append(i[1])


def create_plot_bar(locations, number):
    plt.bar(locations, number, color='maroon', width=0.4)
    plt.title('Location vs number of jobs there', fontsize=14)
    plt.xlabel('Locations', fontsize=14)
    plt.ylabel('Number of Jobs', fontsize=14)
    return plt.gcf()


layout = [
    [sg.Text("Line Plot")],
    [sg.Canvas(size=(1000, 1000), key='-CANVAS-')]
    # [sg.Canvas(size=(1000, 1000), key='-CANVAS2-')]
]


def draw_figure(canvas, figure):
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
    return figure_canvas_agg


window = sg.Window("PLOT", layout, finalize=True, element_justification='center')
draw_figure(window['-CANVAS-'].TKCanvas, create_plot_bar(locations, num))
# draw_figure(window['-CANVAS2-'].TKCanvas, create_plot_line(job_id, min_ex))

while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED:
        break

    window.close()