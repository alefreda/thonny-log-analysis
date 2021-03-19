from os.path import isfile
import dateutil.parser
import json

import random
import csv
import os
import shutil

import numpy as np
import pandas as pd

# Visualization
import missingno as msno
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px


import seaborn as sns # For mathematical calculations
import matplotlib.pyplot as plt  # For plotting graphs
from datetime import datetime    # To access datetime

'''
logs[0]["time"]   -> apertura
logs[-1]["time"]   -> chiusura


"sequence" "ShellCommand" "command_text" "%Run" -> Run
"sequence" "Save"  -> salvataggi

sequence" "<<Paste>>" "text_widget_class" "CodeViewText" -> paste

'''

# #data
# def printDate(logs):

#     print("Apertura: ", logs[0]["time"])
#     print("Chiusura: ", logs[-1]["time"])
#     #datetime
#     print(dateutil.parser.parse(logs[0]["time"]))

# #errori
# def printErrors(logs):

#     for i in range(len(logs)):
#         if "text" in logs[i]:
#             #check se la stringa error è nel valore corrispondente
#             if "Error" in logs[i]["text"]:
#                 print(logs[i]["text"],"at time: ", dateutil.parser.parse(logs[i]["time"]))
#             else:
#                 pass
#         else:
#             pass
# #testo incollato
# def printPastedText(logs):
#     for i in range(len(logs)):
#         if "sequence" in logs[i]:
#             #check se la stringa paste è nel valore corrispondente
#             if "<<Paste>>" in logs[i]["sequence"]:
#                 #il testo si trova in i-1 in "text"
#                 print(logs[i-1]["text"],"at time: ",dateutil.parser.parse(logs[i]["time"]))
#             else:
#                 pass
#         else:
#             pass
# #run
# def printRun(logs):
#     run = 0
#     for i in range(len(logs)):
#         if "command_text" in logs[i]:
#             #check se la stringa run è nel valore corrispondente
#             if "%Run" in logs[i]["command_text"]:
#                 run = logs[i]["command_text"]
#                 print(run, "at time:", dateutil.parser.parse(logs[i]["time"]))
#             else:
#                 pass
#         else:
#             pass
#     print("numero di run: ", len(run))


#fuction to check element in json
def in_json(element, key, value, exact=True):
    if key not in element:
        return False
    if exact:
        return element[key] == value
    else:
        return element[key].find(value) != -1

#Iterate through folders, then subfolders and file
#list not dataframe 
def dataFrame(dir, scores):                                                                                                  

    #df_thonny_logs = pd.DataFrame()
    lab_days = ['2020-03-19', '2020-03-23', '2020-03-26', '2020-03-30', '2020-04-06', '2020-04-16', '2020-04-27', '2020-04-30', '2020-05-07', '2020-05-11', '2020-05-14']
    subdirs = [x[0] for x in os.walk(dir)] 

    thonny_logs_list = []                                                             
    for subdir in subdirs:
                                                                                                    
        files = os.walk(subdir).__next__()[2]
        sortedFiles = sorted(files)
        #print(df_thonny_logs)
        
        for file in sortedFiles:
            f = open(os.path.join(subdir, file))
            logs = json.load(f)
            
            #df = pd.DataFrame(logs)
            
            #extract integers from the string of the substring
            stringSubdir = subdir
            student_ID = 0

            res = ''.join(filter(lambda i: i.isdigit(), stringSubdir)) 
            student_ID = res


            score = 'fail'
            for item2 in scores:
                if (student_ID == item2['student_ID']):
                    score = item2['score']
            
            list_logs = []

            for item in logs:

                #select lab days
                if any(ele[0:10] in item['time'] for ele in lab_days):

                    #add student id
                    item.update( {"student_ID":student_ID})
                    item.update({"score":score})
                    if in_json(item, "sequence", "TextInsert") and in_json(item, "text", "Error", False):
                        txt = item['text']
                        error_text_type = txt.split(":", 1)[0]
                        #check number of characters
                        if len(error_text_type) < 50:
                            #remove \n
                            if '\n' in error_text_type:
                                clean_error_text_type = error_text_type.replace('\n', '') 
                                item.update( {"error_type": clean_error_text_type})
                            else:
                                item.update( {"error_type": error_text_type})
                    list_logs.append(item)
                else:
                    logs.remove(item)

            thonny_logs_list.extend(list_logs)

            #df['Student ID'] = student_ID
            #print(df)
            #df_thonny_logs = df_thonny_logs.append(df, sort=False, ignore_index=True)

    df_thonny_logs = pd.DataFrame(thonny_logs_list)
    df_thonny_logs.to_csv('dataset_thonny_logs.csv', index=False)    
    return df_thonny_logs                                                                         
                                                                               

def scores():
    scores = []
    
    with open('id-log_voto.csv') as f:

        csv_reader = csv.reader(f, delimiter=';')
        line_count = 0
        
        for row in csv_reader:
            info = {}
            if line_count == 0:
                print(f'Column names are {", ".join(row)}')
                line_count += 1
            else:
                info['student_ID'] = row[0]
                if row[1] == '-':
                    info['score'] = 'fail'
                elif int(row[1]) >= 18 and int(row[1]) <= 26:
                    info['score'] = 'pass'
                elif int(row[1]) > 26:
                    info['score'] = 'excellent'

            scores.append(info)    
        del scores[0]
        return scores      

def main(): 
    dataFrame('logs/', scores())
    #df = pd.read_csv('dataset_thonny_logs.csv') 
    #errors
    #df2 = df[df['text'].str.contains("Error", na=False)]
    #df2.to_csv('errors.csv')  
    #print(df['time'].dtypes) 
                
if __name__ == "__main__":
    main()

