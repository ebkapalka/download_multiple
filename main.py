from threading import Thread, Lock
from typing import List
from queue import Queue
from time import time
import youtube_dl
import time


options = {}
counter = 0
thread_time = 0.0


class FakeLogger(object):
    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        pass


class DownloadWorker(Thread):
    def __init__(self, queue, lock):
        Thread.__init__(self)
        self.lock = lock
        self.queue = queue

    def run(self):
        while True:
            url = self.queue.get()
            try:
                start_time = time.time()
                file_name = get_video_name(url)
                print(f'    Starting {file_name}')
                failed = download_url(url)
                elapsed = time.time() - start_time
                count = self.update_globals(elapsed)
                elapsed = f'{elapsed / 60:.2f}m'
                if failed:
                    print(f'({elapsed}, {count}/{total_pages}) - '
                          f'Failed to download {file_name}')
                else:
                    print(f'({elapsed}, {count}/{total_pages}) - '
                          f'Downloaded {file_name}')
            finally:
                self.queue.task_done()

    def update_globals(self, seconds) -> int:
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
    # TODO: change bool from "skipped" to "success" for readability
    failures = 0
    while failures < try_count:
        try:
            with youtube_dl.YoutubeDL(options) as ydl:
                ydl.download([url])
                return False
        except Exception as e:
            failures += 1
            print(f'{failures} of {try_count} -- failed to download: {e}')
    return True


def start_downloads(urls: List[str], thread_count=16) -> None:
    """
    Populate queue and start worker threads to download videos
    :param urls: list of URLs to download videos from
    :param thread_count: number of worker threads to use.  Default 8
    :return: None
    """
    queue = Queue()
    lock = Lock()
    for _ in range(thread_count):
        worker = DownloadWorker(queue, lock)
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


def remove_duplicates(seq: any) -> List[any]:
    """
    Fast function to remove duplicates while preserving order
    :param seq: iterable to remove duplicates from
    :return: list of the object type from the iterable
    """
    seen = set()
    seen_add = seen.add
    return [x for x in seq if not (x in seen or seen_add(x))]


if __name__ == '__main__':
    app_start = time.time()
    pages = [
        # put URLs here
    ]
    options = {
        'outtmpl': 'out/%(title)s-%(id)s.%(ext)s',
        'quiet': True,
        'no-warnings': True,
        "logger": FakeLogger()
    }
    pages = remove_duplicates(pages)
    total_pages = len(pages)
    start_downloads(urls=pages)
    app_elapsed = time.time() - app_start
    print(f'Actual Elapsed: {app_elapsed / 60:.2f}m')
    print(f'Thread Elapsed: {thread_time / 60:.2f}m')
