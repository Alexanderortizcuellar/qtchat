from PyQt5 import QtCore
from PyQt5.QtNetwork import QTcpServer, QTcpSocket, QHostAddress


class Server(QTcpServer):
    def __init__(self, parent=None):
        super(Server, self).__init__(parent)
        self.clients: list[QTcpSocket] = []

    def start(self):
        if not self.listen(QHostAddress("192.168.1.8"), 12345):
            print(self.errorString())
        else:
            print("Listening for connections...")

    def incomingConnection(self, socket_descriptor):
        socket = QTcpSocket()
        socket.setSocketDescriptor(socket_descriptor)
        print("Client connected")
        socket.readyRead.connect(self.read_data)
        socket.disconnected.connect(self.on_disconnect)
        self.clients.append(socket)
    
    def broadcast(self, msg, sender):
        for client in self.clients:
            if client.isOpen() and client != sender:
                client.write(msg)


    def read_data(self):
        for client in self.clients:
            if client.bytesAvailable() > 0:
                msg = client.readAll()
                try:
                    self.broadcast(msg, client)
                except Exception as e:
                    print(e)

    def on_disconnect(self):
        print("Client disconnected")
        client: QTcpSocket = self.sender()
        client.readyRead.disconnect()
        client.disconnected.disconnect()
        client.deleteLater()
        self.clients.remove(client)



app = QtCore.QCoreApplication([])
server = Server()
server.start()
app.exec()