import PySimpleGUI as sg
import pandas as pd
import webbrowser

# This function extracts jobs with the particular search tag
def get_tag_values(tag):
    df=pd.read_csv("clean_data (1).csv")
    df

    neww=[]
    for i in range(len(df)):
        df['Tags'][i]=df['Tags'][i].lower()
        if tag==None:
            break
        if tag.lower() in df['Tags'][i]:
            neww.append(df.iloc[i])
            
    a=pd.DataFrame(neww)
    return a
# Theme
sg.theme("Light Blue")


# Defining the columns for layout
col1=[[sg.Text('BOOKS', background_color='white', size=(76,1), justification='center')]]
col2=[[sg.Text('TUTORIALS', background_color='white', size=(76,1), justification='center')]]
#Has predefined placements for each element. When an event happens, the values are updated.
col3=[
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
    
# Decribes what will be shown on the screen
layout = [
    [sg.Text("DATA", font=("Times New Roman",25), text_color='black'), sg.Text("PRISM", font=("Times New Roman",25), text_color='blue')],
    [sg.HSeparator()],
    [sg.Text("Enter a field", size=(1470,1), justification='center', font=('Times New Roman', 15))],
    [sg.Text('', size=(95,1)),sg.InputText(key='-Tag-', do_not_clear=True, size=(40,1), background_color='white', justification='left'), sg.Submit()],
    [sg.Text("For Example: Machine Learning, Artificial Intelligence, Analysis", font=("Arial", 10), text_color='gray', size=(1470,1), justification='center')],
    [sg.Text("NOTE FOR USER: The website is using pre-loaded data to provide results, as scraping is a time consuming step. The data is updated every day to provide best value to our users.", text_color='red', font=('Times New Roman', 15))],
    [sg.Column(col1, element_justification='c' ), sg.Column(col2, element_justification='c'), sg.Column(col3, background_color='white')],
    
    ]
#size_screen=sg.Window.get_screen_size()

window = sg.Window('Data Prism', layout, size=(1470, 875))

#Event loop starts
while True:
    event, values= window.read()
    print( event, " : ", values)
    
    # get_tag_values is the function defined on top
    x=get_tag_values(values['-Tag-'])
    x.reset_index(inplace=True)
    #x=x.drop(['index','Unnamed: 0'], axis=1)
    
    #if the event happened is of nature job, example - job1 
    #refer to "sg.Button("Apply", key='job1', visible=False)]" on col3
    if event[0:3]=='job':
        if len(x)>10:
            for i in range(10):
                if event == 'job'+str(i+1):
                    webbrowser.open(x['Link'][i])
        if len(x)<10:
            for i in range(len(x)):
                if event == 'job'+ str(i+1):
                    webbrowser.open(x['Link'][i])
                
    #if the window is closed
    if event == sg.WIN_CLOSED:
        break
    
    #if x is not empty and the tag is not null
    
    if x.empty==False and values['-Tag-']!='':
        if len(x)>10:
            for i in range(10):
                temp1 = 'Company_Name'+ str(i+1)
                key='job'+str(i+1)
                window[temp1].Update(x['Company'][i], background_color='Light Blue')
                window[key].Update(visible=True)
                temp2  = 'Position' + str(i+1)
                window[temp2].Update(x['Job Title'][i])
                temp3 = 'Req' + str(i+1)
                window[temp3].Update(x['Requirements'][i])
                window['error'].Update('')
                
        #there are some tags, for which values are less than 5, try- "optimization" tag on GUI, to understand better
        if len(x)<10:
            for i in range(len(x)):
                temp1 = 'Company_Name'+ str(i+1)
                key='job'+str(i+1)
                window[temp1].Update(x['Company'][i], background_color='Light Blue')
                window[key].Update(visible=True)
                temp2  = 'Position' + str(i+1)
                window[temp2].Update(x['Job Title'][i])
                temp3 = 'Req' + str(i+1)
                window[temp3].Update(x['Requirements'][i])
                window['error'].Update('')
            for i in range(len(x), 10):
                temp1 = 'Company_Name'+ str(i+1)
                key='job'+str(i+1)
                window[temp1].Update('', background_color='white')
                window[key].Update(visible=False)
                temp2  = 'Position' + str(i+1)
                window[temp2].Update('', background_color='white')
                temp3 = 'Req' + str(i+1)
                window[temp3].Update('', background_color='white')
                window['error'].Update('', background_color='white')
                
    #if the tag is not relevant, example, if the tag is "heyy"        
    if x.empty==True:
        window['error'].Update("No matches found")
        for i in range(10):
            temp1 = 'Company_Name'+ str(i+1)
            key='job'+str(i+1)
            window[temp1].Update('', background_color='white')
            window[key].Update(visible=False)
            temp2  = 'Position' + str(i+1)
            window[temp2].Update('', background_color='white')
            temp3 = 'Req' + str(i+1)
            window[temp3].Update('', background_color='white')
            
    #window['job1'].Update(visible=True)
            

window.close()