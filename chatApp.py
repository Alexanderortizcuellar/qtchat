from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtNetwork import QAbstractSocket
from chat_ui import Ui_MainWindow
from message import Message
from client import Client
from connect import ConnectDialog
import sys
import typing

class Window(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.profile_pic = "profile.png"
        self.username = ""
        self.client = Client()
        self.timer = QtCore.QTimer()
        self.client.data.connect(self.receive_message)
        self.messages = []
        self.main_box = QtWidgets.QWidget()
        self.main_box_layout = QtWidgets.QVBoxLayout()
        self.main_box.setLayout(self.main_box_layout)
        self.setCentralWidget(self.main_box)
        self.box = QtWidgets.QWidget()
        self.scroll = QtWidgets.QScrollArea()
        self.main_layout = QtWidgets.QVBoxLayout()
        self.box.setLayout(self.main_layout)
        self.scroll.setWidget(self.box)
        self.scroll.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)  # pyright: ignore
        self.scroll.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)  # pyright: ignore
        self.scroll.setWidgetResizable(True)
        self.scroll.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.main_box_layout.addWidget(self.scroll)
        self.vscrollbar = self.scroll.verticalScrollBar()
        self.vscrollbar.rangeChanged.connect(self.scroll_to_bottom)
        self.vscrollbar.setSingleStep(20)
        # My gui stuff starts here
        self.action_Image.triggered.connect(self.set_image)
        self.action_Connect.triggered.connect(self.connect)
        self.input_box = QtWidgets.QTextEdit()
        self.input_box.setFixedHeight(50)
        self.input_box.setPlaceholderText("Enter your message here")
        self.input_box.setStyleSheet(
            "background-color: rgb(255, 255, 255);border-radius:8px;padding-left:10px;padding-top:10px;"
        )
        self.input_box.setFont(QtGui.QFont("Arial", 12))
        self.input_box.setTabChangesFocus(True)
        self.input_box.setGraphicsEffect(
            QtWidgets.QGraphicsDropShadowEffect(
                blurRadius=10,
                xOffset=0,
                yOffset=3,
                color=QtGui.QColor(0, 0, 0, 80),  # pyright: ignore
            )
        )
        self.input_box.setFont(QtGui.QFont("Arial", 12))
        self.send_button = QtWidgets.QPushButton("Send")
        self.send_button.setGraphicsEffect(
            QtWidgets.QGraphicsDropShadowEffect(
                blurRadius=10,
                xOffset=0,
                yOffset=3,
                color=QtGui.QColor(0, 0, 0, 80),  # pyright: ignore
            )
        )
        self.send_button.setCursor(QtCore.Qt.PointingHandCursor)
        self.send_button.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.send_button.setFont(QtGui.QFont("Arial", 12))
        self.send_button.clicked.connect(self.send_message)
        self.send_button.setShortcut("Ctrl+Return")
        self.hbox = QtWidgets.QHBoxLayout()
        self.hbox.addWidget(self.input_box)
        self.hbox.addWidget(self.send_button)
        self.main_box_layout.addLayout(self.hbox)
        self.btn = QtWidgets.QPushButton("Disconnect", self)
        self.btn.move(self.width() - 100, 100)
        user_value, ok = QtWidgets.QInputDialog.getText(self, "Chat", "Enter Your Username")
        while not ok:
            user_value, ok = QtWidgets.QInputDialog.getText(self, "Chat", "Enter Your Username")
        self.username = user_value



    @QtCore.pyqtSlot(int, int)
    def scroll_to_bottom(self, minmum, maximum):
        self.vscrollbar.setValue(maximum)

    @QtCore.pyqtSlot()
    def send_message(self):
        date = QtCore.QDateTime.currentDateTime().toString("hh:mm:ss")
        if self.client.state() == QAbstractSocket.ConnectedState:
            message = f"{self.username}:{self.input_box.toPlainText()}".encode()
            self.client.write(message)
            msg = Message(
                self.input_box.toPlainText(),
                author=self.username,
                date=date,
                profile_image=self.profile_pic,
            )
            self.main_layout.addWidget(msg)
            self.input_box.clear()
            self.animamate_message(msg.opacity_effect)
            self.timer.singleShot(1000, msg.set_shadow)
            
        else:
            QtWidgets.QMessageBox.warning(
                self, "Chat", "you are not connected to a chat room"
            )

    def handle_connection(self, **kwargs):
        if self.client.state() in [
            QAbstractSocket.ConnectedState,
            QAbstractSocket.HostLookupState,
            QAbstractSocket.ConnectingState,
        ]:
            return
        self.client.connect_to_server(kwargs["host"], kwargs["port"])
        self.statusBar().showMessage(f"Connected to {kwargs['host']}")

    def connect(self):
        self.connect_dlg = ConnectDialog(self)
        self.connect_dlg.show()

    def receive_message(self, msg_str):
        date = QtCore.QDateTime.currentDateTime().toString("hh:mm:ss")
        data_splited =  msg_str.split(":", 1)
        print(data_splited)
        author = data_splited[0]
        message = data_splited[1]
        msg = Message(
            message, author=author, date=date, profile_image="profile.png"
        )
        self.main_layout.addWidget(msg)

    def set_image(self):
        file, _ = QtWidgets.QFileDialog.getOpenFileName(
            self, "Open", None, "(PNG *.png)"
        )
        if file:
            print(file)
            self.setWindowIcon(QtGui.QIcon(file))
            self.profile_pic = file
    
    def animamate_message(self, widget):
        self.anim = QtCore.QPropertyAnimation(widget, b"opacity")
        self.anim.setDuration(1000)
        self.anim.setStartValue(0)
        self.anim.setEndValue(1)
        self.anim.start()

    def resizeEvent(self, a0: typing.Optional[QtGui.QResizeEvent]) -> None:
        self.btn.move(self.width() - 100, 100)
        return super().resizeEvent(a0)


app = QtWidgets.QApplication(sys.argv)
window = Window()
window.show()
app.exec()
