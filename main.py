import requests
import subprocess
import sys
import urllib3
from bs4 import BeautifulSoup
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QMessageBox
from git import Repo
import urllib.request
import rarfile
from pyunpack import Archive
import pathlib
import importlib
import main
APP_VERSION = "0.0.1"



class Example(QWidget): 

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):

        btn = QPushButton(APP_VERSION, self)
        btn.setToolTip('Click to show message box')
        btn.resize(btn.sizeHint())
        btn.move(50, 50)
        btn.clicked.connect(lambda: self.check_for_updates(APP_VERSION)) # call check_for_updates with current_version parameter
        # btn.clicked.connect(self.showMessageBox)

        self.setGeometry(300, 300, 1000, 400)
        self.setWindowTitle('Example')
        self.show()

    def showMessageBox(self):
        QMessageBox.information(self, 'Message', 'Hello, world!')


    def check_for_updates(self, current_version):     
        try:
            http = urllib3.PoolManager()
            url = 'https://raw.githubusercontent.com/TBAZ123/TMP/main/VS.ini'
            response = http.request('GET', url)
            version_text = response.data.decode('utf-8')  # decode bytes to str
            version_parts = version_text.split('.')
            version = tuple(map(int, version_parts))
            current_version = current_version.split('.')
            current_version = tuple(map(int, current_version))
            if version > current_version:
                # QMessageBox.critical(None, 'Error', f'Failed to check for updatessss: {response.data}')
                reply = QMessageBox.question(None, 'Update available',
                                             f'A new version ({version_text}) is available. Do you want to update?',
                                             QMessageBox.Yes | QMessageBox.No)
                if reply == QMessageBox.Yes:
                    url = "https://raw.githubusercontent.com/TBAZ123/TMP/main/Tmp.rar"
                    filename = "Update_Tmp.rar"
                    urllib.request.urlretrieve(url, filename)
                    Archive(filename).extractall(pathlib.Path(__file__).parent.resolve())
                    # sys.exit(0)
                    QMessageBox.critical(None, 'Success', f'The update is successful, please close the program and relaunch it.')
                    sys.exit(0)
            else:
                QMessageBox.information(None, 'No update available', 'You have the latest version of the application.')
        except Exception as e:
            QMessageBox.critical(None, 'Error', f'Failed to check for updates: {e}')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
