# cobopy: Your Comic Feed Reader

A simple program to parse multiple comic site's rss feeds and send new comics to a telegram chat of your choice!

---

## Usage

1. Install needed python-libraries (see `requirements.txt`) or use the provided Dockerfile.
2. Set needed environment variables:
    - BOT_ID: ID of your telegram bot
    - BOT_TOKEN: Token of your telegram bot
    - CHAT_ID: ID of your telegram chat
    - SQLITE_DB: Path to your SQLite3 Database
3. Simply run `python3 main.py`.

Currently the telegram bot doesn't listen to any incoming messages nor does the programm loop itself. Simply create a CRON Job, and let it run every hour (don't flood people's rss feeds!).

### Comic Sites

The program is easy to extend: Take a look at `cobopy/comics.py` and see for yourself!

I used some (probably dirty) python code to create for each comic site an Object and a method `parse_comics`. You only need to copy the boilerplate code, create a new object write the needed code and it get's picked up by `cobopy/catcher.py`. 

**Example:**

```python
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
```