import sys
from PyQt5.QtWidgets import QApplication # type: ignore
from core.clipboard_manager_tool import ClipboardManager

if __name__ == "__main__":
    try:
        print("Starting Clipboard Manager...")
        # Initialize the application
        app = QApplication(sys.argv)
        window = ClipboardManager()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)

