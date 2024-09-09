from PyQt5 import QtWidgets, QtCore, QtGui
from connect_ui import Ui_Dialog


class ConnectDialog(QtWidgets.QDialog, Ui_Dialog):
    def __init__(self, parent):
        super().__init__()
        self.setupUi(self)
        self.parent = parent
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.close)

    @QtCore.pyqtSlot()
    def accept(self):
        print("calling accept")
        self.parent.handle_connection(
            host=self.host.currentText(), port=self.port.value()
        )
        self.close()
