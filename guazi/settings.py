

BOT_NAME = 'guazi'

SPIDER_MODULES = ['guazi.spiders']
NEWSPIDER_MODULE = 'guazi.spiders'

# HOST = 'your host'
# DATABASE = 'your  database'
# USERNAME = ''
# PASSWORD = ''

ROBOTSTXT_OBEY = False

DOWNLOAD_DELAY = 5

COOKIES_ENABLED = True

DOWNLOADER_MIDDLEWARES = {
   'guazi.middlewares.GuaziDownloaderMiddleware': 500,
}

ITEM_PIPELINES = {
   'guazi.pipelines.GuaziPipeline': 300
}


LOG_FILE = "log.txt"
