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

## Using the Installer Pipeline

1. In the Spider, we scrape an item and put the URLs of its installers into a `installer_urls` field.
2. The item is returned from the spider and goes to the item pipeline.
3. When the item reaches the InstallersPipeline, the URLs in the `installer_urls` field are scheduled for download using the standard Scrapy scheduler and downloader (which means the scheduler and downloader middlewares are reused), but with a higher priority, processing them before other pages are scraped. The item remains “locked” at that particular pipeline stage until the installers have finish downloading (or fail for some reason).
4. When the installers are downloaded another field (installers) will be populated with the results. This field will contain a list of dicts with information about the installers downloaded, such as the downloaded path, the original scraped url (taken from the `installer_urls` field) , and the installer checksum. The installers in the list of the installers field will retain the same order of the original `installer_urls` field. If some installer failed downloading, an error will be logged and the installer won’t be present in the installers field.

## Usage

```
scrapy crawl mycrawler
```

## Reference

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
