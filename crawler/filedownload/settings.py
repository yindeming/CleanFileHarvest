# Scrapy settings for filedownload project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'filedownload'

SPIDER_MODULES = ['filedownload.spiders']
NEWSPIDER_MODULE = 'filedownload.spiders'

ITEM_PIPELINES = [
    'filedownload.files.FilesPipeline',
]
FILES_STORE = '/home/test/filedownload/downloads'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'filedownload (+http://www.yourdomain.com)'
