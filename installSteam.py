import requests
import os
import platform
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QLabel
import subprocess

url = None

downloadForMac = "https://media.st.dl.eccdnx.com/client/installer/steam.dmg"
downloadForWin = "https://cdn.akamai.steamstatic.com/client/installer/SteamSetup.exe"
downloadForLinux = "https://steamcdn-a.akamaihd.net/client/installer/steam.deb"

hander = {
      "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

userDownloadPath = os.path.expanduser("~/Downloads")

def downloadSteam():
    system = platform.system()

    if system == "Windows":
        url = downloadForWin
        endName = "SteamSetup.exe"
    if system == "Darwin":
        url = downloadForMac
        endName = "steam.dmg"
    if system == "Linux":
        url = downloadForLinux
        endName = "steam.deb"

    response = requests.get(url, headers=hander)
    with open(f"{userDownloadPath}/{endName}", "wb") as f:
        f.write(response.content)
        f.close()

    installSteam()
def installSteam():
    system = platform.system()

    if system == "Windows":
        os.system(f"start {userDownloadPath}/SteamSetup.exe")

    if system == "Darwin":
        os.system(f"open {userDownloadPath}/steam.dmg")
        os.system("cp -r /Volumes/Steam/Steam.app /Applications")
        os.system("diskutil unmount /Volumes/Steam")
        cmd = "sudo spctl --master-disable"
        run_as_admin(cmd)
        QMessageBox.information(None, "提示", "如果显示Apple无法验证“Steam”是否包含可能危害Mac安全或泄漏隐私的恶意软件。\n需要手动打开访达->应用程序(Applications)文件夹->Steam.app->右键点击->打开")
        os.system("open /Applications/Steam.app")
        os.system("rm -rf ~/Downloads/steam.dmg")

    if system == "Linux":
        os.system(f"sudo dpkg -i {userDownloadPath}/steam.deb")

def run_as_admin(command):
    os_command = 'do shell script "{}" with administrator privileges'.format(command)
    subprocess.run(["osascript", "-e", os_command],timeout=10)
class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Steam安装器")
        self.setGeometry(100, 100, 300, 200)
        self.setFixedSize(300, 200)
        self.button = QPushButton("安装Steam", self)
        self.button.setGeometry(100, 100, 100, 50)
        title = QLabel("Steam安装器", self)
        title.setStyleSheet("font-size: 20px; font-weight: bold;")
        title.setGeometry(90, 10, 120, 50)
        title.setAlignment(Qt.AlignCenter)
        self.button.setStyleSheet("background-color: #4CAF50; color: white; border-radius: 10px;")

        self.button.clicked.connect(downloadSteam)
        self.show()

if __name__ == "__main__":

    app = QApplication([])

    window = MainWindow()

    app.exec_()
