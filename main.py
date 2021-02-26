import json
import pandas as pd

import os
import shutil

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


#Iterate through folders, then subfolders and file
#list not dataframe 
def dataFrame(dir):                                                                                                  

    #df_thonny_logs = pd.DataFrame()

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
            
            for item in logs:
                item.update( {"Student ID":student_ID})
            
            thonny_logs_list.extend(logs)

            #df['Student ID'] = student_ID
            #print(df)
            #df_thonny_logs = df_thonny_logs.append(df, sort=False, ignore_index=True)

    df_thonny_logs = pd.DataFrame(thonny_logs_list)
    df_thonny_logs.to_csv('dataset_thonny_logs.csv')    
    return df_thonny_logs                                                                         
                                                                               


def main():
    dataFrame('logs/')



                


if __name__ == "__main__":
    main()

