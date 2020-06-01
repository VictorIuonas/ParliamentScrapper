from scrapy import cmdline

from runner.downloader import spanish_congress_sequential_request_generator, download_files
from runner.output_cleaner import clean_empty_files_from_folder

# crawl_command_pattern = 'scrapy crawl SpiderCDEP -a date={date} -o output/test_output20200416.csv'
crawl_command_pattern = 'scrapy crawl CongresoESSpider'

command = crawl_command_pattern.format(date='20200203')

# clean_empty_files_from_folder('output')

# cmdline.execute(crawl_command_pattern.split())

requests = spanish_congress_sequential_request_generator(30)
download_files(requests)
clean_empty_files_from_folder('output', 250)
