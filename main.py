from typing import List
import youtube_dl
import pprint


def download_urls(urls: List[str]) -> List[str]:
    """
    Download a list of URLs using youtube-dl
    :param urls: list of URLs (strings)
    :return: list of URLs that could not have videos downloaded
    """
    ydl_opts = {}
    skipped = []
    for index, page in enumerate(urls):
        try:
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                ydl.download([page])
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
    pages = [
        # put URLs here
    ]
    download_urls(pages)
