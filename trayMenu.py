from PyQt5 import QtGui
from PyQt5.QtWidgets import QApplication, QSystemTrayIcon, QMenu, QAction

import globalData as g
import utility
import qtResource

trayActionSwitch: QAction = None
trayActionSwitchPauseMsg = "暂停监视 | Pause Monitoring"
trayActionSwitchStartMsg = "恢复监视 | Resume Monitoring"


def switchRunningStatus():
    global trayActionSwitchPauseMsg
    global trayActionSwitchStartMsg

    g.running = not g.running

    if g.running:
        trayActionSwitch.setText(trayActionSwitchPauseMsg)
    else:
        trayActionSwitch.setText(trayActionSwitchStartMsg)


def exitApp():
    QApplication.quit()


def setupTray(trayParent):

    tray = QSystemTrayIcon(trayParent)
    tray.setIcon(QtGui.QIcon(":/image/images/trayIcon-eye.png"))

    trayMenu = QMenu()

    global trayActionSwitch
    trayActionSwitch = QAction(trayActionSwitchPauseMsg, trayParent)
    trayActionSwitch.triggered.connect(switchRunningStatus)
    trayMenu.addAction(trayActionSwitch)

    trayActionAbout = QAction("关于 | About", trayParent)
    trayActionAbout.triggered.connect(utility.openAboutPage)
    trayMenu.addAction(trayActionAbout)

    trayActionExit = QAction("退出 | Exit", trayParent)
    trayActionExit.triggered.connect(exitApp)
    trayMenu.addAction(trayActionExit)

    tray.setContextMenu(trayMenu)

    tray.show()
