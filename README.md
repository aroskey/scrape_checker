# 🤖 Robots.txt, Scrape Checker

Legal web scraping checker via robots.txt

## Requirements

- Python 3.x
- No third-party dependencies

## Usage

1. Clone or download the script
2. Run the script:

```bash
python scraper_checker.py
```

3. Enter your target URL when prompted:

```
Enter URL: https://example.com
```

---

## Example Output

**SCRAPING ALLOWED:**

```
SCRAPING IS ALLOWED IN (https://example.com) FOR USER AGENT '*' ✅
```

**SCRAPING NOT ALLOWED:**

```
SCRAPING IS NOT ALLOWED IN (https://example.com) FOR USER AGENT '*' ⛔
```

**ERROR:**

```
HTTP ERROR: 403 ❌
NETWORK ERROR: <urlopen error ...> ❌
```

## Notes

- A `*` user agent applies the check to all bots. Use a specific user agent string (e.g. `"Googlebot"`) to check for a named crawler
- This tool only checks `robots.txt` rules so beware
- Basic HTTP and network errors are now handled gracefully
