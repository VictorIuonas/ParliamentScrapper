from datetime import date, timedelta
from multiprocessing import Pool
from multiprocessing.context import Process
from typing import Generator

from scrapy import cmdline

from runner.output_cleaner import clean_empty_files_from_folder

crawl_command_pattern = 'scrapy crawl SpiderCDEP -a date={date} -o output/vote_details{date}.json'


def generate_date_range(start_date: date, end_date: date) -> Generator[date, None, None]:
    for day_index in range(int ((end_date - start_date).days)):
        yield start_date + timedelta(day_index)


def scrapy_worker(command: str):
    print(f'executing: {command}')
    cmdline.execute(command.split())


# start_date = date(2006, 2, 6)
start_date = date(2020, 2, 1)
end_date = date.today()

all_scrape_commands = [
    crawl_command_pattern.format(date=day.strftime('%Y%m%d'))
    for day in generate_date_range(start_date, end_date)
]

all_commands = list(all_scrape_commands)

processes = []

if __name__ == '__main__':
    with Pool(processes=3) as pool:
        multiple_result = [pool.apply_async(scrapy_worker, (command,)) for command in all_commands]
        print(len(multiple_result))

        for result in multiple_result:
            print(result.get(timeout=50))

#clean_empty_files_from_folder('output')
