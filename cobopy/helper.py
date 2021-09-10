import sqlite3
from re import escape
from logzero import logger
from cobopy import telegram
from os import getenv


class ComicSite:
    def __init__(self, name, url):
        db = get_db()

        self.name = name
        self.url = url
        self.setup_comic_db(db)
        self.comic_site_id = self.get_comic_site_id(db)

        db.close()

    def setup_comic_db(self, database: sqlite3.Connection):
        c = database.cursor()
        c.execute('''
        INSERT or IGNORE into comic_sites(name, url)
        VALUES (?, ?)
        ''', (self.name,
              self.url))
        database.commit()

    def get_comic_site_id(self, database: sqlite3.Connection):
        c = database.cursor()
        c.execute('''
        SELECT comic_site_id
        FROM comic_sites
        WHERE name is ?
        ''', (self.name,))
        comic_site_id = c.fetchone()
        if comic_site_id is not None:
            return comic_site_id[0]

    def parse_comics(self, soup, db):
        """
        Get's dynamically expanded via function calls see comics.py.

        Takes parsed BeautifulSoup and SQLite Connection, finds comics in soup and
        checks against Database (Send notification for new ones and save them, skip old ones)
        :param soup:
        :param db:
        :return:
        """
        pass


class Comic:
    def __init__(self, title, source, comic_site: ComicSite, db):
        self.title = title
        self.source = source
        self.comic_site = comic_site
        self.save_to_db(db)
        self.comic_id = self.get_comic_id(db)

    def save_to_db(self, database: sqlite3.Connection):
        c = database.cursor()
        logger.debug("%s: Checking if Comic '%s' already exists in database." % (self.comic_site.name, self.title))
        if self.get_comic_id(database) is None:
            # Comic not found in DB, saving it...
            logger.info("%s: Comic not found in database. Saving Comic '%s' ..." % (self.comic_site.name, self.title))
            c.execute('''
                INSERT or IGNORE into comics(title, source, comic_site_id)
                VALUES (?, ?, ?)
            ''', (self.title,
                  self.source,
                  self.comic_site.comic_site_id))

            try:
                resp = telegram.send_photo(
                    bot_id=getenv('BOT_ID'),
                    bot_token=getenv('BOT_TOKEN'),
                    chat_id=getenv('CHAT_ID'),
                    photo=self.source,
                    caption="*Title:* %s\n*Site:* %s" % (escape(self.title), escape(self.comic_site.name))
                )
                if resp.status_code == 200:
                    logger.info("Successfully sent telegram notification for Comic '%s: %s'!" % (
                        self.comic_site.name, self.title))
                    c.execute('''
                        INSERT into telegram_notifications(sent_bool, comic_id)
                        VALUES (?, ?)
                    ''', (1, self.get_comic_id(database)))
                    database.commit()
                else:
                    logger.error("Error while sending telegram notification for Comic '%s: %s': %s" % (
                        self.comic_site.name, self.title, resp.content))
                    database.rollback()
            except Exception as e:
                logger.error("Error while sending telegram notification for Comic '%s: %s': %s" % (
                    self.comic_site.name, self.title, e))
                database.rollback()
        else:
            logger.debug("%s: Comic '%s' already in database. Skipping..." % (self.comic_site.name, self.title))

    def get_comic_id(self, database: sqlite3.Connection):
        c = database.cursor()
        logger.debug("Source: %s" % self.source)
        c.execute('''
               SELECT comic_id FROM comics WHERE source is ?
           ''', (self.source,))
        try:
            return c.fetchone()[0]
        except TypeError:
            return None


def get_db():
    return sqlite3.connect(getenv('SQLITE_DB'))


def setup_db():
    database = get_db()
    logger.debug("Setting up database.")
    c = database.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS comic_sites(
        comic_site_id integer PRIMARY KEY,
        name text NOT NULL UNIQUE,
        url text NOT NULL
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS comics(
        comic_id integer PRIMARY KEY,
        title text NOT NULL UNIQUE,
        source text NOT NULL,
        comic_site_id integer NOT NULL,
        FOREIGN KEY (comic_site_id)
            REFERENCES comic_sites (comic_site_id)
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS telegram_notifications(
        telegram_notification_id integer PRIMARY KEY,
        sent_bool boolean NOT NULL CHECK (sent_bool IN (0,1)),
        comic_id integer NOT NULL,
        FOREIGN KEY (comic_id)
            REFERENCES comics (comic_id)
        )
    ''')
    database.commit()
    database.close()
