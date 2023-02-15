from utils.download import start_downloads, generate_options
from utils.general import remove_duplicates
from datetime import datetime, timedelta

def td_hours_minutes(td: timedelta) -> str:
    """
    Convert a timedelta object into hours and minutes
    :param td: timedelta object
    :return: tuple of hours and minutes
    """
    return f"{td.seconds//3600}:{(td.seconds//60)%60}"


if __name__ == '__main__':
    pages = [
        # put URLs here
    ]
    options = generate_options('d:/videos')
    pages = remove_duplicates(pages)
    start_t = datetime.now()
    thread_time = start_downloads(urls=pages,
                                  thread_count=4,
                                  ydl_opts=options)
    end_t = datetime.now()
    elapsed = end_t-start_t
    print("Finished at ", end_t.strftime("%H:%M:%S"))
    print("Elapsed: ", td_hours_minutes(elapsed))
