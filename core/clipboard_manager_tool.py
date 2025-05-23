from PyQt5.QtWidgets import QApplication, QMainWindow # type: ignore
from PyQt5.QtCore import pyqtSlot, Qt # type: ignore
from PyQt5.QtGui import QClipboard # type: ignore
from PyQt5 import QtWidgets , QtCore # type: ignore
from PyQt5.QtSql import QSqlQuery # type: ignore

#? Utility imports
from utils.clippad_text_resize import ElidedLabel
from datetime import datetime

#? Ui imports
from ui.clipboard_manager import Ui_MainWindow
from stylesheets.label_text_style import *

#? DB imports
from Db.database import get_db_connection
from Db.models import init_db
from Db.sql_queries.sql_command_for_load_histories import *
from Db.sql_queries.sql_command_for_text_save import *
from Db.sql_queries.sql_command_for_data_insertion import *

class ClipboardManager(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        # Initialize DB
        if not init_db():
            print("Failed to initialize database")

        # Set proper window flags
        self.setWindowFlags(QtCore.Qt.Window | QtCore.Qt.WindowTitleHint | QtCore.Qt.WindowCloseButtonHint)

        # Optional: Keep window always on top
        self.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint, True)
        # Reference to system clipboard
        self.clipboard = QApplication.clipboard()
        self.clipboard.dataChanged.connect(self.on_clipboard_changed)
        
        # Also monitor primary selection (optional)
        self.clipboard.selectionChanged.connect(self.on_selection_changed)
        
        # Keep track of clipboard items to avoid duplicates
        self.clipboard_items = []     # For new items to save to DB
        self.loaded_from_db = []     # For items already in DB

        self.load_clipboard_history()
        # will implement the logic of clearing all items
        self.clearall_button.clicked.connect(self.clear_all_items)
        # Connect click event
        self.restore_button.clicked.connect(self.handle_restore_click)
        
        
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
        # Remove placeholder if it exists
        if hasattr(self, 'placeholder_label') and self.placeholder_label is not None:
            try:
                print("Removing placeholder")  # Debug log
                self.content_layout.removeWidget(self.placeholder_label)
                self.placeholder_label.deleteLater()
                self.placeholder_label = None
            except:
                pass  # Placeholder might already be removed
        today_date = datetime.now().strftime("%Y-%m-%d")
        query = QSqlQuery()
        query.exec_(SQL_QUERY_FOR_LOAD_HISTORIES(today_date))

        

        while query.next():
            text = query.value(0)
            # Create new elided label
            self.clipboard_items.append(text)
            label = ElidedLabel(self.content_widget)
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
        mime_data = self.clipboard.mimeData()
        
        if mime_data.hasText():
            text = mime_data.text().strip()
            if text and text not in self.clipboard_items:  # Avoid duplicates
                print(f"New clipboard text: {text}")  # Debug log
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
        label = ElidedLabel(self.content_widget)
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