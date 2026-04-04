# 🤖 Robots.txt Compliance Checker

A Python utility to check if a URL allows web scraping according to its `robots.txt` file. This tool helps developers ensure compliance with website crawling policies before starting any scraping projects.

## Features

✨ **Core Functionality**
- ✅ Check if a URL allows scraping for a specific user agent
- 📋 Parse and validate `robots.txt` files
- 🚫 Respect crawl delays and scraping restrictions
- 🗺️ Extract sitemap URLs from `robots.txt`
- 🔄 Batch check multiple URLs at once
- 📊 Detailed compliance reporting

**Developer-Friendly**
- 🎯 Simple API for integration into larger projects
- 📝 Verbose output for debugging
- ⚡ Configurable timeouts
- 🔒 SSL certificate handling
- 🛡️ Comprehensive error handling

## Installation

### Prerequisites
- Python 3.6+
- No external dependencies (uses only Python standard library)

### Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/robots-txt-checker.git
cd robots-txt-checker
```

2. No additional installation needed! Just run it:
```bash
python robots_checker.py
```

## Usage

### Interactive Mode

Run the script directly for an interactive prompt:

```bash
python robots_checker.py
```

You'll be prompted to enter:
- **URL**: The website URL to check (e.g., `example.com` or `https://example.com`)
- **User-Agent**: The user agent string (default: `*` for all bots)

**Example Output:**
```
🔍 Robots.txt Compliance Checker
----------------------------------------
Enter URL: github.com
ℹ️  Added https:// prefix: https://github.com
Enter User-Agent (press Enter for '*'): 

✅ SCRAPING IS ALLOWED
   URL: https://github.com
   User-Agent: '*'
   robots.txt: https://github.com/robots.txt
   Crawl Delay: 1 second
   Sitemaps: https://github.com/sitemap.xml
```

### Programmatic Usage

Import and use the functions in your own Python code:

```python
from robots_checker import can_scrape, batch_check

# Check a single URL
result = can_scrape('https://example.com', user_agent='MyBot/1.0', verbose=True)

print(result['can_fetch'])      # True or False
print(result['crawl_delay'])    # Delay in seconds (if any)
print(result['sitemaps'])       # List of sitemap URLs
```

### Batch Check Multiple URLs

```python
from robots_checker import batch_check

urls = [
    'https://example.com',
    'https://github.com',
    'https://stackoverflow.com'
]

results = batch_check(urls, user_agent='MyBot/1.0')

for result in results:
    print(f"{result['url']}: {'✅ Allowed' if result['can_fetch'] else '⛔ Blocked'}")
```

### Function Reference

#### `can_scrape(url, user_agent='*', timeout=10, verbose=True) -> dict`

Check if scraping is allowed for a given URL.

**Parameters:**
- `url` (str): The website URL to check
- `user_agent` (str): User agent string (default: `'*'` - all bots)
- `timeout` (int): Request timeout in seconds (default: `10`)
- `verbose` (bool): Print detailed output (default: `True`)

**Returns:** Dictionary containing:
```python
{
    'url': str,                    # Input URL
    'user_agent': str,             # User agent used
    'robots_url': str,             # robots.txt URL
    'can_fetch': bool,             # Scraping allowed?
    'robots_exists': bool,         # robots.txt exists?
    'status_code': int,            # HTTP status code
    'crawl_delay': float,          # Crawl delay in seconds (if any)
    'sitemaps': list,              # List of sitemap URLs
    'error': str,                  # Error message (if any)
    'message': str                 # Additional info
}
```

#### `batch_check(urls, user_agent='*') -> list`

Check multiple URLs at once with formatted output.

**Parameters:**
- `urls` (list): List of URLs to check
- `user_agent` (str): User agent string (default: `'*'`)

**Returns:** List of result dictionaries (same format as `can_scrape()`)

#### `get_robots_url(url: str) -> str`

Generate the robots.txt URL for a given website URL.

#### `check_robots_txt_exists(robots_url, timeout=10) -> Tuple[bool, Optional[int]]`

Check if robots.txt exists and return its HTTP status code.

## Examples

### Example 1: Check if you can scrape a website

```python
from robots_checker import can_scrape

result = can_scrape('https://example.com', user_agent='GoogleBot')

if result['can_fetch']:
    print(f"✅ You can scrape {result['url']}")
    if result['crawl_delay']:
        print(f"   Respect a {result['crawl_delay']} second delay")
else:
    print(f"⛔ Scraping not allowed for {result['url']}")
```

### Example 2: Batch check and filter results

```python
from robots_checker import batch_check

sites = ['example.com', 'github.com', 'stackoverflow.com']
results = batch_check(sites)

# Only get allowed sites
allowed = [r for r in results if r['can_fetch']]
print(f"Can scrape {len(allowed)}/{len(results)} sites")
```

### Example 3: Extract sitemaps

```python
from robots_checker import can_scrape

result = can_scrape('https://example.com', verbose=False)

if result['sitemaps']:
    print("Sitemaps found:")
    for sitemap in result['sitemaps']:
        print(f"  - {sitemap}")
```

## Output Indicators

| Symbol | Meaning |
|--------|---------|
| ✅ | Scraping is allowed |
| ⛔ | Scraping is not allowed |
| ℹ️ | Information message |
| ⚠️ | Warning message |
| ❌ | Error occurred |

## How It Works

1. **Constructs robots.txt URL** from the input website URL
2. **Checks if robots.txt exists** by sending an HTTP HEAD request
3. **Parses the robots.txt file** using Python's `urllib.robotparser`
4. **Checks permissions** for the specified user agent
5. **Extracts metadata** including crawl delays and sitemaps
6. **Returns detailed results** in a structured dictionary format

## Error Handling

The tool gracefully handles:
- 🌐 Network timeouts and connection errors
- 🔒 SSL/TLS certificate issues
- 📡 HTTP errors (404, 500, etc.)
- ⏱️ Request timeouts
- 🔍 Malformed URLs

## Security Notes

⚠️ **Important:**
- This tool disables SSL certificate verification for better compatibility
- Only check robots.txt for sites you have legitimate reasons to scrape
- Always respect website terms of service
- Never use this tool for malicious purposes

## License

MIT License - see LICENSE file for details

## Disclaimer

This tool is provided for educational and compliance purposes. Users are responsible for:
- Complying with website terms of service
- Respecting robots.txt files and crawl delays
- Using this tool ethically and legally
- Following applicable laws and regulations
