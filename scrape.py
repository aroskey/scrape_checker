import urllib.robotparser
from urllib.parse import urlparse
from urllib.error import URLError, HTTPError

def get_robots_url(url: str) -> str:
    parsed = urlparse(url)
    return f"{parsed.scheme}://{parsed.netloc}/robots.txt"

def can_scrape(url: str, user_agent: str = "*") -> None:
    robots_url = get_robots_url(url)
    try:
        rp = urllib.robotparser.RobotFileParser()
        rp.set_url(robots_url)
        rp.read()
        allowed = rp.can_fetch(user_agent, url)
        if allowed:
            print(f"SCRAPING IS ALLOWED IN ({url}) FOR USER AGENT '{user_agent}' ✅")
        else:
            print(f"SCRAPING IS NOT ALLOWED IN ({url}) FOR USER AGENT '{user_agent}' ⛔")
    except HTTPError as e:
        print(f"HTTP ERROR: {e.code} ❌")
    except URLError as e:
        print(f"NETWORK ERROR: {e.reason} ❌")

def main() -> None:
    websiteUrl = input("Enter URL: ").strip()
    user_agent = "*"
    can_scrape(websiteUrl, user_agent)

if __name__ == "__main__":
    main()