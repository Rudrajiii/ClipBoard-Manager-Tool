# clipboard_watcher.py
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import pyqtSlot, Qt
from PyQt5.QtGui import QClipboard
from PyQt5 import QtWidgets
from ui.clipboard_manager import Ui_MainWindow
from utils.clippad_text_resize import ElidedLabel

class ClipboardManager(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        
        # Reference to system clipboard
        self.clipboard = QApplication.clipboard()
        self.clipboard.dataChanged.connect(self.on_clipboard_changed)
        
        # Also monitor primary selection (optional)
        self.clipboard.selectionChanged.connect(self.on_selection_changed)
        
        # Keep track of clipboard items to avoid duplicates
        self.clipboard_items = []

        # will implement the logic of clearing all items
        self.clearall_button.clicked.connect(self.clear_all_items)
        
        # For testing (optional)
        # long_text = "hell ya boi"
        # self.add_clipboard_item(long_text)
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
                """
                QLabel {
                        font: 11pt "MS Shell Dlg 2";
                        color: rgb(150, 150, 150);
                        background-color: transparent;
                        padding: 20px;
                }
                """
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
        label.setStyleSheet("""
            QLabel {
                font: 11pt "MS Shell Dlg 2";
                color: rgb(255, 255, 255);
                background-color: rgb(30, 30, 30);
                border: 1px solid rgb(75, 75, 75);
                border-radius: 8px;
                padding: 5px;
                margin: 2px;
            }
            QLabel:hover {
                border: 1px solid white;
            }
        """)
        label.setObjectName("dynamic_text_label")
        
        # Set minimum height to ensure visibility
        label.setMinimumHeight(40)
        
        # Add to layout at the top (most recent first)
        print("Adding label to layout")  # Debug log
        self.content_layout.insertWidget(0, label)
        
        # Force layout updates
        self.content_widget.updateGeometry()
        self.scroll_area.updateGeometry()
        self.update()
        
        print(f"Layout now has {self.content_layout.count()} items")  # Debug log

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = ClipboardManager()
    window.show()
    sys.exit(app.exec_())