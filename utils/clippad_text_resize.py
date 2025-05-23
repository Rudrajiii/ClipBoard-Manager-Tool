from PyQt5 import QtWidgets, QtCore, QtGui # type: ignore
from PyQt5.QtWidgets import QApplication # type: ignore
from stylesheets.animation_style import *  

class ElidedLabel(QtWidgets.QLabel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setTextFormat(QtCore.Qt.PlainText)
        self.setWordWrap(True)
        self.setSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Ignored)
        self._original_text = ""
        self._paddings = (0, 0)
        self._max_lines = 3  # Show up to 3 lines
        self.setStyleSheet("padding: 5px;")
        self.setCursor(QtCore.Qt.PointingHandCursor)  # Optional: Set cursor on init

    def setOriginalText(self, text):
        self._original_text = text
        self.update_elided_text()

    def setTextPadding(self, left=0, right=0):
        self._paddings = (left, right)
        self.update_elided_text()

    def setMaxLines(self, lines):
        self._max_lines = lines
        self.update_elided_text()

    def resizeEvent(self, event):
        self.update_elided_text()
        return super().resizeEvent(event)

    def update_elided_text(self):
        if not self._original_text or self.width() <= 0:
            self.setText("")
            return

        metrics = QtGui.QFontMetrics(self.font())
        available_width = self.width() - self._paddings[0] - self._paddings[1]
        line_spacing = metrics.lineSpacing()
        max_height = line_spacing * self._max_lines

        lines = []
        paragraphs = self._original_text.split('\n')

        for para in paragraphs:
            words = para.split(' ')
            current_line = ""

            for word in words:
                test_line = current_line + (" " if current_line else "") + word
                if metrics.width(test_line) > available_width:
                    if current_line:
                        lines.append(current_line)
                        current_line = word
                    else:
                        # Word too long, break it
                        lines.append(word[:int(available_width / metrics.averageCharWidth()) - 1])
                        word = word[int(available_width / metrics.averageCharWidth()) - 1:]
                else:
                    current_line = test_line
            if current_line:
                lines.append(current_line)
                current_line = ""

            if len(lines) * line_spacing >= max_height:
                break  # Stop after reaching max lines

        # Truncate to max allowed lines
        lines = lines[:int(max_height / line_spacing)]

        self.setText("\n".join(lines))
    
    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton and self._original_text:
            clipboard = QApplication.clipboard()
            clipboard.setText(self._original_text)
            print(f"Copied to clipboard: {self._original_text}")
            # Trigger visual feedback
            self.animate_copy_feedback()
        super().mousePressEvent(event)
    
    def animate_copy_feedback(self):
        # Change border color to green indicate success
        self.setStyleSheet(ANIMATE_COPY_FEEDBACK)

        # Revert back after 1 second
        QtCore.QTimer.singleShot(1000, self.revert_style)
    
    def revert_style(self):
        self.setStyleSheet(REVERT_STYLE)