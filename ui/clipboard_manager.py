from PyQt5 import QtCore, QtGui, QtWidgets # type: ignore
from utils.clippad_text_resize import ElidedLabel # type: ignore
from PyQt5.QtGui import QIcon # type: ignore
from PyQt5.QtCore import Qt # type: ignore

# Local imports
from stylesheets.main_window_style import *
from stylesheets.button_styles import *
from stylesheets.label_text_style import *
from stylesheets.main_body_style import *
import os
import sys

class CustomTitleBar(QtWidgets.QWidget):
    """Custom title bar for frameless window with dragging capability"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_window = parent
        self.setFixedHeight(35)
        self.setStyleSheet("""
            background-color: #000;
            border-top-left-radius: 8px;
            border-top-right-radius: 8px;
        """)
        
        # Create layout
        layout = QtWidgets.QHBoxLayout(self)
        layout.setContentsMargins(10, 0, 5, 0)
        # layout.setFont(self.font)
        layout.setSpacing(0)
        # layout.
        
        # Title label with icon
        self.title = QtWidgets.QLabel("📋 Clipyy", self)
        self.title.setStyleSheet("""
            color: white;
            font-weight: bold;
            font-size: 16px;
            background: transparent;
        """)
        layout.addWidget(self.title)
        layout.addStretch()
        
        # Minimize button
        self.min_btn = QtWidgets.QPushButton("—", self)
        self.min_btn.setFixedSize(40, 30)
        self.min_btn.setStyleSheet("""
            QPushButton {
                color: white;
                background: transparent;
                border: none;
                font-size: 18px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #333333;
            }
        """)
        self.min_btn.clicked.connect(lambda: parent.showMinimized() if parent else None)
        layout.addWidget(self.min_btn)
        
        # Close button
        self.close_btn = QtWidgets.QPushButton("✕", self)
        self.close_btn.setFixedSize(40, 30)
        self.close_btn.setStyleSheet("""
            QPushButton {
                color: white;
                background: transparent;
                border: none;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #e81123;
            }
        """)
        self.close_btn.clicked.connect(lambda: parent.close() if parent else None)
        layout.addWidget(self.close_btn)
        
        # For window dragging
        self._drag_pos = None
    
    def mousePressEvent(self, event):
        """Handle mouse press for window dragging"""
        if event.button() == QtCore.Qt.LeftButton:
            self._drag_pos = event.globalPos() - self.parent_window.frameGeometry().topLeft()
            event.accept()
    
    def mouseMoveEvent(self, event):
        """Handle mouse move for window dragging"""
        if event.buttons() == QtCore.Qt.LeftButton and self._drag_pos:
            self.parent_window.move(event.globalPos() - self._drag_pos)
            event.accept()
    
    def mouseReleaseEvent(self, event):
        """Handle mouse release"""
        self._drag_pos = None
        event.accept()

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        # Set frameless window
        MainWindow.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowSystemMenuHint)
        MainWindow.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        
        MainWindow.setObjectName("MainWindow")
        # MainWindow.resize(476, 551)
        MainWindow.resize(476, 587)  # Increased to accommodate title bar
        
        # Instead of fixed size, use minimum size
        MainWindow.setMinimumSize(QtCore.QSize(476, 587))
        
        # Optional: Set maximum size to same value to mimic fixed size
        MainWindow.setMaximumSize(QtCore.QSize(476, 587))
        icon_path = self.resource_path("assets/restore_gif.gif")  # Path to your icon file
        MainWindow.setStyleSheet(MAIN_WINDOW_STYLE)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.centralwidget.setStyleSheet("""
            QWidget#centralwidget {
                background-color: #252525;
                border-radius: 8px;
            }
        """)
        
        # Add custom title bar
        font = QtGui.QFont()
        font.setPointSize(12)
        self.title_bar = CustomTitleBar(MainWindow)
        self.title_bar.setParent(self.centralwidget)
        self.title_bar.setGeometry(QtCore.QRect(0, 0, 476, 35))
        self.title_bar.setFont(font)
        self.header_name = QtWidgets.QLabel(self.centralwidget)
        self.header_name.setGeometry(QtCore.QRect(10, 45, 141, 41))  # Moved down to accommodate title bar
        self.header_name.setFont(font)
        self.header_name.setStyleSheet(HEADER_NAME_STYLE)
        self.header_name.setObjectName("header_name")


        # Create restore button
        self.restore_button = QtWidgets.QPushButton(self.centralwidget)
        self.restore_button.setGeometry(QtCore.QRect(230, 47, 40, 40))  # Moved down by 35px
        self.restore_button.setIcon(QIcon(icon_path))  # Make sure your icon is already white
        self.restore_button.setIconSize(QtCore.QSize(40, 40))
        self.restore_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.restore_button.setStyleSheet(RESTORE_BUTTON_STYLE)
        self.restore_button.setText("")  # No text
        self.restore_button.setObjectName("restore_button")

        # Create animation label (for GIF)
        self.animation_label = QtWidgets.QLabel(self.centralwidget)
        self.animation_movie = QtGui.QMovie(icon_path)
        self.animation_label.setMovie(self.animation_movie)
        self.animation_label.resize(40, 40)
        self.animation_label.setStyleSheet(ANIMATION_LABEL_STYLE)  # Make it transparent
        self.animation_label.move(238, 47)  # Moved down by 35px
        self.animation_label.hide()

        self.clearall_button = QtWidgets.QPushButton(self.centralwidget)
        self.clearall_button.setGeometry(QtCore.QRect(380, 45, 91, 41))  # Moved down by 35px
        font = QtGui.QFont()
        font.setPointSize(11)
        self.clearall_button.setFont(font)
        self.clearall_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.clearall_button.setStyleSheet(CLEARALL_BUTTON_STYLE)

        self.clearall_button.setObjectName("clearall_button")
        self.history_button = QtWidgets.QPushButton(self.centralwidget)
        self.history_button.setGeometry(QtCore.QRect(280, 45, 91, 41))  # Moved down by 35px
        font = QtGui.QFont()
        font.setPointSize(11)
        self.history_button.setFont(font)
        self.history_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.history_button.setStyleSheet(
            HISTORY_BUTTON_STYLE
        )
        self.history_button.setObjectName("history_button")

        self.line_seperator = QtWidgets.QFrame(self.centralwidget)
        self.line_seperator.setGeometry(QtCore.QRect(10, 100, 451 , 1))  # Moved down by 35px
        self.line_seperator.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_seperator.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_seperator.setObjectName("line_seperator")
        self.line_seperator.setStyleSheet(LINE_SEPARATOR_STYLE)

        # Scroll Area for Dynamic Labels
        self.scroll_area = QtWidgets.QScrollArea(self.centralwidget)
        self.scroll_area.setGeometry(QtCore.QRect(10, 115, 461, 450))  # Moved down by 35px
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
        MainWindow.setWindowTitle(_translate("MainWindow", "Clipyy"))
        self.header_name.setText(_translate("MainWindow", "Clipboard Data"))
        self.clearall_button.setText(_translate("MainWindow", "Clear All"))
        self.history_button.setText(_translate("MainWindow", "History"))
    

    def resource_path(self,relative_path):
        """ Get absolute path to resource, works for dev and for PyInstaller """
        try:
            # PyInstaller creates a temp folder and stores path in _MEIPASS
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")

        return os.path.join(base_path, relative_path)

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())