import time
import sys
import json

from win32 import win32gui, win32process, win32api
import win32con
import pywintypes

import PopWindow
from WhiteList import WhiteList

from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QTimer, Qt


theWhiteList: WhiteList = None

popWindowObject = None


def doINeedWaring():
    checkSuccess = False
    processName = None
    frontWindowTitle = None

    while not checkSuccess:
        try:
            frontWindowHandle = frontWindowTitle = thread_id = process_id = processToCheck = processName = None

            frontWindowHandle = win32gui.GetForegroundWindow()
            frontWindowTitle = win32gui.GetWindowText(frontWindowHandle)

            thread_id, process_id = win32process.GetWindowThreadProcessId(
                frontWindowHandle)
            processToCheck = win32api.OpenProcess(
                win32con.PROCESS_QUERY_INFORMATION | win32con.PROCESS_VM_READ, False, process_id)
            processName = win32process.GetModuleFileNameEx(processToCheck, 0)
            checkSuccess = True
        except pywintypes.error:
            time.sleep(0.1)
            print(
                "(Don't panic! This is for developers!) Win32 error happeend: fW={}, fWTitle={}, thread_id={}, process_id={}, processToCheck={}, proc_name={}".format(
                    frontWindowHandle, frontWindowTitle, thread_id, process_id, processToCheck, processName))

    needWaring = not theWhiteList.test(processName, frontWindowTitle)

    message = "You are {}working! {} | {}".format(
        "not " if needWaring else "", frontWindowTitle, processName)
    print(message)

    return needWaring


previousWaringStatus = False


def postWarningIfNeeded():
    global previousWaringStatus

    currentWarningStatus = doINeedWaring()

    if(previousWaringStatus != currentWarningStatus):
        if (currentWarningStatus):
            popWindowObject.showViaAnimation()
        else:
            popWindowObject.closeViaAnimation()

    previousWaringStatus = currentWarningStatus


if __name__ == "__main__":

    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)

    app = QApplication(sys.argv)

    # list
    theWhiteList = WhiteList()
    with open("SampleConfig.json") as jFile:
        configData = json.load(jFile)
        theWhiteList.buildFromDict(configData["whiteList"])

    # window
    popWindowObject = PopWindow.WindowNotify(animationDuration=50)
    popWindowObject.show()

    # timer
    checkTimer = QTimer(timeout=postWarningIfNeeded)
    checkTimer.setInterval(1000)
    checkTimer.start()

    sys.exit(app.exec_())
