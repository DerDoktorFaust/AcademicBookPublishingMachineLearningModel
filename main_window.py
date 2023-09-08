
# TERMINAL COMMAND TO CONVERT UI TO PY: python -m PyQt5.uic.pyuic -x [FILENAME].ui -o [FILENAME].py

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QObject, pyqtSlot
import createData
import matplotlib.pyplot as plt
from datetime import datetime
import numpy as np
from collections import Counter

class Ui_MainWindow(QObject):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(640, 480)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.disciplinebybooktablebutton = QtWidgets.QPushButton(self.centralwidget)
        self.disciplinebybooktablebutton.setGeometry(QtCore.QRect(160,70,341,32))
        self.disciplinebybooktablebutton.setObjectName("disciplinebybooktablebutton")
        self.disciplinebookcountbutton = QtWidgets.QPushButton(self.centralwidget)
        self.disciplinebookcountbutton.setGeometry(QtCore.QRect(160, 130, 341, 32))
        self.disciplinebookcountbutton.setObjectName("disciplinebookcountbutton")
        #self.topicbywordcountbutton = QtWidgets.QPushButton(self.centralwidget)
        #self.topicbywordcountbutton.setGeometry(QtCore.QRect(160, 200, 341, 32))
        #self.topicbywordcountbutton.setObjectName("topicbywordcountbutton")
        #self.booksbydisciplineperyear = QtWidgets.QPushButton(self.centralwidget)
        #self.booksbydisciplineperyear.setGeometry(QtCore.QRect(160, 270, 331, 32))
        #self.booksbydisciplineperyear.setObjectName("booksbydisciplineperyear")
        self.topdisciplinetrendlinebutton = QtWidgets.QPushButton(self.centralwidget)
        self.topdisciplinetrendlinebutton.setGeometry(160, 190, 341, 32)
        self.topdisciplinetrendlinebutton.setObjectName("topdisciplinetrendlinebutton")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 640, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.disciplinebookcountbutton.clicked.connect(self.disciplineBookCountClicked)
        self.disciplinebybooktablebutton.clicked.connect(self.disciplineByBookTableClicked)
        self.topdisciplinetrendlinebutton.clicked.connect(self.topDisciplineTrendLineClicked)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.disciplinebybooktablebutton.setText(_translate("MainWindow", "View Table of Top 20 Disciplines' Book Counts Total"))
        self.disciplinebookcountbutton.setText(_translate("MainWindow", "View Chart of Top 5 Disciplines' Book Counts"))
        #self.topicbywordcountbutton.setText(_translate("MainWindow", "View List of Topics and Word Counts"))
        #self.booksbydisciplineperyear.setText(_translate("MainWindow", "View Number of Books per Discipline by Year"))
        self.topdisciplinetrendlinebutton.setText(_translate("MainWindow", "View Top Discipline's Recommendation and Trendline"))

    @pyqtSlot()
    def disciplineBookCountClicked(self):

        #Log the user's action
        user_log = open("user_log.txt", 'a+')
        user_log.write("{} - User has viewed the 'Total Books by Discipline over 1996-2017' Chart\n".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        user_log.close()

        c = Counter(database.calculateBooksByDiscipline())  # take the top 10 most frequent words from the compiled dictionary

        sortedDictionary = dict(c.most_common(5)) #get the 5 largest disciplines
        disciplines = list(sortedDictionary.keys())
        counts = list(sortedDictionary.values())

        fig, ax = plt.subplots()
        ax.plot(disciplines, counts)
        ax.set(xlabel='Discipline', ylabel='Total Books', title='Total Books by Discipline over 1996-2017')
        plt.show()

    @pyqtSlot()
    def disciplineByBookTableClicked(self):

        #Log the user's action
        user_log = open("user_log.txt", 'a+')
        user_log.write("{} - User has viewed the 'Top 20 Disciplines' Number of Books Published from 1996-2017' table\n".format(
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        #user_log.write("User has viewed the 'Top 20 Disciplines' Number of Books Published from 1996-2017' table\n")
        user_log.close()

        totalbooks = database.calculateBooksByDiscipline()

        sorted_totalbooks = dict(sorted(totalbooks.items(), key=lambda x:x[1], reverse=True)) #sort the list

        data = [["Discipline", "Number of Books"]]

        for key in sorted_totalbooks: #table data must be in the form of lists in a list, so convert dictionary to this
            list = [key, sorted_totalbooks[key]]
            data.append(list)
            if len(data) == 20:
                break

        fig = plt.figure(dpi=80)
        ax = fig.add_subplot(1,1,1)
        table = ax.table(cellText=data, loc="upper center")
        ax.set_title("Top 20 Disciplines' Number of Books Published from 1996-2017")
        ax.axis('off')
        plt.show()

    @pyqtSlot()
    def topDisciplineTrendLineClicked(self):

        #Log the user's action
        user_log = open("user_log.txt", 'a+')
        user_log.write(
            "{} - User has viewed the 'Top Discipline's Trend Lines for Predictive Business Analysis' Chart\n".format(
                datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        #user_log.write("User has viewed the 'Top Discipline's Trend Lines for Predictive Business Analysis' Chart\n")
        user_log.close()

        totalbooks = database.calculateBooksByDiscipline()
        sorted_totalbooks = dict(sorted(totalbooks.items(), key=lambda x: x[1], reverse=True))  # sort the list

        data = []

        for key in sorted_totalbooks: #table data must be in the form of lists in a list, so convert dictionary to this
            list = [key, sorted_totalbooks[key]]
            data.append(list)

        top_discipline = data[0] #get the top discipline

        list_of_years = database.findUniqueYears() #find which years are present in the data sample

        data_for_each_year = []
        for element in list_of_years:
            data_for_each_year.append([element,0]) #this is what we will use to count each instance

        for key in database.bookMetaData:
            for x in range(len(data_for_each_year)):
                if (data_for_each_year[x][0] == database.bookMetaData[key][3]):
                    for discipline in database.bookMetaData[key][4]: #this is a list, check each item
                        if top_discipline[0] == discipline:
                            data_for_each_year[x][1] = data_for_each_year[x][1] + 1

        #### Now we plot a scatter plot and draw a best fit line
        x = []
        y = []
        for o in range(len(data_for_each_year)-1):
            x.append(data_for_each_year[o][0])
            y.append(data_for_each_year[o][1])

        plt.figure(figsize=(15, 6))
        plt.plot(x,y,'o')
        z=np.polyfit(x,y,1)
        p=np.poly1d(z)

        ext_x = np.linspace(1996, 2024) ##now we will extend the trend line to predict the future
        ext_y = p(ext_x)

        plt.plot(x,p(x),"r--", ext_x, ext_y)

        ### Now we want to take only the last seven years and make another best fit line
        ### The reason is, there may have been a lot of publications in early years
        ### and a few in recent years, making the slope positive when there is, at the
        ### least, a short term decrease.

        x2 = x[-7:]
        y2 = y[-7:]
        plt.plot(x2,y2,'o')
        z2=np.polyfit(x2,y2,1)
        p2=np.poly1d(z2)

        ext_x2 = np.linspace(min(x2), 2024)  ##now we will extend the trend line to predict the future
        ext_y2 = p(ext_x2)

        plt.plot(x2, p2(x2), "r--", ext_x2, ext_y2)
        #plt.plot(x2,p2(x2),"r--")


        plt.title("{}'s Trend Lines for Predictive Business Analysis".format(top_discipline[0]))
        plt.xlabel("Year")
        plt.ylabel("Number of Books Published")
        plt.xticks(range(1996, 2024))

        if z[0] >=0:
            plt.text(2015, 3, 'Long term trends: Publish in this discipline', style='italic', bbox={'facecolor': 'green', 'alpha': 0.5, 'pad': 10})
        if z[0] < 0:
            plt.text(2015, 3, 'Long term trends: Do not publish in this discipline', style='italic',
                     bbox={'facecolor': 'red', 'alpha': 0.5, 'pad': 10})

        if z2[0] >= 0:
            plt.text(2015, 0, 'Short term trends: Publish in this discipline', style='italic',
                     bbox={'facecolor': 'green', 'alpha': 0.5, 'pad': 10})
        if z2[0] <0:
            plt.text(2015, 0, 'Short term trends: Do not publish in this discipline', style='italic',
                     bbox={'facecolor': 'red', 'alpha': 0.5, 'pad': 10})

        plt.show()



if __name__ == "__main__":

    database = createData.BookDatabase()
    database.main_func() #set up the database

    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
