import cv2
import os
from multiprocessing import Process, Queue, cpu_count
from datetime import datetime


class Image:
    video_path = ""
    save_path = ""
    video = None
    video_fps = 0
    video_length = 0
    slice_per_second = 5
    slice_per_frame = 0
    total_image_count = 0
    task_queue = Queue()
    worker_count = cpu_count()


    @staticmethod
    def open_video(video_path, save_path="./images/", save_name=datetime.today().strftime("%Y%m%d")):
        Image.video = cv2.VideoCapture(video_path)
        if not Image.video.isOpened():
            Image.video = None
            raise Exception("CANNOT_OPEN_VIDEO")
        return

    @staticmethod
    def check_video_info():
        if not Image.video.isOpened():
            raise Exception("CANNOT_OPEN_VIDEO")
        Image.video_fps = round(Image.video.get(cv2.CAP_PROP_FPS))
        Image.video_length = round(int(Image.video.get(cv2.CAP_PROP_FRAME_COUNT)))
        Image.slice_per_frame = Image.video_fps * Image.slice_per_second
        Image.total_image_count = Image.video_length // Image.slice_per_frame
        Image.video.release()
        return

    @staticmethod
    def auto_cal():
        Image.slice_per_frame = Image.video_fps * Image.slice_per_second
        Image.total_image_count = Image.video_length // Image.slice_per_frame
        return

    @staticmethod
    def make_task_queue():
        # 작업 할 프레임 번호를 Queue에 넣기
        for i in range(1, Image.video_length + 1):
            if i % Image.slice_per_frame == 0:
                Image.task_queue.put(i)
        return Image.task_queue.qsize()

    @staticmethod
    def run():
        num_proc = Image.worker_count
        proc = []

        # 프로세스 생성
        for i in range(num_proc):
            p = Process(target=Image.slice_video, args=(Image.task_queue, Image.video_path, Image.save_path, Image.save_name))
            p.start()
            proc.append(p)

        # 프로세스가 종료될 때까지 대기
        for p in proc:
            p.join()

        return

    def slice_video(task_queue, video_path, save_path, save_name):
        video = cv2.VideoCapture(video_path)

        while not task_queue.empty():
            frame_num = task_queue.get()
            video.set(cv2.CAP_PROP_POS_FRAMES, frame_num)
            ret, frame = video.read()
            if ret:
                cv2.imwrite(
                    os.path.join(save_path, save_name + "_" + str(frame_num) + ".jpg"),
                    frame,
                )
            else:
                pass
        
        video.release()
        return