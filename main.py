from utils.download import start_downloads
from utils.general import remove_duplicates
from utils.fakelogger import FakeLogger
import time

options = {
    'outtmpl': 'out/%(title)s-%(id)s.%(ext)s',
    'quiet': True,
    'no-warnings': True,
    "logger": FakeLogger()
}

if __name__ == '__main__':
    app_start = time.time()
    pages = [
        # put URLs here
    ]
    pages = remove_duplicates(pages)
    thread_time = start_downloads(urls=pages,
                                  thread_count=16,
                                  ydl_opts=options)
    app_elapsed = time.time() - app_start
    print(f'Actual Elapsed: {app_elapsed / 60:.2f}m')
    print(f'Thread Elapsed: {thread_time / 60:.2f}m')
