from PyQt6.QtWidgets import QApplication, QWidget
# Only needed for access to command line arguments
import sys

# You need one (and only one) QApplication instance per application.
# 애플리케이션당 하나의 QApplication 인스턴스가 필요합니다.
# Pass in sys.argv to allow command line arguments for your app.
# 앱에 대한 명령줄 인수를 허용하려면 sys.argv를 전달합니다.
# If you know you won't use command line arguments QApplication([]) works too.
# 명령줄 인수를 사용하지 않는다는 것을 안다면 QApplication([])도 작동합니다.
app = QApplication(sys.argv)

# 창이 될 Qt 위젯을 만듭니다.
window = QWidget()

# 중요!!!!!! Windows는 기본적으로 숨겨져 있습니다.
window.show()  

# Start the event loop.
app.exec()