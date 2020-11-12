import json
import pandas as pd
import dateutil.parser

'''
data[0]["time"]   -> apertura
data[-1]["time"]   -> chiusura


"sequence" "ShellCommand" "command_text" "%Run" -> Run
"sequence" "Save"  -> salvataggi

sequence" "<<Paste>>" "text_widget_class" "CodeViewText" -> paste

'''


def printDate(data):
    print("Apertura: ", data[0]["time"])
    print("Chiusura: ", data[-1]["time"])
    #datetime
    print(dateutil.parser.parse(data[0]["time"]))
 


def main():

    try:
        f = open("logs/5/2020-04-16_14-10-53_0.txt")
        data = json.load(f)
        f.close()
    except Exception:
        print('Errore nella lettura file: ', Exception)
    
    printDate(data) 
    


if __name__ == "__main__":
    main()

