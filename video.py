from pytube import YouTube

class Video:
    video = None
    video_stream = None

    @staticmethod
    def get_video_info(url):
        Video.video = YouTube(url)
        Video.video_stream = Video.video.streams.filter(file_extension="mp4", only_video=True).order_by('resolution').desc()
        return Video.video_stream

    @staticmethod
    def download_video(index):
        if Video.video_stream == []:
            raise Exception("EMPTY_VIDEO_STREAMS")
        Video.video_stream[index].download(output_path="./videos/", filename="video.mp4")
        return True
