import json

'''
data[0]["time"]   -> apertura
data[-1]["time"]   -> chiusura


"sequence" "ShellCommand" "command_text" "%Run" -> Run
"sequence" "Save"  -> salvataggi

sequence" "<<Paste>>" "text_widget_class" "CodeViewText" -> paste

'''


def main():

    try:
        f = open("logs/5/2020-04-16_14-10-53_0.txt")
        data = json.load(f) 
        f.close()

        print("Apertura: ", data[0]["time"])
        print("Chiusura: ", data[-1]["time"])


    except Exception:
        print('Errore nella lettura file')
    

    

    


if __name__ == "__main__":
    main()

