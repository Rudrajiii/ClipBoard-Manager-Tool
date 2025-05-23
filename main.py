import sys
from PyQt5.QtWidgets import QApplication # type: ignore
from core.clipboard_manager_tool import ClipboardManager

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ClipboardManager()
    window.show()
    sys.exit(app.exec_())
