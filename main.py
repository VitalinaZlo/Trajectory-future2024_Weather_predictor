import sys
from logic import restore_integrity
from PyQt5.QtWidgets import QApplication
from ui import App

if __name__ == "__main__":
    app = QApplication(sys.argv)
    restore_integrity()
    window = App()
    window.show()
    sys.exit(app.exec_())
