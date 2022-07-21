from utils.download import start_downloads, generate_options
from utils.general import remove_duplicates
import time


if __name__ == '__main__':
    app_start = time.time()
    pages = [
        # put URLs here
    ]
    options = generate_options('out')
    pages = remove_duplicates(pages)
    thread_time = start_downloads(urls=pages,
                                  thread_count=24,
                                  ydl_opts=options)
