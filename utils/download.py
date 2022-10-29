from utils.fakelogger import FakeLogger
from threading import Thread, Lock
from typing import List
from queue import Queue
import youtube_dl
import time
import os


options = {}
counter = 0
thread_time = 0.0
total_pages = 0


class DownloadWorker(Thread):
    def __init__(self, queue, lock):
        Thread.__init__(self)
        self.lock = lock
        self.queue = queue

    def run(self):
        """
        Iterate through queue to retrieve and download URLs
        :return: None
        """
        while True:
            url = self.queue.get()
            try:
                start_time = time.time()
                file_name = get_video_name(url)
                print(f'    Starting {file_name.strip()}')
                success = download_url(url)
                elapsed = time.time() - start_time
                count = self.update_globals(elapsed)
                elapsed = f'{elapsed / 60:.2f}m'
                if not success:
                    print(f'({elapsed}, {count}/{total_pages}) - '
                          f'Failed to download {file_name}')
                else:
                    print(f'({elapsed}, {count}/{total_pages}) - '
                          f'Downloaded {file_name}')
            finally:
                self.queue.task_done()

    def update_globals(self, seconds) -> int:
        """
        Update shared variables for counter and thread_time
        :param seconds: number of milliseconds to increment thread_time by
        :return: the current count of completed downloads
        """
        global thread_time
        global counter
        self.lock.acquire()

        local_counter = counter
        local_counter += 1
        counter = local_counter

        local_thread_time = thread_time
        local_thread_time += seconds
        thread_time = local_thread_time

        self.lock.release()
        return local_counter


def download_url(url: str, try_count=4) -> bool:
    """
    Download a list of URLs using youtube-dl
    :param url: url to attempt download from
    :param try_count: max number of retries if need-be
    :return: list of URLs that could not have videos downloaded
    """
    failures = 0
    while failures < try_count:
        try:
            with youtube_dl.YoutubeDL(options) as ydl:
                ydl.download([url])
                return True
        except Exception as e:
            failures += 1
            print(f'{failures} of {try_count} '
                  f'-- failed to download: {e}')
    return False


def start_downloads(urls: List[str], thread_count=8, ydl_opts=None) -> float:
    """
    Populate queue and start worker threads to download videos
    :param urls: list of URLs to download videos from
    :param thread_count: number of worker threads to use.  Default 8
    :param ydl_opts: youtube-dl options string
    :return: None
    """
    global options
    global total_pages
    if ydl_opts is not None:
        options = ydl_opts
    total_pages = len(urls)
    queue = Queue()
    lock = Lock()
    for _ in range(thread_count):
        worker = DownloadWorker(queue, lock)
        worker.daemon = True
        worker.start()
    for link in urls:
        queue.put(link)
    queue.join()
    return thread_time


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
        print('Error in get_video_name:', e)
    return f_name


def generate_options(path='out', template='%(title)s-%(id)s.%(ext)s') -> dict:
    path = os.path.join(path, template)
    print(path)
    return {
        'outtmpl': path,
        'quiet': True,
        'no-warnings': True,
        'logger': FakeLogger()
    }
