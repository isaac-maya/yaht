from PyQt5 import QtWidgets, QtGui, QtCore

class HabitTracker(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(HabitTracker, self).__init__(parent)
        self.days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        self.habits = {}

        self.table = QtWidgets.QTableWidget(0, len(self.days) + 1)
        self.table.setHorizontalHeaderLabels(['Habits'] + self.days)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.verticalHeader().setVisible(False)
        self.table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectItems)
        self.table.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.table.setFocus()
        self.table.cellClicked.connect(self.toggle_completion_status)

        self.addButton = QtWidgets.QPushButton("Add Habit")
        self.addButton.clicked.connect(self.add_habit)

        self.deleteButton = QtWidgets.QPushButton("Delete Habit")
        self.deleteButton.clicked.connect(self.delete_habit)

        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.table)
        layout.addWidget(self.addButton)
        layout.addWidget(self.deleteButton)

    def add_habit(self):
        habit, ok = QtWidgets.QInputDialog.getText(self, 'Input Dialog', 'Enter new habit:')
        if ok and habit:
            self.habits[habit] = [False] * len(self.days)
            self.refresh_table()

    def delete_habit(self):
        if self.table.currentRow() >= 0:
            habit = self.table.item(self.table.currentRow(), 0).text()
            del self.habits[habit]
            self.refresh_table()

    def refresh_table(self):
        self.table.setRowCount(len(self.habits))
        for row, (habit, days) in enumerate(self.habits.items()):
            self.table.setItem(row, 0, QtWidgets.QTableWidgetItem(habit))
            for column, done in enumerate(days, start=1):
                item = QtWidgets.QTableWidgetItem('X' if done else '')
                item.setTextAlignment(QtCore.Qt.AlignCenter)
                self.table.setItem(row, column, item)

    def keyPressEvent(self, event):
        super(HabitTracker, self).keyPressEvent(event)
        if event.key() == QtCore.Qt.Key_Space and self.table.currentRow() >= 0:
            self.toggle_completion_status()

    def toggle_completion_status(self, row=None, column=None):
        if row is None or column is None:
            row = self.table.currentRow()
            column = self.table.currentColumn()
        if row >= 0 and column > 0:
            habit = self.table.item(row, 0).text()
            self.habits[habit][column - 1] = not self.habits[habit][column - 1]
            self.refresh_table()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = HabitTracker()
    window.show()
    sys.exit(app.exec_())
