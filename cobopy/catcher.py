from cobopy import helper, comics
from logzero import logger
from bs4 import BeautifulSoup
import requests


def start():
    comic_sites_list = comics.generate_comic_sites()
    for comic_site in comic_sites_list:
        get(comic_site)


def get(comic_site: helper.ComicSite):
    try:
        r = requests.get(url=comic_site.url,
                         headers={"User-Agent": "Cobopy"})
        if r.status_code == 200:
            db = helper.get_db()
            soup = BeautifulSoup(r.content, "lxml")
            comic_site.parse_comics(soup, db)
        else:
            logger.error("Status Code for '%s' not 'OK': %s - %s" % (comic_site.url,
                                                                     r.status_code,
                                                                     r.content))
    except requests.exceptions.Timeout as e:
        logger.error("Python-Requests Timeout Error connecting to %s: %s" % (comic_site.url, e))
    except Exception as e:
        logger.error("Unknown Error connecting to %s: %s" % (comic_site.url, e))
