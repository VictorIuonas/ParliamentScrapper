from scrapy import cmdline

from runner.output_cleaner import clean_empty_files_from_folder

crawl_command_pattern = 'scrapy crawl SpiderCDEP -a date={date} -o output/test_output20200416.csv'

command = crawl_command_pattern.format(date='20200416')

clean_empty_files_from_folder('output')

# cmdline.execute(command.split())
