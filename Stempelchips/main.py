from functools import partial

import pyodbc
import traceback
import sys
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui


# initialisiere App
app = QApplication(sys.argv)
window = QWidget()
window.setWindowTitle("Stempelchip")
window.setFixedWidth(800)
window.setFixedHeight(480)
window.setStyleSheet("background: white;")
grid = QGridLayout()

widgets = {
           "header":[],
            "label1":[],
            "input1":[],
            "label2":[],
            "button1":[]
           }

class Db:
    DRIVER   =  r'DRIVER={SQL Server};'
    SERVER   =  r'SERVER=172.25.2.40\SQLEXPRESS;'
    DATABASE =  r'DATABASE=bcore;'
    USERNAME =  r'UID=bcommerp;'
    PASSWORD =  r'PWD=bcomm$01'

    def __init__(self):
        self.cnxn = pyodbc.connect(self.DRIVER + self.SERVER + self.DATABASE + self.USERNAME + self.PASSWORD)
        self.cursor = self.cnxn.cursor()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        print("__exit__")
        self.cursor.close()
        self.cnxn.close()

def headertext(text1):
    # OG Kaden Text
    logotext = QLabel(text1)
    logotext.setAlignment(QtCore.Qt.AlignCenter)
    logotext.setStyleSheet("text-align: right;" +
                           "font-size: 37px;" +
                           "vertical-align: top;" +
                           "margin-top: 10px;"

                           )

    logotext.setFocusPolicy(QtCore.Qt.NoFocus)
    return logotext
def create_button(name):
    button = QPushButton(name)
    button.setFixedWidth(250)
    button.setStyleSheet("*{font-size: 30px;" +
                         "font-weight: bold;" +
                         "margin: 8px 0;" +
                         "background-color: #0066CC;" +
                         "color: white;" +
                         "border: none;" +
                         "border-radius: 25px;" +
                         "padding: 12px 1px;}" +
                         "*:hover{background-color: #45a049}"

                         )
    return button

def clear_widgets():
    for widget in widgets:
        if widgets[widget] != []:
            widgets[widget][-1].hide()
        for i in range(0, len(widgets[widget])):
            widgets[widget].pop()

def startscreen():
    Stempelchip = None
    Name = None
    Status = None

    def infobox():
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)

        msg.setText("Stempelchip löschen?")
        # msg.setInformativeText("This is additional information")
        msg.setWindowTitle("Löschen bestätigen")
        # msg.setDetailedText("The details are as follows:")
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msg.buttonClicked.connect(msg.close)

        retval = msg.exec_()
        if retval == 16384:
            print ("Wird gelöscht")
            stempelidloeschen()
            clear_widgets()
            startscreen()



        msg.show()

    def stempelidloeschen():
        print("test")
        with Db() as d:
            print(input1.text())
            query = """
            SELECT person.[first_name] + ' ' + person.last_name as Name,
                                        perop.[empl_id],perop.[logincardno],perop.[jobid], 
                                        Case When perop.jobid = 'WEW-000010' then 'Ausgestempelt' 
                                        WHEN  perop.jobid = 'WEW-000009' then 'Eingestempelt' Else 
                                        perop.jobid End as Status FROM [bcommerp].[mdax_perop] as perop 
                                        left outer join [bcommerp].person_info_view as person 
                                        ON perop.person_id = person.person_id where perop.logincardno = '00000""" + input1.text() + "';"

            d.cursor.execute(query)
            d.cursor.commit()


    def stempelinfos():
        with Db() as d:
            print(input1.text())
            query = """
            SELECT person.[first_name] + ' ' + person.last_name as Name,
                                        perop.[empl_id],perop.[logincardno],perop.[jobid], 
                                        Case When perop.jobid = 'WEW-000010' then 'Ausgestempelt' 
                                        WHEN  perop.jobid = 'WEW-000009' then 'Eingestempelt' Else 
                                        perop.jobid End as Status FROM [bcommerp].[mdax_perop] as perop 
                                        left outer join [bcommerp].person_info_view as person 
                                        ON perop.person_id = person.person_id where perop.logincardno = '00000""" + input1.text() + "';"

            ergebnis = d.cursor.execute(query)
            if d.cursor.rowcount != 0:

                for row in ergebnis:
                    print(row)
                    Stempelchip = row[2]
                    Status = row[4]
                    text = row[0] + "\nPersonalnummer: "+row[1]+"\n Aktueller Status: "+row[4]
                    label2.setText(text)
                    button1 = create_button("Löschen")
                    button1.clicked.connect(infobox)
                    widgets["button1"].append(button1)
                    grid.addWidget(widgets["button1"][-1], 3, 0,1,3)


            else:
                label2.setText("Bitte Stempelnummer eingeben:\n zur aktuellen Nummer wurde kein Eintrag gefunden!")
                if widgets["button1"]:
                    widgets["button1"][-1].hide()
                    #widgets["button1"][-1].pop()

    # Erstelle Benutzer
    logotext = headertext("Stempelchip TMWE")

    label1 = QLabel()
    label1.setText("Chipnummer")

    label2 = QLabel()
    label2.setText("Bitte Stempelnummer eingeben:")
    label2.setAlignment(QtCore.Qt.AlignCenter)
    label2.setStyleSheet("text-align: right;" +
                           "font-size: 25px;" +
                           "vertical-align: top;"

                           )


    input1 = QLineEdit()
    input1.setFixedHeight(30)
    input1.setFocusPolicy(QtCore.Qt.TabFocus)
    input1.textChanged.connect(stempelinfos)





    widgets["header"].append(logotext)
    widgets["label1"].append(label1)
    widgets["input1"].append(input1)
    widgets["label2"].append(label2)



    grid.addWidget(widgets["header"][-1], 0, 0, 1, 3)
    grid.addWidget(widgets["label1"][-1], 2,0)
    grid.addWidget(widgets["input1"][-1],2,1)
    grid.addWidget(widgets["label2"][-1],1,0,1,3)








window.setLayout(grid)
#window.setWindowFlag(QtCore.Qt.FramelessWindowHint)
# window.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint)
window.setFocusPolicy(QtCore.Qt.StrongFocus)
window.show()
startscreen()
#stempelinfos("188")
sys.exit(app.exec())

#Beispiel
"""with Db() as d:
    ergebnis = d.cursor.execute('''Select * FROM mdax_conf
WHERE        (emplid = ' 3000045') ''')
    for row in ergebnis:
        print(row)"""