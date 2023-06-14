import PySimpleGUI as sg
import pandas as pd
import webbrowser


# This function extracts jobs with the particular search tag
def get_tag_values(tag):
    df = pd.read_csv("clean_data (1).csv")
    df

    neww = []
    for i in range(len(df)):
        df['Tags'][i] = df['Tags'][i].lower()
        if tag == None:
            break
        if tag.lower() in df['Tags'][i]:
            neww.append(df.iloc[i])

    a = pd.DataFrame(neww)
    return a

# Theme
sg.theme("Light Blue")

# ----------- Create the 3 layouts this Window will display -----------
layout0 = [[sg.Text('Welcome to Data PRISM\nYour handy tool to get information about Data Science related books, jobs and tutorials\nPress "Next" button to continue')],]

layout1 = [[sg.Text('Please enter the search term and select the entity you would like to search')],
           [sg.Text('Search: '), sg.Input(key='-SEARCH-')],
           [sg.Text('Entity:  '), sg.Combo(["Books","Tutorials","Jobs"],key='-ENTITY-')]]

layout2 = [[sg.Text('Layout 2')]]

layout3 = [[sg.Text('You have reached the end of Data PRISM\nWe hope you found this application helpful in your data science journey!!! \n\n\nPress the "Return to Start" button to go back to start page\nOr press the "Exit" button to exit the application.')]]

#Has predefined placements for each element. When an event happens, the values are updated.
layout4 =[
    [sg.Text('Enter your vote:', key='-SEARCHMESSAGE-')],
    [sg.Text('JOBS',justification='center', background_color='white', size=(76,1))],
    [sg.Text(key='error', background_color='white')],
    [sg.Text(key='Company_Name1', background_color='white'), sg.Button("Apply", key='job1', visible=False)],
    [sg.Text(key='Position1', background_color='white')],
    [sg.Text(key='Req1', background_color='white')],
    [sg.HSeparator(" ")],
    [sg.Text(key='Company_Name2', background_color='white'), sg.Button("Apply", key='job2', visible=False)],
    [sg.Text(key='Position2', background_color='white')],
    [sg.Text(key='Req2', background_color='white')],
    [sg.HSeparator(" ")],
    [sg.Text(key='Company_Name3', background_color='white'), sg.Button("Apply", key='job3', visible=False)],
    [sg.Text(key='Position3', background_color='white')],
    [sg.Text(key='Req3', background_color='white')],
    [sg.HSeparator(" ")],
    [sg.Text(key='Company_Name4', background_color='white'), sg.Button("Apply", key='job4', visible=False)],
    [sg.Text(key='Position4', background_color='white')],
    [sg.Text(key='Req4', background_color='white')],
    [sg.HSeparator(" ")],
    [sg.Text(key='Company_Name5', background_color='white'), sg.Button("Apply", key='job5', visible=False)],
    [sg.Text(key='Position5', background_color='white')],
    [sg.Text(key='Req5', background_color='white')],
    [sg.HSeparator(" ")],
    [sg.Text(key='Company_Name6', background_color='white'), sg.Button("Apply", key='job6', visible=False)],
    [sg.Text(key='Position6', background_color='white')],
    [sg.Text(key='Req6', background_color='white')],
    [sg.HSeparator(" ")],
    [sg.Text(key='Company_Name7', background_color='white'), sg.Button("Apply", key='job7', visible=False)],
    [sg.Text(key='Position7', background_color='white')],
    [sg.Text(key='Req7', background_color='white')],
    [sg.HSeparator(" ")],
    [sg.Text(key='Company_Name8', background_color='white'), sg.Button("Apply", key='job8', visible=False)],
    [sg.Text(key='Position8', background_color='white')],
    [sg.Text(key='Req8', background_color='white')],
    [sg.HSeparator(" ")],
    [sg.Text(key='Company_Name9', background_color='white'), sg.Button("Apply", key='job9', visible=False)],
    [sg.Text(key='Position9', background_color='white')],
    [sg.Text(key='Req9', background_color='white')],
    [sg.HSeparator(" ")],
    [sg.Text(key='Company_Name10', background_color='white'), sg.Button("Apply", key='job10', visible=False)],
    [sg.Text(key='Position10', background_color='white')],
    [sg.Text(key='Req10', background_color='white')]
]

# ----------- Create actual layout using Columns and a row of Buttons
layout = [[sg.Column(layout0, key='-COL0-'),
           sg.Column(layout1, visible=False, key='-COL1-'),
           sg.Column(layout2, visible=False, key='-COL2-'),
           sg.Column(layout3, visible=False, key='-COL3-'),
           sg.Column(layout4, visible=False, key='-COL4-')],
          [sg.Button('Next'), sg.Button('Return to Start'), sg.Button('Exit')]]

window = sg.Window('Data PRISM', layout)

layout = 0  # The currently visible layout
while True:
    event, values = window.read()
    print( event, " : ", values)

    #if the event happened is of nature job, example - job1
    #refer to "sg.Button("Apply", key='job1', visible=False)]" on col3
    if event[0:3]=='job':
        if len(subset_df)>10:
            for i in range(10):
                if event == 'job'+str(i+1):
                    webbrowser.open(subset_df['Link'][i])
        if len(subset_df)<10:
            for i in range(len(subset_df)):
                if event == 'job'+ str(i+1):
                    webbrowser.open(subset_df['Link'][i])

    if event in (None, 'Exit'):
        break
    if event == 'Next':
        print(layout)
        window[f'-COL{layout}-'].update(visible=False)
        if layout==0:
            pass
        if layout ==1:
            search = values['-SEARCH-']
            entity = values['-ENTITY-']
        if layout < 3:
            layout += 1
            window[f'-COL{layout}-'].update(visible=True)
        else:
            window[f'-COL3-'].update(visible=True)
            if entity=='Jobs':
                window[f'-COL4-'].update(visible=False)
            elif entity=='Books':
                pass
            else:
                pass
        if layout == 2:
            window['-SEARCHMESSAGE-'].update(f'Thanks for choosing to search "{search}" in "{entity}"')
            
            # If entity entered by the user is Jobs
            if entity == 'Jobs':
                window[f'-COL2-'].update(visible=False)
                window[f'-COL4-'].update(visible=True)
                subset_df = get_tag_values(search)
                subset_df.reset_index(inplace=True)
                print(subset_df)

                # if the window is closed
                if event == sg.WIN_CLOSED:
                    break

                # if x is not empty and the tag is not null
                if subset_df.empty == False and search != '':
                    if len(subset_df) > 10:
                        for i in range(10):
                            temp1 = 'Company_Name' + str(i + 1)
                            key = 'job' + str(i + 1)
                            window[temp1].Update(subset_df['Company'][i], background_color='Light Blue')
                            window[key].Update(visible=True)
                            temp2 = 'Position' + str(i + 1)
                            window[temp2].Update(subset_df['Job Title'][i])
                            temp3 = 'Req' + str(i + 1)
                            window[temp3].Update(subset_df['Requirements'][i])
                            window['error'].Update('')

                    # there are some tags, for which values are less than 5, try- "optimization" tag on GUI, to understand better
                    if len(subset_df) < 10:
                        for i in range(len(subset_df)):
                            temp1 = 'Company_Name' + str(i + 1)
                            key = 'job' + str(i + 1)
                            window[temp1].Update(subset_df['Company'][i], background_color='Light Blue')
                            window[key].Update(visible=True)
                            temp2 = 'Position' + str(i + 1)
                            window[temp2].Update(subset_df['Job Title'][i])
                            temp3 = 'Req' + str(i + 1)
                            window[temp3].Update(subset_df['Requirements'][i])
                            window['error'].Update('')
                        for i in range(len(subset_df), 10):
                            temp1 = 'Company_Name' + str(i + 1)
                            key = 'job' + str(i + 1)
                            window[temp1].Update('', background_color='white')
                            window[key].Update(visible=False)
                            temp2 = 'Position' + str(i + 1)
                            window[temp2].Update('', background_color='white')
                            temp3 = 'Req' + str(i + 1)
                            window[temp3].Update('', background_color='white')
                            window['error'].Update('', background_color='white')

                    # if the tag is not relevant, example, if the tag is "heyy"
                    if subset_df.empty == True:
                        window['error'].Update("No matches found")
                        for i in range(10):
                            temp1 = 'Company_Name' + str(i + 1)
                            key = 'job' + str(i + 1)
                            window[temp1].Update('', background_color='white')
                            window[key].Update(visible=False)
                            temp2 = 'Position' + str(i + 1)
                            window[temp2].Update('', background_color='white')
                            temp3 = 'Req' + str(i + 1)
                            window[temp3].Update('', background_color='white')

            layout=3


    elif event == 'Return to Start':
         window[f'-COL{layout}-'].update(visible=False)
         window[f'-COL0-'].update(visible=True)
         layout = 0
window.close()