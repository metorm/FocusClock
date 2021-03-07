from os import system
import time
import sys

from win32 import win32gui, win32process, win32api
import win32con
import pywintypes

import PopWindow
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QTimer, Qt

whiteWindowPrefixList = [
    "Office\\root\Office16\WINWORD.EXE", "Office\\root\Office16\VISIO.EXE", "Code\Code.exe", "SearchApp.exe"]

popWindowObject = None


def doINeedWaring():
    checkSuccess = False
    proc_name = None

    while not checkSuccess:
        try:
            frontWindowHandle = frontWindowHandleTitle = thread_id = process_id = processToCheck = proc_name = None

            frontWindowHandle = win32gui.GetForegroundWindow()
            frontWindowHandleTitle = win32gui.GetWindowText(frontWindowHandle)

            thread_id, process_id = win32process.GetWindowThreadProcessId(
                frontWindowHandle)
            processToCheck = win32api.OpenProcess(
                win32con.PROCESS_QUERY_INFORMATION | win32con.PROCESS_VM_READ, False, process_id)
            proc_name = win32process.GetModuleFileNameEx(processToCheck, 0)
            checkSuccess = True
        except pywintypes.error:
            time.sleep(50)
            print(
                "(Don't panic! This is for developers!) Win32 error happeend: fW={}, fWTitle={}, thread_id={}, process_id={}, processToCheck={}, proc_name={}".format(
                    frontWindowHandle, frontWindowHandleTitle, thread_id, process_id, processToCheck, proc_name))

    needWaring = True
    for w in whiteWindowPrefixList:
        if proc_name.endswith(w):
            needWaring = False
            break

    if needWaring:
        print("You are not working! {} | {}".format(
            frontWindowHandleTitle, proc_name))

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

    # window
    popWindowObject = PopWindow.WindowNotify(animationDuration=50)
    popWindowObject.show()

    # timer
    checkTimer = QTimer(timeout=postWarningIfNeeded)
    checkTimer.setInterval(1000)
    checkTimer.start()

    sys.exit(app.exec_())
