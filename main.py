import pandas as pd
import cv2
from PIL import Image
import pytesseract

img = cv2.imread("prescription4.jpg")
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
text = pytesseract.image_to_string(img)

file = open("sample.txt","a")
file.write
file.close
file = open("sample.txt","r")
data = file.readlines()
#data = data.split("\n")
med = []
for i in range(len(data)):
    if(data[i].startswith("Dr.")):
        doctors_name = data[i]
    if(data[i].startswith("Patient Name")):
        loc = data[i].find(":")
        pateint_name = data[i][loc+2:]
    if(data[i].startswith("Rx")):
        med.append(data[i][3:])
        i = i+1
        while(data[i].startswith("Sign")!=True):
            med.append(data[i])
            i = i+1
    if(data[i].startswith("Date")):
        date = data[i][6:]
#print("Doctors Name = "+doctors_name)
print("Patient's Name = "+pateint_name)
#print("Medicines")
medicine_name = []
for i in range(len(med)):
    m = med[i][:-1]
    
    if len(m)>0:
        #print(m)
        medicine_name.append([med[i][:-1]])
#print("Date: "+date)
med_list = []
dosage =[]
for med in medicine_name:
    med_list.append(med[0][:-6])
    dosage.append(med[0][-5:])
#print(med_list)
#print(dosage)
dosages = []
for i in range(len(dosage)):
    tot = 0
    for j in range(5):
        if dosage[i][j] == '-':
            continue
        else:
            tot = tot+int(dosage[i][j])
    dosages.append(tot)
med_dict = {med_list[i]: dosages[i] for i in range(len(med_list))}
print(med_dict)
#print_bill(pateint_name,med_dict)


def to_nodemcu(med_list):
    toreturn = []
    df = pd.read_csv("Medicine.csv")
    lst = list(df["Name"])
    df.set_index(keys= "Name",inplace =True)
    for i in med_list.keys():
        if i in lst:
            toreturn.append(df.loc[i][0])

    return toreturn
        
res = to_nodemcu(med_dict)
print(res)


import flask

app = flask.Flask(__name__)
app.config["DEBUG"] = True


@app.route('/', methods=['GET','POST'])
def home():
    return str(res)

@app.route('/med_list', methods=['GET','POST'])
def med_list():
    return str(list(med_dict.keys()))

app.run()

