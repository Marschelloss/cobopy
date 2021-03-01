from sqlite3 import Connection
from bs4 import BeautifulSoup
from cobopy import helper
from os import path


def generate_comic_sites():
    comic_sites_list = []

    # ---

    lastplace = helper.ComicSite(name="Last Place Comics",
                                 url="http://feeds.feedburner.com/lastplacecomics/RSS")

    def parse_comics(self, soup: BeautifulSoup, db: Connection):
        for item in soup.find_all("item"):
            _comic = helper.Comic(title=item.find("title").text,
                                  source=item.find("img")['src'],
                                  comic_site=self,
                                  db=db)

    lastplace.parse_comics = parse_comics.__get__(lastplace, helper.ComicSite)
    comic_sites_list.append(lastplace)

    # ---

    exocomics = helper.ComicSite(name="Extra Ordinary",
                                 url="https://www.exocomics.com/feed")

    def parse_comics(self, soup: BeautifulSoup, db: Connection):
        for item in soup.find_all("item"):
            # Some non-magic Magic needed to get real picture url...
            _comic = helper.Comic(title=item.find("title").text,
                                  source="%s/wp-content/uploads/%s.jpg" % (path.dirname(exocomics.url),
                                                                           item.find("title").text),
                                  comic_site=self,
                                  db=db)

    exocomics.parse_comics = parse_comics.__get__(exocomics, helper.ComicSite)
    comic_sites_list.append(exocomics)

    # ---

    mesutkaya = helper.ComicSite(name="Mesut Kaya",
                                 url="https://blog.mesutkaya.com/feed.xml")

    def parse_comics(self, soup: BeautifulSoup, db: Connection):
        for item in soup.find_all("item"):
            # 'Hidden' HTML in Description of Item
            item_soup = BeautifulSoup(item.find('description').contents[0], "lxml")
            _comic = helper.Comic(title=item.find("title").text,
                                  source=item_soup.find('img')['src'],
                                  comic_site=self,
                                  db=db)

    mesutkaya.parse_comics = parse_comics.__get__(mesutkaya, helper.ComicSite)
    comic_sites_list.append(mesutkaya)

    # ---

    mrlovenstein = helper.ComicSite(name="Mr Lovenstein",
                                    url="https://www.mrlovenstein.com/rss.xml")

    def parse_comics(self, soup: BeautifulSoup, db: Connection):
        for item in soup.find_all("item"):
            # 'Hidden' HTML in Description of Item
            item_soup = BeautifulSoup(item.find('description').contents[0], "lxml")
            _comic = helper.Comic(title=item.find("title").text,
                                  source=item_soup.find('img')['src'],
                                  comic_site=self,
                                  db=db)

    mrlovenstein.parse_comics = parse_comics.__get__(mrlovenstein, helper.ComicSite)
    comic_sites_list.append(mrlovenstein)

    # ---

    poorlydrawnlines = helper.ComicSite(name="Poorly Drawn Lines",
                                        url="http://feeds.feedburner.com/PoorlyDrawnLines")

    def parse_comics(self, soup: BeautifulSoup, db: Connection):
        for item in soup.find_all("item"):
            _comic = helper.Comic(title=item.find("title").text,
                                  source=item.find("img")['src'],
                                  comic_site=self,
                                  db=db)

    poorlydrawnlines.parse_comics = parse_comics.__get__(poorlydrawnlines, helper.ComicSite)
    comic_sites_list.append(poorlydrawnlines)

    # ---

    return comic_sites_list
