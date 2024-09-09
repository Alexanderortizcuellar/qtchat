import datetime
from PyQt5 import QtWidgets, QtCore, QtGui
from message_ui import Ui_Form as MessageBase

class Message(QtWidgets.QWidget, MessageBase):
    def __init__(
        self,
        message: str,
        author: str,
        date: str,
        profile_image: str
    ):
        super().__init__()
        self.setupUi(self)
        # self.message_label.setMinimumHeight(40)
        self.message_label.setText(message)
        self.message_label.setScaledContents(True)
        self.message_label.setTextInteractionFlags(QtCore.Qt.TextSelectableByMouse) # pyright: ignore
        self.date_label.setText(date)
        self.profile_label.setPixmap(QtGui.QPixmap(profile_image))
        self.author_label.setText(author)
        #self.adjustSize()
        self.setFixedWidth(600)
        self.setMaximumWidth(600)
        self.setToolTip(author)
        self.opacity_effect = QtWidgets.QGraphicsOpacityEffect()
        self.setGraphicsEffect(self.opacity_effect)

    def set_shadow(self):
        self.shadow = QtWidgets.QGraphicsDropShadowEffect()
        self.shadow.setBlurRadius(10)
        self.shadow.setOffset(0, 4)
        self.shadow.setColor(QtGui.QColor(0, 0, 0, 80))
        self.setGraphicsEffect(self.shadow)

    def resizeEvent(self, a0: QtGui.QResizeEvent | None) -> None:
        # self.message_label.adjustSize()
        super().resizeEvent(a0)
