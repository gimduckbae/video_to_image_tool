from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QFileDialog, QMessageBox
import sys
import os
import cv2
from pathlib import Path
from multiprocessing import Process, Queue, cpu_count
from pytube import YouTube
from datetime import datetime


# 이미지 분할 작업
def sliceVideo(taskQueue, videoPath, savePath, saveName):
    video = cv2.VideoCapture(videoPath)

    while not taskQueue.empty():
        frameNum = taskQueue.get()
        video.set(cv2.CAP_PROP_POS_FRAMES, frameNum)
        ret, frame = video.read()
        if ret:
            _savePath = str(Path(savePath)) + "/" + saveName + "_" + str(frameNum) + ".jpg"
            cv2.imwrite(_savePath, frame)
    video.release()
    return

class Ui_form(object):
    videoPath = "./videos/"
    videoName = "video.mp4"
    selectedVideo = None

    savePath = os.getcwd() + "\\images"
    saveName = datetime.now().strftime("%Y%m%d_")
    videoCapture = None

    taskQueue = Queue()
    totalFrameLength = 0
    slicePerFrame = 0
    totalImageCount = 0


    def setupUi(self, form):
        form.setObjectName("form")
        form.resize(513, 245)
        font = QtGui.QFont()
        font.setFamily("돋움")
        form.setFont(font)
        form.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.linkEdit = QtWidgets.QLineEdit(parent=form)
        self.linkEdit.setGeometry(QtCore.QRect(110, 60, 291, 22))
        self.linkEdit.setText("")
        self.linkEdit.setObjectName("linkEdit")
        self.label = QtWidgets.QLabel(parent=form)
        self.label.setGeometry(QtCore.QRect(20, 60, 91, 21))
        font = QtGui.QFont()
        font.setFamily("HY중고딕")
        font.setPointSize(11)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.searchBtn = QtWidgets.QPushButton(parent=form)
        self.searchBtn.setGeometry(QtCore.QRect(410, 60, 75, 22))
        font = QtGui.QFont()
        font.setFamily("돋움")
        font.setPointSize(10)
        font.setBold(True)
        font.setItalic(False)
        font.setUnderline(False)
        self.searchBtn.setFont(font)
        self.searchBtn.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.searchBtn.setObjectName("searchBtn")
        self.dirText = QtWidgets.QLabel(parent=form)
        self.dirText.setGeometry(QtCore.QRect(100, 20, 381, 21))
        font = QtGui.QFont()
        font.setFamily("돋움")
        font.setPointSize(9)
        self.dirText.setFont(font)
        self.dirText.setObjectName("dirText")
        self.videoDDL = QtWidgets.QComboBox(parent=form)
        self.videoDDL.setGeometry(QtCore.QRect(20, 100, 381, 22))
        self.videoDDL.setObjectName("videoDDL")
        self.dirBtn = QtWidgets.QPushButton(parent=form)
        self.dirBtn.setGeometry(QtCore.QRect(20, 20, 75, 22))
        font = QtGui.QFont()
        font.setFamily("돋움")
        font.setPointSize(10)
        font.setBold(True)
        font.setItalic(False)
        font.setUnderline(False)
        self.dirBtn.setFont(font)
        self.dirBtn.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.dirBtn.setObjectName("dirBtn")
        self.downloadBtn = QtWidgets.QPushButton(parent=form)
        self.downloadBtn.setGeometry(QtCore.QRect(410, 100, 71, 22))
        font = QtGui.QFont()
        font.setFamily("돋움")
        font.setPointSize(10)
        font.setBold(True)
        font.setItalic(False)
        font.setUnderline(False)
        self.downloadBtn.setFont(font)
        self.downloadBtn.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.downloadBtn.setObjectName("downloadBtn")
        self.slider = QtWidgets.QSlider(parent=form)
        self.slider.setGeometry(QtCore.QRect(20, 190, 381, 31))
        self.slider.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.slider.setObjectName("slider")
        self.startBtn = QtWidgets.QPushButton(parent=form)
        self.startBtn.setGeometry(QtCore.QRect(410, 190, 71, 31))
        font = QtGui.QFont()
        font.setFamily("돋움")
        font.setPointSize(10)
        font.setBold(True)
        font.setItalic(False)
        font.setUnderline(False)
        self.startBtn.setFont(font)
        self.startBtn.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.startBtn.setObjectName("startBtn")
        self.previewText = QtWidgets.QLabel(parent=form)
        self.previewText.setGeometry(QtCore.QRect(20, 150, 381, 20))
        font = QtGui.QFont()
        font.setFamily("돋움")
        font.setPointSize(10)
        self.previewText.setFont(font)
        self.previewText.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.previewText.setObjectName("previewText")
        self.multiDDL = QtWidgets.QComboBox(parent=form)
        self.multiDDL.setGeometry(QtCore.QRect(440, 150, 41, 22))
        self.multiDDL.setObjectName("multiDDL")
        self.label_2 = QtWidgets.QLabel(parent=form)
        self.label_2.setGeometry(QtCore.QRect(410, 150, 31, 21))
        self.label_2.setObjectName("label_2")

        self.dirBtn.clicked.connect(self.dirBtnClicked)
        self.searchBtn.clicked.connect(self.searchBtnClicked)
        self.downloadBtn.clicked.connect(self.downloadBtnClicked)
        self.startBtn.clicked.connect(self.startBtnClicked)
        self.slider.valueChanged.connect(self.sliderChanged)

        # 초기 설정
        self.checkFolderExist()
        self.setWorkerCount()

        self.retranslateUi(form)
        QtCore.QMetaObject.connectSlotsByName(form)

    def retranslateUi(self, form):
        _translate = QtCore.QCoreApplication.translate
        form.setWindowTitle(_translate("form", "Duckbae ImageSet Helper"))
        self.linkEdit.setPlaceholderText(_translate("form", "ex) http://youtube.com/watch?v=2lAe1cqCOXo"))
        self.label.setText(_translate("form", "유튜브 링크:"))
        self.searchBtn.setText(_translate("form", "검색"))
        self.dirText.setText(_translate("form", f"{os.getcwd()}\\images"))
        self.dirBtn.setText(_translate("form", "저장경로"))
        self.downloadBtn.setText(_translate("form", "다운로드"))
        self.startBtn.setText(_translate("form", "작업시작"))
        self.previewText.setText(_translate("form", "총 9999 프레임 중 24 프레임 마다 이미지 추출 => 총 330장"))
        self.label_2.setText(_translate("form", "병렬:"))

    # 폴더 존재 여부 확인 및 생성
    def checkFolderExist(self):
        if not os.path.exists("./images"):
            os.makedirs("./images")
        if not os.path.exists("./videos"):
            os.makedirs("./videos")
        self.savePath = "./images"
        self.dirText.setText(self.savePath)

    # CPU 코어 수에 따라서 병렬 처리 개수 설정
    def setWorkerCount(self):
        self.multiDDL.clear()
        for i in range(cpu_count(), 0, -1):
            self.multiDDL.addItem(str(i))
        self.multiDDL.setCurrentIndex(0)

    # 저장경로 선택
    def dirBtnClicked(self):
        dir_name = QFileDialog.getExistingDirectory(None, "이미지 저장 경로 선택")
        if dir_name:
            path = Path(dir_name)
            self.dirText.setText(str(path))

    # 유튜브 링크로 영상 검색
    def searchBtnClicked(self):
        videoUrl = self.linkEdit.text()
        if videoUrl == "":
            QMessageBox.about(None, "경고", "유튜브 링크를 입력해주세요")
            return
        self.selectedVideo = YouTube(videoUrl)
        _streamList = self.selectedVideo.streams.filter(file_extension="mp4", only_video=True).order_by('resolution').desc()
        self.videoDDL.clear()
        for stream in _streamList:
            self.videoDDL.addItem(str(f"{self.selectedVideo.title} - [{stream.resolution} {stream.fps}FPS]"))

    # DDL 선택 옵션으로 영상 다운로드
    def downloadBtnClicked(self):
        if self.selectedVideo == None:
            QMessageBox.about(None, "경고", "먼저 영상을 검색해주세요")
            return
        _selectedVideo = self.videoDDL.currentIndex()
        _streamList = self.selectedVideo.streams.filter(file_extension="mp4", only_video=True).order_by('resolution').desc()
        _streamList[_selectedVideo].download(output_path=self.videoPath, filename=self.videoName)
        QMessageBox.about(None, "알림", "다운로드 완료")
        self.getVideoInfo()

    # 슬라이더 이벤트
    def sliderChanged(self):
        if self.totalFrameLength == 0:
            return
        else:
            self.slicePerFrame = self.slider.value()
            self.calculateImageCount()

    # 슬라이더 최소, 최대값 설정
    def setSliderLimit(self):
        self.slider.setMinimum(1)
        self.slider.setMaximum(self.totalFrameLength // 10)

    # 동영상 파일 열어서 정보 가져오기
    def getVideoInfo(self):
        self.videoCapture = cv2.VideoCapture(self.videoPath + self.videoName)
        if not self.videoCapture.isOpened():
            QMessageBox.about(None, "경고", "동영상 파일을 열 수 없습니다.")
            return
        self.totalFrameLength = round(int(self.videoCapture.get(cv2.CAP_PROP_FRAME_COUNT)))
        self.videoCapture.release()
        self.setSliderLimit()

    # 이미지 추출 개수 계산
    def calculateImageCount(self):
        self.totalImageCount = self.totalFrameLength // self.slicePerFrame
        self.previewText.setText(f"총 {self.totalFrameLength} 프레임 중 {self.slicePerFrame} 프레임 마다 이미지 추출 => 총 {self.totalImageCount}장")

    # 작업 시작버튼
    def startBtnClicked(self):
        if self.totalFrameLength == 0:
            QMessageBox.about(None, "경고", "먼저 영상을 다운로드 해주세요")
            return
        if self.taskQueue.empty():
            self.createTaskQueue()
        
        # 병렬 처리 개수
        _workerCount = int(self.multiDDL.currentText())
        _processList = []

        # 프로세스 생성
        for i in range(_workerCount):
            p = Process(target=sliceVideo, args=(self.taskQueue, self.videoPath + self.videoName, self.savePath, self.saveName))
            p.start()
            _processList.append(p)

        # 프로세스 종료 대기
        for p in _processList:
            p.join()

        QMessageBox.about(None, "알림", "작업 완료")
        self.reset()

    # 작업관련 필드 초기화
    def reset(self):
        self.taskQueue = Queue()
        self.previewText.setText("추출 완료!")

    # 작업 큐 생성
    def createTaskQueue(self):
        self.taskQueue = Queue()
        for i in range(1, self.totalFrameLength + 1):
            if i % self.slicePerFrame == 0:
                self.taskQueue.put(i)




if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    form = QtWidgets.QWidget()
    ui = Ui_form()
    ui.setupUi(form)
    form.show()
    sys.exit(app.exec())
