import cv2
import os
from multiprocessing import Process, Queue, cpu_count
import time


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
        print(f"남은 이미지 수: {task_queue.qsize()}")
    
    video.release()
    return

if __name__ == "__main__":

    # 동영상 파일 열기
    
    video_path = "./videos/video.mp4"
    save_path = "./images/"
    save_name = "test"
    video = cv2.VideoCapture(video_path)

    if not video.isOpened():
        print("동영상 파일을 열 수 없습니다.")
        exit(0)

    fps = round(video.get(cv2.CAP_PROP_FPS))
    length = round(int(video.get(cv2.CAP_PROP_FRAME_COUNT)))
    video.release()

    # {slice_per_second} 초에 한 장씩 저장
    slice_per_second = 10
    slice_per_frame = fps * slice_per_second
    total_image_count = length // slice_per_frame

    # 공유 Queue
    task_queue = Queue()

    # 작업 할 프레임 번호를 Queue에 넣기
    for i in range(1, length + 1):
        if i % slice_per_frame == 0:
            task_queue.put(i)

    print(f"생성 될 이미지 개수: {task_queue.qsize()}")

    isReady = input("시작? (y/n): ")
    if isReady != "y":
        print("종료")
        exit(0)
    st = time.time()


    # 프로세스 수
    num_proc = cpu_count()
    proc = []

    # 프로세스 생성
    for i in range(num_proc):
        p = Process(target=slice_video, args=(task_queue, video_path, save_path, save_name))
        p.start()
        proc.append(p)

    # 프로세스가 종료될 때까지 대기
    for p in proc:
        p.join()

    print(f"소요 시간: {round(time.time() - st)}초")
    print("동영상 이미지 추출 완료")
    exit(0)
