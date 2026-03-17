import urllib.robotparser
from bs4 import BeautifulSoup

def can_scrape(url: str, user_agent: str = "*") -> bool:
    rp = urllib.robotparser.RobotFileParser()
    rp.set_url(url + "/robots.txt")
    rp.read()
    return rp.can_fetch(user_agent, url)

def main() -> None:
    websiteUrl = "https://github.com" # IT'S JUST EXAMPLE WEBSITE LINK (IT WILL GIVE YOU ERR ENTER THE RIGHT LINK)
    user_agent = "*"
    if can_scrape(websiteUrl, user_agent):
        print(f"SCRAPING IS ALLOWED IN ({websiteUrl}) FOR USER AGENT '{user_agent}' ✅")
    else:
        print(f"SCRAPING IS NOT ALLOWED IN ({websiteUrl}) FOR USER AGENT '{user_agent}' ⛔")

if __name__ == "__main__":
    main()