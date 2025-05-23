from PyQt5 import QtCore, QtGui, QtWidgets # type: ignore
from utils.clippad_text_resize import ElidedLabel # type: ignore
from PyQt5.QtGui import QIcon # type: ignore
from PyQt5.QtCore import Qt # type: ignore

# Local imports
from stylesheets.main_window_style import *
from stylesheets.button_styles import *
from stylesheets.label_text_style import *
from stylesheets.main_body_style import *

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        # MainWindow.resize(476, 551)
        MainWindow.setFixedSize(QtCore.QSize(476, 551))
        self.icon_path = "assets/restore_gif.gif"  # Path to your icon file
        MainWindow.setStyleSheet(MAIN_WINDOW_STYLE)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.header_name = QtWidgets.QLabel(self.centralwidget)
        self.header_name.setGeometry(QtCore.QRect(10, 10, 141, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.header_name.setFont(font)
        self.header_name.setStyleSheet(HEADER_NAME_STYLE)
        self.header_name.setObjectName("header_name")


        # Create restore button
        self.restore_button = QtWidgets.QPushButton(self.centralwidget)
        self.restore_button.setGeometry(QtCore.QRect(230, 12, 40, 40))  # Positioned before history_button
        self.restore_button.setIcon(QIcon(self.icon_path))  # Make sure your icon is already white
        self.restore_button.setIconSize(QtCore.QSize(40, 40))
        self.restore_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.restore_button.setStyleSheet(RESTORE_BUTTON_STYLE)
        self.restore_button.setText("")  # No text
        self.restore_button.setObjectName("restore_button")

        # Create animation label (for GIF)
        self.animation_label = QtWidgets.QLabel(self.centralwidget)
        self.animation_movie = QtGui.QMovie("assets/restore_gif.gif")
        self.animation_label.setMovie(self.animation_movie)
        self.animation_label.resize(40, 40)
        self.animation_label.setStyleSheet(ANIMATION_LABEL_STYLE)  # Make it transparent
        self.animation_label.move(238, 12)  # Same position as restore_button
        self.animation_label.hide()

        

        self.clearall_button = QtWidgets.QPushButton(self.centralwidget)
        self.clearall_button.setGeometry(QtCore.QRect(380, 10, 91, 41))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.clearall_button.setFont(font)
        self.clearall_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.clearall_button.setStyleSheet(CLEARALL_BUTTON_STYLE)

        self.clearall_button.setObjectName("clearall_button")
        self.history_button = QtWidgets.QPushButton(self.centralwidget)
        self.history_button.setGeometry(QtCore.QRect(280, 10, 91, 41))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.history_button.setFont(font)
        self.history_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.history_button.setStyleSheet(
            HISTORY_BUTTON_STYLE
        )
        self.history_button.setObjectName("history_button")

        self.line_seperator = QtWidgets.QFrame(self.centralwidget)
        self.line_seperator.setGeometry(QtCore.QRect(10, 65, 451 , 1))  # Moves it 15px lower, makes it thinner
        self.line_seperator.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_seperator.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_seperator.setObjectName("line_seperator")
        self.line_seperator.setStyleSheet(LINE_SEPARATOR_STYLE)

        # Scroll Area for Dynamic Labels
        self.scroll_area = QtWidgets.QScrollArea(self.centralwidget)
        self.scroll_area.setGeometry(QtCore.QRect(10, 80, 461, 450))  # Increased height
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setStyleSheet(SCROLL_AREA_STYLE)
        self.scroll_area.setObjectName("scroll_area")

        # ✅ Apply style directly to the vertical scroll bar
        self.scroll_area.verticalScrollBar().setStyleSheet(SCROLL_BAR_STYLE)


        # Content Widget inside Scroll Area
        self.content_widget = QtWidgets.QWidget()
        self.content_widget.setStyleSheet(CONTENT_WIDGET_STYLE)
        
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
                PLACEHOLDER_LABEL_STYLE
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