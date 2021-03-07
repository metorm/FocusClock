from PyQt5.QtCore import Qt, QPropertyAnimation, QPoint, QTimer, QPropertyAnimation, pyqtProperty
from PyQt5.QtWidgets import QLabel, QWidget, QPushButton, QHBoxLayout, QGraphicsColorizeEffect, QApplication
from PyQt5.QtGui import QColor


class WindowNotify(QWidget):

    def __init__(self, title="", content="", animationDuration=1000, *args, **kwargs):
        super(WindowNotify, self).__init__(*args, **kwargs)

        # 窗口内容
        self.setFixedSize(1000, 250)
        layout = QHBoxLayout(self)
        self.label = QLabel(self)
        self.label.setText("ε=(´ο｀*))) 你干啥呢")
        self.label.setAlignment(Qt.AlignCenter)

        self.label.setStyleSheet(
            "font-size: 96px; font-family: Microsoft Yahei, Roman;")

        p = self.palette()
        p.setColor(self.backgroundRole(), Qt.black)
        self.setPalette(p)

        layout.addWidget(self.label)

        self._animationDuration = animationDuration
        self._initWindowBehavior()

    def setTimeout(self, timeout):
        if isinstance(timeout, int):
            self._autoCloseTimeout = timeout
        return self

    def timeout(self):
        return self._autoCloseTimeout

    def onClose(self):
        # 其他渠道关闭
        self.isShow = False
        QTimer.singleShot(100, self.closeViaAnimation)  # 启动弹回动画

    def _initWindowBehavior(self):
        # 隐藏任务栏|去掉边框|顶层显示
        self.setWindowFlags(Qt.Tool | Qt.X11BypassWindowManagerHint |
                            Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        # 是否在显示标志
        self.isShow = True
        # 桌面
        self._desktop = QApplication.instance().desktop()
        # 窗口初始开始位置
        self._startPos = QPoint(
            self._desktop.screenGeometry().width() - self.width() - 5,
            self._desktop.screenGeometry().height()
        )
        # 窗口弹出结束位置
        self._endPos = QPoint(
            self._desktop.screenGeometry().width() - self.width() - 5,
            self._desktop.availableGeometry().height() - self.height() - 5
        )
        # 初始化位置到右下角
        self.move(self._startPos)

        # 动画
        self.animation = QPropertyAnimation(self, b"pos")
        self.animation.setDuration(self._animationDuration)  # ms

        self.labelEffect = QGraphicsColorizeEffect(self.label)
        self.label.setGraphicsEffect(self.labelEffect)
        self.labelColorAnimation = QPropertyAnimation(
            self.labelEffect, b"color")
        self.labelColorAnimation.setStartValue(QColor(Qt.yellow))
        self.labelColorAnimation.setEndValue(QColor(Qt.red))
        self.labelColorAnimation.setDuration(500)
        self.labelColorAnimation.setLoopCount(1)

        self.labelColorAnimation.finished.connect(self.flipAnimation)

    def flipAnimation(self):
        currentDirection = self.labelColorAnimation.direction()
        if currentDirection == QPropertyAnimation.Forward:
            self.labelColorAnimation.setDirection(QPropertyAnimation.Backward)
        else:
            self.labelColorAnimation.setDirection(QPropertyAnimation.Forward)

        self.labelColorAnimation.start()

    def show(self):
        self.hide()  # 先隐藏
        self.move(self._startPos)  # 初始化位置到右下角
        super(WindowNotify, self).show()
        return self

    def showViaAnimation(self):
        # 显示动画
        self.animation.stop()  # 先停止之前的动画,重新开始
        self.animation.setStartValue(self.pos())
        self.animation.setEndValue(self._endPos)
        self.animation.start()

        self.labelColorAnimation.start()

    def closeViaAnimation(self):
        # 通过动画关闭
        self.animation.stop()
        self.animation.setStartValue(self.pos())
        self.animation.setEndValue(self._startPos)
        self.animation.start()


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)

    window = QWidget()
    notify = WindowNotify(parent=window)
    notify.show()

    layout = QHBoxLayout(window)
    b1 = QPushButton(
        "弹窗", window, clicked=lambda: notify.showViaAnimation())
    b2 = QPushButton(
        "关闭", window, clicked=lambda: notify.closeViaAnimation())
    layout.addWidget(b1)
    layout.addWidget(b2)
    window.show()

    sys.exit(app.exec_())
