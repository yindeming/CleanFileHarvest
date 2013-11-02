from scrapy.spider import BaseSpider
from filedownload.items import FiledownloadItem

class InstallerSpider(BaseSpider):
    name = "spider"
    allowed_domains = ["softpedia.com"]
    start_urls = (
        'http://win.softpedia.com/',
        )

    def parse(self, response):
        yield FiledownloadItem(
            file_urls=[
               'http://download1us.softpedia.com/dl/1edab48d1e5fa2262a24f8c510428e63/52727aa5/100016875/software/security/stpsinst.exe'
            ]
        )
