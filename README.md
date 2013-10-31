Crawler
================

## Features
- Maximum crawling depth, pages
- Repects robots.txt
- Able to crawler AJAX pages (crawler-ajax.py)

The overall dataflow for the crawling processing looks like:

![Alt text](architecture-scrapy.png "Architecture")

## Requirements
- Scrapy

- The [FilesPipeline](https://raw.github.com/scrapy/scrapy/master/scrapy/contrib/pipeline/files.py)

1. In the Spider, we scrape an item and put the URLs of its installers into a `file_urls` field.
2. The item is returned from the spider and goes to the item pipeline.
3. When the item reaches the FilesPipeline, the URLs in the `file_urls` field are scheduled for download using the standard Scrapy scheduler and downloader (which means the scheduler and downloader middlewares are reused), but with a higher priority, processing them before other pages are scraped. The item remains “locked” at that particular pipeline stage until the files have finish downloading (or fail for some reason).
4. When the files are downloaded another field (files) will be populated with the results. This field will contain a list of dicts with information about the installers downloaded, such as the downloaded path, the original scraped url (taken from the `file_urls` field) , and the installer checksum. The files in the list of the files field will retain the same order of the original `file_urls` field. If some file failed downloading, an error will be logged and the files won’t be present in the files field.

## Usage

```
scrapy crawl spider
```

## Note

This crawler is a modification of [Scrapy 1.8.4](http://www.scrapy.org/).

Auto
================

## Requirements
- Python v2.7+
- vmauto.py
- [Python for Windows extensions](http://sourceforge.net/projects/pywin32/)

## Usage

```
python auto.py filename.exe
```

## Reference

The automation is based on [Simon Brunning's winGuiAuto.py](http://www.brunningonline.net/simon/blog/archives/winGuiAuto.py.html)
