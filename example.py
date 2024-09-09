import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout

class Example(QWidget):
    def __init__(self):
        super().__init__()

        # Setting up the main window
        self.setGeometry(100, 100, 300, 200)
        self.setWindowTitle('Alert Message with Layout Example')

        # Main layout
        self.layout = QVBoxLayout(self)

        # Adding some main content (for example, buttons)
        self.main_button1 = QPushButton('Main Button 1', self)
        self.main_button2 = QPushButton('Main Button 2', self)
        
        # Add buttons to the layout
        self.layout.addWidget(self.main_button1)
        self.layout.addWidget(self.main_button2)

        # Creating the alert message label with absolute positioning
        self.alert_label = QLabel('This is an alert message!', self)
        self.alert_label.setStyleSheet("background-color: yellow; border: 1px solid black; padding: 5px;")
        self.alert_label.move(50, 30)  # Place the alert at (x=50, y=30)

        # A button to simulate closing the alert message
        self.close_button = QPushButton('Close Alert', self)
        self.close_button.move(50, 70)  # This button is also positioned absolutely
        self.close_button.clicked.connect(self.close_alert)

    def close_alert(self):
        # Hide the alert message
        self.alert_label.hide()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec_())
