from PyQt5.QtCore import pyqtSignal
from PyQt5.QtNetwork import QTcpSocket, QHostAddress


class Client(QTcpSocket):
    data = pyqtSignal(str)

    def __init__(self, parent=None):
        super(Client, self).__init__(parent)

    def connect_to_server(self, host: str = QHostAddress.LocalHost, port: int = 8080):
        # print("here is a call")
        self.connectToHost(host, port)
        self.readyRead.connect(self.read_data)
        self.disconnected.connect(self.on_disconnect)
        self.error.connect(self.display_error)

    def read_data(self):
        while self.bytesAvailable() > 0:
            msg = self.readAll()
            try:
                self.data.emit(msg.data().decode())
            except Exception as e:
                print(e)

    def display_error(self, socket_error):
        print(socket_error)

    def on_disconnect(self):
        print("Disconnected from server")
