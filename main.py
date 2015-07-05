__authors__ = 'Rismshah Sabir, Khalida Bibi, Adnan Niazi'

from PyQt4.QtGui import *
from PyQt4.QtCore import *
from my_gui import Ui_MainWindow

class MyMainGui(QMainWindow, Ui_MainWindow):

    def __init__(self, parent=None):
        super(MyMainGui, self).__init__(parent)
        self.setupUi(self)
        app.setStyle(QStyleFactory.create('Plastique'))

        self.pushButton.clicked.connect(self.generate_table)

        self.tableWidget.setColumnCount(3)
        self.tableWidget.setHorizontalHeaderLabels(['Course name', 'Grade', 'Credit hours'])

        self.rowcount = 1
        self.tableWidget.setRowCount(self.rowcount)

        self.tableWidget.itemChanged.connect(self.respond_to_changed_table_entries)
        self.columns_populated = 0

    def generate_table(self):
        """Populates the table with Subject name, credit hours, and the grades obtained."""

        self.subject_name = self.lineEdit_subject_name.text()
        self.grade= self.comboBox_grade.currentText()
        self.credit_hours = self.comboBox_credit_hours.currentText()

        if self.subject_name == '' or self.grade == 'Choose grade obtained' or self.credit_hours == 'Choose credit hours':
            return

        self.tableWidget.setItem(self.rowcount-1,0, QTableWidgetItem(self.subject_name))
        self.tableWidget.setItem(self.rowcount-1,1, QTableWidgetItem(self.grade))
        self.tableWidget.setItem(self.rowcount-1,2, QTableWidgetItem(self.credit_hours))
        self.rowcount += 1
        self.tableWidget.setRowCount(self.rowcount)
        self.calculate_gpa()

    def calculate_gpa(self):
        """Calculates GPA every time the table has a new entry."""

        self.denominator = 0
        self.numerator = 0

        for row in range(0, self.rowcount-1):

            self.ch= self.tableWidget.item(row, 2)
            self.credithours_from_table = int(self.ch.text())

            self.gft = self.tableWidget.item(row, 1)
            self.grade_from_table = self.gft.text()

            self._grade_to_gradePoint()

            self.denominator = self.denominator + self.credithours_from_table
            self.numerator = self.numerator + (self.credithours_from_table * self.grade_point_from_table)

        gpa = self.numerator/self.denominator
        gpa = "{0:.2f}".format(gpa)
        self.lineEdit_gpa_results.setText(str(gpa))

    def respond_to_changed_table_entries(self):
        """Update GPA if the user changes entries in the table. !3 is a check to
        avoid spurious updates of the table when the first row is not fully populated"""

        if self.columns_populated != 3:
            self.columns_populated += 1
        else:
            self.calculate_gpa()

    def _grade_to_gradePoint(self):
        """Maps letter grades to grade points."""

        if self.grade_from_table == 'A':
            self.grade_point_from_table = 4
        elif self.grade_from_table == 'A-':
            self.grade_point_from_table = 3.70
        elif self.grade_from_table == 'B+':
            self.grade_point_from_table = 3.33
        elif self.grade_from_table == 'B':
            self.grade_point_from_table = 3.00
        elif self.grade_from_table == 'B-':
            self.grade_point_from_table = 2.70
        elif self.grade_from_table == 'C+':
            self.grade_point_from_table = 2.30
        elif self.grade_from_table == 'C':
            self.grade_point_from_table = 2.00
        elif self.grade_from_table == 'C-':
            self.grade_point_from_table = 1.70
        elif self.grade_from_table == 'D+':
            self.grade_point_from_table = 1.20
        elif self.grade_from_table == 'D':
            self.grade_point_from_table = 1.00
        elif self.grade_from_table == 'D-':
            self.grade_point_from_table = 0.70
        else:
            self.grade_point_from_table = 0.0


if __name__ == "__main__":
    app = QApplication([])
    my_gui = MyMainGui()
    my_gui.show()
    app.exit(app.exec_())