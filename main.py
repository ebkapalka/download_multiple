from typing import List, Optional
import youtube_dl
import pprint
import time


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
        'outtmpl': 'out/%(title)s-%(id)s.%(ext)s'
    }
    download_urls(pages, options)
    app_elapsed = time.time() - app_start
    print(f'Elapsed: {app_elapsed / 60:.2f}m')
