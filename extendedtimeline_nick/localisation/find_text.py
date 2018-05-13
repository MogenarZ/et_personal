import os

for fil in [fil for fil in os.listdir(os.getcwd()) if ".yml" in fil]:
    with open(fil, "r", encoding="UTF-8") as text_fil:
        text_data = text_fil.read()
    if "Noric" in text_data:
        print(fil)
