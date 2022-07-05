from typing import List, Optional
from threading import Thread
from queue import Queue
from time import time
import youtube_dl
import pprint
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


def download_url(url: str, try_count=2) -> bool:
    """
    Download a list of URLs using youtube-dl
    :param url: url to attempt download from
    :param try_count: max number of retries if need-be
    :return: list of URLs that could not have videos downloaded
    """
    skipped = True
    while try_count > 0:
        try:
            with youtube_dl.YoutubeDL(options) as ydl:
                ydl.download([url])
                skipped = False
                break
        except Exception as e:
            try_count -= 1
    return skipped


def start_downloads(urls: List[str], thread_count=8):
    """

    :param urls:
    :param thread_count:
    :return:
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

    :param url:
    :return:
    """
    f_name = url
    try:
        with youtube_dl.YoutubeDL(options) as ydl:
            info = ydl.extract_info(url, download=False)
            f_name = ydl.prepare_filename(info)
    except Exception as e:
        print(e)
    return f_name


def download_urls(urls: List[str], ydl_opts: Optional = None) -> List[str]:
    """
    Download a list of URLs using youtube-dl
    :param urls: list of URLs (strings)
    :param ydl_opts: dictionary of youtube-dl parameters / options
    :return: list of URLs that could not have videos downloaded
    """
    if not ydl_opts:
        ydl_opts = {}
    skipped = []
    for index, page in enumerate(urls):
        start_time = time.time()
        try:
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                ydl.download([page])
                elapsed = time.time() - start_time
                print(f'Elapsed: {elapsed / 60:.2f}m')
        except Exception as e:
            print(f'Exception: {e}')
            print('Failed, retrying one more time')
            try:
                with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([page])
            except Exception as e:
                print(f'Exception: {e}')
                print(f'Failed twice, skipping {page}')
                skipped.append(page)
        print(f'Completed {index - len(skipped) + 1}/{len(urls)}')
    if skipped:
        print(f'Failed to download {len(skipped)} videos:')
        pprint.pprint(skipped)
    return skipped


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
