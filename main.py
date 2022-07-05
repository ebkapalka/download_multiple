from threading import Thread
from typing import List
from queue import Queue
from time import time
import youtube_dl
import time


options = {}


class DownloadWorker(Thread):
    def __init__(self, queue):
        Thread.__init__(self)
        self.queue = queue

    def run(self):
        while True:
            url = self.queue.get()
            try:
                start_time = time.time()
                file_name = get_video_name(url)
                failed = download_url(url)
                elapsed = time.time() - start_time
                elapsed = f'{elapsed / 60:.2f}m'
                if failed:
                    print(f'({elapsed}) - Failed to download {file_name}')
                else:
                    print(f'({elapsed}) - Downloaded {file_name}')
            finally:
                self.queue.task_done()


def download_url(url: str, tc=2) -> bool:
    """
    Download a list of URLs using youtube-dl
    :param url: url to attempt download from
    :param tc: max number of retries if need-be
    :return: list of URLs that could not have videos downloaded
    """
    skipped = True
    try_count = int(tc)
    while try_count > 0:
        try:
            with youtube_dl.YoutubeDL(options) as ydl:
                ydl.download([url])
                skipped = False
                break
        except Exception as e:
            print(e, 'Exception in download_url')
            print(f'{try_count}/{tc} -- failed to download')
            try_count -= 1
    return skipped


def start_downloads(urls: List[str], thread_count=8) -> None:
    """
    Populate queue and start worker threads to download videos
    :param urls: list of URLs to download videos from
    :param thread_count: number of worker threads to use.  Default 8
    :return: None
    """
    queue = Queue()
    for _ in range(thread_count):
        worker = DownloadWorker(queue)
        worker.daemon = True
        worker.start()
    for link in urls:
        queue.put(link)
    queue.join()


def get_video_name(url: str) -> str:
    """
    Retrieve name of video to be downloaded
    :param url: url of video to get name of
    :return: name of video OR original URL
    """
    f_name = url
    try:
        with youtube_dl.YoutubeDL(options) as ydl:
            info = ydl.extract_info(url, download=False)
            f_name = ydl.prepare_filename(info)
    except Exception as e:
        print(e)
    return f_name


if __name__ == '__main__':
    app_start = time.time()
    pages = [
        # put URLs here
    ]
    options = {
        'outtmpl': 'out/%(title)s-%(id)s.%(ext)s',
        'quiet': True
    }
    start_downloads(urls=pages)
    app_elapsed = time.time() - app_start
    print(f'Elapsed: {app_elapsed / 60:.2f}m')
