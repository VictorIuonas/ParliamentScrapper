from scrapy import cmdline

crawl_command_pattern = 'scrapy crawl SpiderCDEP -a date={date}'

command = crawl_command_pattern.format(date='20200513')

cmdline.execute(command.split())
# cmdline.execute('scrapy crawl SpiderCDEP -a date=20200513'.split())
