from PyQt5.QtWidgets import QApplication, QMainWindow # type: ignore
from PyQt5.QtCore import pyqtSlot, Qt, QDate # type: ignore
from PyQt5.QtGui import QClipboard , QIcon # type: ignore
from PyQt5 import QtWidgets , QtCore # type: ignore
from PyQt5.QtSql import QSqlQuery # type: ignore


#? Utility imports
from utils.clippad_text_resize import ElidedLabel
from datetime import datetime , date
import calendar
import os

#? Ui imports
from ui.clipboard_manager import Ui_MainWindow
from stylesheets.button_styles import *
from stylesheets.label_text_style import *

#? DB imports
from Db.database import get_db_connection
from Db.models import init_db
from Db.sql_queries.sql_command_for_load_histories import *
from Db.sql_queries.sql_command_for_text_save import *
from Db.sql_queries.sql_command_for_data_insertion import *
from Db.sql_queries.sql_command_for_load_alltime_histories import *


from core.navigation.month_navigation import MonthNavigator

class ClipboardManager(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        # Set window icon
        icon_path = os.path.join(os.path.dirname(__file__),"..", "assets", "clipboard_manager_icon.ico")
        self.setWindowIcon(QIcon(icon_path))
        
        try:
            import ctypes
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID('my.clipboard.manager.1')
        except:
            pass
        self.no_history_label = None

        #? DB initialization
        if not init_db():
            print("Failed to initialize database")

        # In __init__
        self.current_view_items = []  # To track items currently displayed
        self.selected_date = None     # Optional: track selected date

        #? Initialize navigator
        self.month_navigator = MonthNavigator(self)
        
        self.history_heading = None
        self.is_history_button_clicked = False

        #? Set proper window flags
        self.setWindowFlags(QtCore.Qt.Window | QtCore.Qt.WindowTitleHint | QtCore.Qt.WindowCloseButtonHint)

        #? Keep window always on top
        self.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint, True)

        #? Reference to system clipboard
        self.clipboard = QApplication.clipboard()
        self.clipboard.dataChanged.connect(self.on_clipboard_changed)
        
        #? Also monitor primary selection
        self.clipboard.selectionChanged.connect(self.on_selection_changed)
        
        #? Keep track of clipboard items to avoid duplicates
        #? For new items to save to DB
        self.clipboard_items = []
        #? For items already in DB     
        self.loaded_from_db = []     

        self.load_clipboard_history()
        self.clearall_button.installEventFilter(self)
        self.restore_button.installEventFilter(self)
        #? Implementation the logic of clearing all items
        self.clearall_button.clicked.connect(self.clear_all_items)
        #? Connect click event for restoring data
        self.restore_button.clicked.connect(self.handle_restore_click)
        #? History Button connection for loading all-time history
        self.history_button.clicked.connect(self.load_alltime_history)
        
    def eventFilter(self, obj, event):
        if obj in [self.clearall_button, self.restore_button]:
            if event.type() == QtCore.QEvent.Enter:
                if not obj.isEnabled():
                    QtWidgets.QApplication.setOverrideCursor(QtCore.Qt.ForbiddenCursor)
                else:
                    QtWidgets.QApplication.setOverrideCursor(QtCore.Qt.PointingHandCursor)
            elif event.type() == QtCore.QEvent.Leave:
                QtWidgets.QApplication.restoreOverrideCursor()
        return super().eventFilter(obj, event)


    def closeEvent(self, event):
        QtWidgets.QApplication.restoreOverrideCursor()
        event.accept()

    def load_alltime_history(self):
        layout = self.content_layout
        db = get_db_connection()
        if not db:
            print("Failed to connect to database")
            return

        if not self.is_history_button_clicked:
            print("btn changed to back....")
            self.clearall_button.setEnabled(False)
            self.restore_button.setEnabled(False)
            


            # Clear current UI state
            for i in reversed(range(layout.count())):
                item = layout.itemAt(i)
                if item.widget() and item.widget() != self.placeholder_label:
                    widget = item.widget()
                    layout.removeWidget(widget)
                    widget.deleteLater()

            # Remove placeholder if exists
            if self.placeholder_label is not None:
                try:
                    layout.removeWidget(self.placeholder_label)
                    self.placeholder_label.deleteLater()
                    self.placeholder_label = None
                except Exception as e:
                    print("Error removing placeholder:", e)

            # Setup month/year from current date
            current_date = QtCore.QDate.currentDate()
            self.month_navigator.current_year = current_date.year()
            self.month_navigator.current_month = current_date.month()

            # Create prev/next buttons and connect signals
            self.month_navigator.prev_month_btn = QtWidgets.QPushButton("←")
            self.month_navigator.prev_month_btn.setFixedSize(40, 40)
            self.month_navigator.prev_month_btn.setCursor(Qt.PointingHandCursor)
            self.month_navigator.prev_month_btn.setStyleSheet("""
                QPushButton {
                    background-color: rgb(41, 41, 41);
                    border-radius: 20px;
                    font: bold 10pt "MS Shell Dlg 2";
                    color: white;
                    border: none;
                }
                QPushButton:hover {
                    background-color: rgb(60, 60, 60);
                }
                QPushButton:pressed {
                    background-color: rgb(80, 80, 80);
                }
            """)
            self.month_navigator.prev_month_btn.clicked.connect(self.month_navigator.load_previous_month)

            self.month_navigator.next_month_btn = QtWidgets.QPushButton("→")
            self.month_navigator.next_month_btn.setFixedSize(40, 40)
            self.month_navigator.next_month_btn.setCursor(Qt.PointingHandCursor)
            self.month_navigator.next_month_btn.setStyleSheet(self.month_navigator.prev_month_btn.styleSheet())
            self.month_navigator.next_month_btn.clicked.connect(self.month_navigator.load_next_month)

            self.month_navigator.month_label = QtWidgets.QLabel()
            self.month_navigator.month_label.setAlignment(Qt.AlignCenter)
            self.month_navigator.month_label.setStyleSheet("""
                QLabel {
                    font: bold 12pt "MS Shell Dlg 2";
                    color: white;
                    padding: 0 10px;
                }
            """)
            self.month_navigator.update_month_label()

            # Create navigation bar
            self.month_nav_widget = QtWidgets.QWidget()
            nav_layout = QtWidgets.QHBoxLayout()
            nav_layout.setContentsMargins(0, 0, 0, 0)
            nav_layout.setSpacing(15)
            nav_layout.setAlignment(Qt.AlignCenter)
            nav_layout.addWidget(self.month_navigator.prev_month_btn)
            nav_layout.addWidget(self.month_navigator.month_label)
            nav_layout.addWidget(self.month_navigator.next_month_btn)
            self.month_nav_widget.setLayout(nav_layout)
            layout.insertWidget(0, self.month_nav_widget)

            # All-time heading
            self.history_heading = QtWidgets.QLabel("All-Time Clipboard Histories", self.content_widget)
            self.history_heading.setObjectName("history_heading")
            self.history_heading.setAlignment(Qt.AlignLeft | Qt.AlignTop)
            self.history_heading.setStyleSheet("""
                QLabel#history_heading {
                    font: 11pt "MS Shell Dlg 2";
                    color: white;
                    background-color: transparent;
                    padding: 10px;
                    margin-bottom: 10px;
                }
            """)
            layout.insertWidget(1, self.history_heading)

            # Generate calendar
            self.calendar_widget = self.month_navigator.create_calendar_buttons()
            layout.insertWidget(2, self.calendar_widget)

            self.is_history_button_clicked = True
            self.history_button.setText("Back")

        else:
            print("btn changed to history....")
            self.clearall_button.setEnabled(True)
            self.restore_button.setEnabled(True)
            
            self.history_button.setText("History")
            self.is_history_button_clicked = False

            if self.placeholder_label is None:
                # Recreate placeholder if it doesn't exist
                self.placeholder_container = QtWidgets.QWidget(self.content_widget)
                placeholder_layout = QtWidgets.QVBoxLayout(self.placeholder_container)
                placeholder_layout.setContentsMargins(0, 0, 0, 0)

                # Add expanding spacers for vertical centering
                spacer_top = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
                spacer_bottom = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)

                # Create the label
                self.placeholder_label = QtWidgets.QLabel(
                    "Nothing Here\nYou'll see your clipboard history once you copied something..", 
                    self.placeholder_container
                )
                self.placeholder_label.setAlignment(Qt.AlignCenter)
                self.placeholder_label.setWordWrap(True)
                self.placeholder_label.setObjectName("placeholder_label")
                self.placeholder_label.setStyleSheet(PLACEHOLDER_LABEL_STYLE)

                # Add to layout
                placeholder_layout.addItem(spacer_top)
                placeholder_layout.addWidget(self.placeholder_label)
                placeholder_layout.addItem(spacer_bottom)

                # Add the container to your main layout
                layout.addWidget(self.placeholder_container)



                

            # Safely remove heading
            if self.history_heading:
                layout.removeWidget(self.history_heading)
                self.history_heading.deleteLater()
                self.history_heading = None

            # Safely remove calendar
            if self.calendar_widget:
                layout.removeWidget(self.calendar_widget)
                self.calendar_widget.deleteLater()
                self.calendar_widget = None

            # Safely remove navigation bar
            if self.month_nav_widget:
                layout.removeWidget(self.month_nav_widget)
                self.month_nav_widget.deleteLater()
                self.month_nav_widget = None

            # Reset navigator references
            self.month_navigator.prev_month_btn = None
            self.month_navigator.next_month_btn = None
            self.month_navigator.month_label = None

            # Reload today's data
            self.handle_restore_click()
    
    def add_clipboard_item_to_ui(self, text):
        # Check if we already have a container
        if not hasattr(self, 'clipboard_container') or self.clipboard_container is None:
            # Recreate container if it doesn't exist
            self.clipboard_container = QtWidgets.QWidget(self.content_widget)
            self.clipboard_container.setObjectName("clipboard_container")
            self.clipboard_container.setStyleSheet("background-color: transparent;")

            self.clipboard_container_layout = QtWidgets.QVBoxLayout(self.clipboard_container)
            self.clipboard_container_layout.setSpacing(5)
            self.clipboard_container_layout.setContentsMargins(0, 0, 0, 0)

            # Insert container at index 3 (after heading, nav bar, and calendar)
            self.content_layout.insertWidget(0, self.clipboard_container)

        # Create new elided label
        label = ElidedLabel(manager=self,parent=self.clipboard_container)
        label.setOriginalText(text)
        label.setMaxLines(3)
        label.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        label.setWordWrap(True)
        label.setCursor(Qt.PointingHandCursor)
        label.setStyleSheet(DATA_TEXT_FIELD_STYLE)
        label.setObjectName("dynamic_text_label")
        label.setMinimumHeight(40)

        # Add to container layout
        self.clipboard_container_layout.addWidget(label)

    def show_no_history_message(self, message: str):
        # Remove previous no_history_label if it exists and has been deleted
        if getattr(self, 'no_history_label', None):
            try:
                self.no_history_label.setText(message)
            except RuntimeError:
                # QLabel has been deleted; recreate it
                self.no_history_label = None

        # Create new QLabel if it doesn't exist
        if self.no_history_label is None:
            self.no_history_label = QtWidgets.QLabel(message, self.content_widget)
            self.no_history_label.setObjectName("no_history_label")
            self.no_history_label.setAlignment(Qt.AlignCenter)
            self.no_history_label.setWordWrap(True)
            self.no_history_label.setStyleSheet("""
                QLabel {
                    color: #888;
                    font-size: 18px;
                    font-family: "MS Shell Dlg 2";
                    padding: 20px;
                }
            """)
            self.content_layout.insertWidget(3, self.no_history_label)
        else:
            self.no_history_label.setText(message)


    def load_clipboard_history(self):
        """Load clipboard history from database and display"""
        db = get_db_connection()
        if not db:
            print("Failed to connect to database")
            return

        today_date = datetime.now().strftime("%Y-%m-%d")
        query = QSqlQuery()
        query.exec_(SQL_QUERY_FOR_LOAD_HISTORIES(today_date))


        while query.next():
            text = query.value(0)
            if text not in self.loaded_from_db:
                self.loaded_from_db.append(text)
                self.add_clipboard_item(text)
        
    # Show animation
    def handle_restore_click(self):
        """Restore all items from the database"""
        self.animation_label.show()
        self.animation_movie.start()
        has_data = False

        # Hide original button temporarily (optional)
        self.restore_button.setEnabled(False)
        print("Restoring all items!")
        db = get_db_connection()
        if not db:
            print("Failed to connect to database")
            return
        # always clear all items before restoring
        self.clear_all_items()
        # Delay to allow animation to show
        QtCore.QTimer.singleShot(1000, self.stop_restore_animation)
        
        today_date = datetime.now().strftime("%Y-%m-%d")
        query = QSqlQuery()
        query.exec_(SQL_QUERY_FOR_LOAD_HISTORIES(today_date))

        

        while query.next():
            has_data = True
            text = query.value(0)
            # Create new elided label
            self.clipboard_items.append(text)
            label = ElidedLabel(manager=self,parent=self.content_widget)
            label.setOriginalText(text)
            label.setMaxLines(3)
            label.setAlignment(Qt.AlignLeft | Qt.AlignTop)
            label.setWordWrap(True)
            label.setCursor(Qt.PointingHandCursor)
            label.setStyleSheet(DATA_TEXT_FIELD_STYLE)
            label.setObjectName("dynamic_text_label")
            label.setMinimumHeight(40)
            print("Restoring labels to layout")  # Debug log
            self.content_layout.insertWidget(0, label)
            # Force layout updates
            self.content_widget.updateGeometry()
            self.scroll_area.updateGeometry()
            self.update()
        if not has_data:
            print("DATA IS YET TO BE ENTRIED")
        elif hasattr(self, 'placeholder_label') and self.placeholder_label is not None:
            try:
                print("Removing placeholder")  # Debug log
                self.content_layout.removeWidget(self.placeholder_label)
                self.placeholder_label.deleteLater()
                self.placeholder_label = None
            except:
                pass  # Placeholder might already be removed
        # Clear calendar view elements
        elif hasattr(self, 'calendar_widget') and self.calendar_widget:
            self.content_layout.removeWidget(self.calendar_widget)
            self.calendar_widget.deleteLater()
            self.calendar_widget = None
        else:
            ...

        # Stop animation after 1 seconds and restore button
    
    def stop_restore_animation(self):
        self.animation_label.hide()
        self.animation_movie.stop()
        self.animation_movie.start()  # Restart for next use
        self.restore_button.setEnabled(True)

    def clear_all_items(self):
        """Clear all clipboard items but keep the placeholder"""
        print("Clearing all items!")

        layout = self.content_layout
        
        # Check if there are any clipboard items to clear
        has_clipboard_items = any(
            item.widget() and item.widget() != self.placeholder_label 
            for item in [layout.itemAt(i) for i in range(layout.count())] 
            if item and item.widget()
        )
        
        # If no clipboard items exist, don't do anything
        if not has_clipboard_items and len(self.clipboard_items) == 0:
            print("No items to clear, placeholder already visible")
            return
        
        # Remove all widgets except the placeholder and spacers
        for i in reversed(range(layout.count())):
            item = layout.itemAt(i)
            if item.widget():
                widget = item.widget()
                # Only remove widgets that are NOT the placeholder
                if widget != self.placeholder_label:
                    print(f"Removing widget: {widget.objectName()}")
                    layout.removeWidget(widget)
                    widget.deleteLater()
            elif item.spacerItem():
                # Remove spacer items (stretch)
                layout.removeItem(item)

        # Show placeholder if it was hidden
        if hasattr(self, 'placeholder_label') and self.placeholder_label is not None:
            self.placeholder_label.show()
            # Check if placeholder is already in layout
            placeholder_in_layout = any(
                layout.itemAt(i).widget() == self.placeholder_label 
                for i in range(layout.count()) 
                if layout.itemAt(i) and layout.itemAt(i).widget()
            )
            
            if not placeholder_in_layout:
                # Add spacers and placeholder
                spacer_top = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
                spacer_bottom = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
                layout.addItem(spacer_top)
                layout.addWidget(self.placeholder_label)
                layout.addItem(spacer_bottom)
            else:
                # Placeholder is already in layout, just add spacers if needed
                if layout.count() == 1:  # Only placeholder exists
                    spacer_top = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
                    spacer_bottom = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
                    layout.insertItem(0, spacer_top)
                    layout.addItem(spacer_bottom)
        else:
            # Recreate placeholder if it doesn't exist
            self.placeholder_label = QtWidgets.QLabel("Nothing Here\nYou'll see your clipboard history once you copied something..", self.content_widget)
            self.placeholder_label.setAlignment(Qt.AlignCenter)
            self.placeholder_label.setWordWrap(True)
            self.placeholder_label.setObjectName("placeholder_label")
            self.placeholder_label.setStyleSheet(
                PLACEHOLDER_LABEL_STYLE
            )
            spacer_top = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
            spacer_bottom = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
            layout.addItem(spacer_top)
            layout.addWidget(self.placeholder_label)
            layout.addItem(spacer_bottom)
                        
        # Clear internal list
        self.clipboard_items.clear()
        
        # Force update
        self.content_widget.update()
        self.scroll_area.update()
        print("All items cleared, placeholder restored")
        
    @pyqtSlot()
    def on_clipboard_changed(self):
        """Triggered when clipboard content changes"""
        print("Clipboard changed!")  # Debug log
        if self.is_history_button_clicked:
            # Prevent saving clipboard changes while browsing history
            return
        mime_data = self.clipboard.mimeData()
        
        if mime_data.hasText():
            text = mime_data.text().strip()
            if text and text not in self.clipboard_items:  # Avoid duplicates
                print(f"New selection text: {text}")  # Debug log
                self.add_clipboard_item(text)

    @pyqtSlot()
    def on_selection_changed(self):
        """Triggered when primary selection changes"""
        print("Primary selection changed!")  # Debug log
        mime_data = self.clipboard.mimeData(QClipboard.Selection)
        
        if mime_data.hasText():
            text = mime_data.text().strip()
            if text and text not in self.clipboard_items:  # Avoid duplicates
                print(f"New selection text: {text}")  # Debug log
                self.add_clipboard_item(text)

    def add_clipboard_item(self, text):
        print(f"Adding clipboard item: {text}")  # Debug log
        
        # Add to our tracking list
        self.clipboard_items.append(text)

        
        
        # Remove placeholder if it exists
        if hasattr(self, 'placeholder_label') and self.placeholder_label is not None:
            try:
                print("Removing placeholder")  # Debug log
                self.content_layout.removeWidget(self.placeholder_label)
                self.placeholder_label.deleteLater()
                self.placeholder_label = None
            except:
                pass  # Placeholder might already be removed
        
        # Create new elided label
        label = ElidedLabel(manager=self,parent=self.content_widget)
        label.setOriginalText(text)
        label.setMaxLines(3)
        label.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        label.setWordWrap(True)
        label.setCursor(Qt.PointingHandCursor)
        label.setStyleSheet(DATA_TEXT_FIELD_STYLE)
        label.setObjectName("dynamic_text_label")
        
        # Set minimum height to ensure visibility
        label.setMinimumHeight(40)
        # Save to database
        
        # Add to layout at the top (most recent first)
        print("Adding label to layout")  # Debug log
        self.content_layout.insertWidget(0, label)
        self.save_to_database(text)
        
        # Force layout updates
        self.content_widget.updateGeometry()
        self.scroll_area.updateGeometry()
        self.update()
        
        print(f"Layout now has {self.content_layout.count()} items")  # Debug log
    def save_to_database(self, text):
        db = get_db_connection()
        if not db:
            return

        today_date = datetime.now().strftime("%Y-%m-%d")

        # Check if this text was already saved today
        query = QSqlQuery()
        query.prepare(SQL_CHECK_FOR_TEXT_SAVE)
        query.bindValue(":content", text)
        query.bindValue(":date", today_date)
        query.exec_()
        query.next()

        if query.value(0) > 0:
            print("Text already exists in DB for today")
            return

        # Insert if not duplicate
        insert_query = QSqlQuery()
        insert_query.prepare(SQL_COMMAND_FOR_DATA_INSERTION)
        insert_query.bindValue(":content", text)
        insert_query.bindValue(":date", today_date)

        if not insert_query.exec_():
            print("Error saving to database:", insert_query.lastError().text())
        else:
            print(f"Saved to DB: {text[:30]}...")

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = ClipboardManager()
    window.show()
    sys.exit(app.exec_())