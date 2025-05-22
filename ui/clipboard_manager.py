from PyQt5 import QtCore, QtGui, QtWidgets
from utils.clippad_text_resize import ElidedLabel 
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        # MainWindow.resize(476, 551)
        MainWindow.setFixedSize(QtCore.QSize(476, 551))
        self.icon_path = "assets/recycle.png"  # Path to your icon file
        MainWindow.setStyleSheet("background-color: rgb(26, 26, 26);")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.header_name = QtWidgets.QLabel(self.centralwidget)
        self.header_name.setGeometry(QtCore.QRect(10, 10, 141, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.header_name.setFont(font)
        self.header_name.setStyleSheet("color: rgb(248, 248, 248);")
        self.header_name.setObjectName("header_name")


        self.restore_button = QtWidgets.QPushButton(self.centralwidget)
        self.restore_button.setGeometry(QtCore.QRect(230, 12, 40, 40))  # Positioned before history_button
        self.restore_button.setIcon(QIcon(self.icon_path))  # Make sure your icon is already white
        self.restore_button.setIconSize(QtCore.QSize(40, 40))
        self.restore_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.restore_button.setStyleSheet("""
        QPushButton {
                background-color: transparent;
        }
        """)
        self.restore_button.setText("")  # No text
        self.restore_button.setObjectName("restore_button")

        self.clearall_button = QtWidgets.QPushButton(self.centralwidget)
        self.clearall_button.setGeometry(QtCore.QRect(380, 10, 91, 41))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.clearall_button.setFont(font)
        self.clearall_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.clearall_button.setStyleSheet("""
                QPushButton {
                        color: rgb(248, 248, 248);
                        background-color: rgb(41, 41, 41);
                        border: 0.6px solid rgb(231, 231, 231);
                        border-radius: 8px;
                }
                QPushButton:hover {
                        border: 1px solid white;
                        background-color: rgb(60, 60, 60);  /* optional: slightly lighter */
                }
                QPushButton:pressed {
                        background-color: rgb(30, 30, 30);  /* darker shade on press */
                        padding-left: 1px;
                        padding-top: 1px;
                }
                """)

        self.clearall_button.setObjectName("clearall_button")
        self.history_button = QtWidgets.QPushButton(self.centralwidget)
        self.history_button.setGeometry(QtCore.QRect(280, 10, 91, 41))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.history_button.setFont(font)
        self.history_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.history_button.setStyleSheet(
            """
                QPushButton {
                        color: rgb(248, 248, 248);
                        background-color: rgb(41, 41, 41);
                        border: 0.6px solid rgb(231, 231, 231);
                        border-radius: 8px;
                }
                QPushButton:hover {
                        border: 1px solid white;
                        background-color: rgb(60, 60, 60);  /* optional: slightly lighter */
                }
                QPushButton:pressed {
                        background-color: rgb(30, 30, 30);  /* darker shade on press */
                        padding-left: 1px;
                        padding-top: 1px;
                }
                """
        )
        self.history_button.setObjectName("history_button")

        self.line_seperator = QtWidgets.QFrame(self.centralwidget)
        self.line_seperator.setGeometry(QtCore.QRect(10, 65, 451 , 1))  # Moves it 15px lower, makes it thinner
        self.line_seperator.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_seperator.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_seperator.setObjectName("line_seperator")
        self.line_seperator.setStyleSheet("background-color: rgb(161, 160, 160); max-height: 1px;")

        # Scroll Area for Dynamic Labels
        self.scroll_area = QtWidgets.QScrollArea(self.centralwidget)
        self.scroll_area.setGeometry(QtCore.QRect(10, 80, 461, 450))  # Increased height
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setStyleSheet("""
        QScrollArea {
                border: none;
                background-color: rgb(26, 26, 26);
        }
        """)
        self.scroll_area.setObjectName("scroll_area")

        # ✅ Apply style directly to the vertical scroll bar
        self.scroll_area.verticalScrollBar().setStyleSheet("""
        QScrollBar:vertical {
                background-color: rgb(41, 41, 41);
                width: 12px;
                border-radius: 6px;
                margin: 0px 0px 0px 0px;
                padding: 2px;
        }
        QScrollBar::handle:vertical {
                background-color: rgb(75, 75, 75);
                border-radius: 6px;
                min-height: 20px;
        }
        QScrollBar::handle:vertical:hover {
                background-color: rgb(100, 100, 100);
        }
        QScrollBar::add-line:vertical,
        QScrollBar::sub-line:vertical {
                background: none;
                border: none;
                height: 0px;
        }
        """)


        # Content Widget inside Scroll Area
        self.content_widget = QtWidgets.QWidget()
        self.content_widget.setStyleSheet("background-color: rgb(26, 26, 26);")
        
        # Changed from AlignCenter to AlignTop for proper alignment
        self.content_layout = QtWidgets.QVBoxLayout(self.content_widget)
        self.content_layout.setAlignment(QtCore.Qt.AlignTop)  # Changed from AlignCenter
        self.content_layout.setSpacing(8)
        self.content_layout.setContentsMargins(5, 5, 5, 5)

        # Add vertical spacer above and below to center the label
        spacer_top = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        spacer_bottom = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)

        

        # Placeholder Label
        self.placeholder_label = QtWidgets.QLabel("Nothing Here\nYou'll see your clipboard history once you copied something..", self.content_widget)
        self.placeholder_label.setAlignment(QtCore.Qt.AlignCenter)
        self.placeholder_label.setWordWrap(True)
        self.placeholder_label.setObjectName("placeholder_label")
        self.placeholder_label.setStyleSheet(
                """
                QLabel {
                        font: 11pt "MS Shell Dlg 2";
                        color: rgb(150, 150, 150);
                        background-color: transparent;
                        padding: 20px;
                }
                """
        )
        self.content_layout.addItem(spacer_top)
        self.content_layout.addWidget(self.placeholder_label)
        self.content_layout.addItem(spacer_bottom)

        # Add stretch to push content to top when items are added
        self.content_layout.addStretch()

        # Set content widget in scroll area
        self.scroll_area.setWidget(self.content_widget)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Clipboard Manager"))
        self.header_name.setText(_translate("MainWindow", "Clipboard Data"))
        self.clearall_button.setText(_translate("MainWindow", "Clear All"))
        self.history_button.setText(_translate("MainWindow", "History"))

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())