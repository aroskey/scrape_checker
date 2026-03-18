# 🤖 Robots.txt Scrape Checker

legal web scrape script scrape

## Requirements

- Python 3.x
- `beautifulsoup4`

```bash
pip install beautifulsoup4
```

## Usage

1. Clone or download the script
2. Open the file and set your target URL and user agent

```python
websiteUrl = "https://example.com"  # Replace with your target URL
user_agent = "*"                     # Replace with your bot's user agent if needed
```

3. Run the script:

```bash
python scraper_checker.py
```

---

## Example Output

**SCRAPING ALLOWED:**

```
SCRAPING IS ALLOWED IN (https://example.com) FOR USER AGENT '*' ✅
```

**SCRAPING NOT ALLOWED:**

```
SCRAPING IS NOT ALLOWED IN https://example.com FOR USER AGENT '*' ⛔
```

## Notes

- The example URL (`https://fatdevadi.com`) in the script is a placeholder replace it with a valid URL before running it dummie
- A `*` user agent applies the check to all bots Use a specific user agent string (e.g `"Googlebot"`) to check for a named crawler
- This tool only checks `robots.txt` rules soo beware
- To keep your global python clean install dependencies inside python virtual environment 
