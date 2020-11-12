import json
import pandas as pd
import dateutil.parser

'''
logs[0]["time"]   -> apertura
logs[-1]["time"]   -> chiusura


"sequence" "ShellCommand" "command_text" "%Run" -> Run
"sequence" "Save"  -> salvataggi

sequence" "<<Paste>>" "text_widget_class" "CodeViewText" -> paste

'''

#data
def printDate(logs):

    print("Apertura: ", logs[0]["time"])
    print("Chiusura: ", logs[-1]["time"])
    #datetime
    print(dateutil.parser.parse(logs[0]["time"]))

#errori
def printErrors(logs):

    for i in range(len(logs)):
        if "text" in logs[i]:
            #check se la stringa error è nel valore corrispondente
            if "Error" in logs[i]["text"]:
                print(logs[i]["text"],"at time: ", dateutil.parser.parse(logs[i]["time"]))
            else:
                pass
        else:
            pass
#testo incollato
def printPastedText(logs):
    for i in range(len(logs)):
        if "sequence" in logs[i]:
            #check se la stringa paste è nel valore corrispondente
            if "<<Paste>>" in logs[i]["sequence"]:
                #il testo si trova in i-1 in "text"
                print(logs[i-1]["text"],"at time: ",dateutil.parser.parse(logs[i]["time"]))
            else:
                pass
        else:
            pass
#run
def printRun(logs):
    run = 0
    for i in range(len(logs)):
        if "command_text" in logs[i]:
            #check se la stringa run è nel valore corrispondente
            if "%Run" in logs[i]["command_text"]:
                run = logs[i]["command_text"]
                print(run, "at time:", dateutil.parser.parse(logs[i]["time"]))
            else:
                pass
        else:
            pass
    print("numero di run: ", len(run))

def main():
    logs = 0
    try:
        f = open("logs/5/2020-04-16_14-10-53_0.txt")
        logs = json.load(f)
        f.close()
    except Exception:
        print('Errore nella lettura file: ', Exception)
    
    printDate(logs) 
    printErrors(logs)
    printPastedText(logs)
    printRun(logs)



if __name__ == "__main__":
    main()

