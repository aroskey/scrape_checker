import urllib.robotparser
from urllib.parse import urlparse, urljoin
from urllib.error import URLError, HTTPError
from urllib.request import urlopen, Request
import ssl
import socket
from typing import Optional, Tuple


def get_robots_url(url: str) -> str:
    parsed = urlparse(url)
    scheme = parsed.scheme if parsed.scheme else 'https'
    netloc = parsed.netloc if parsed.netloc else parsed.path.split('/')[0]
    return f"{scheme}://{netloc}/robots.txt"


def check_robots_txt_exists(robots_url: str, timeout: int = 10) -> Tuple[bool, Optional[int]]:
    try:
        ssl_context = ssl.create_default_context()
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE

        req = Request(
            robots_url,
            headers={
                'User-Agent': 'RobotsChecker/1.0 (Compliance Check Bot)',
                'Accept': '*/*',
                'Accept-Encoding': 'identity',
            }
        )

        with urlopen(req, timeout=timeout, context=ssl_context) as response:
            return True, response.status

    except HTTPError as e:
        if e.code == 404:
            return False, 404
        return False, e.code
    except Exception:
        return False, None


def can_scrape(
    url: str, 
    user_agent: str = "*",
    timeout: int = 10,
    verbose: bool = True
) -> dict:
    result = {
        'url': url,
        'user_agent': user_agent,
        'robots_url': get_robots_url(url),
        'can_fetch': False,
        'robots_exists': False,
        'status_code': None,
        'crawl_delay': None,
        'error': None,
        'sitemaps': []
    }
    
    robots_url = result['robots_url']
    
    exists, status = check_robots_txt_exists(robots_url, timeout)
    result['robots_exists'] = exists
    result['status_code'] = status
    
    if status == 404:
        result['can_fetch'] = True
        result['message'] = "No robots.txt found - scraping allowed by default"
        if verbose:
            print(f"ℹ️  No robots.txt found at {robots_url}")
            print(f"✅ SCRAPING IS ALLOWED (no restrictions found)")
        return result
    
    if not exists and status is not None:
        result['error'] = f"robots.txt returned status {status}"
        if verbose:
            print(f"⚠️  robots.txt returned status {status}")
        return result
    
    try:
        rp = urllib.robotparser.RobotFileParser()
        rp.set_url(robots_url)
        
        ssl_context = ssl.create_default_context()
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE
        
        rp.read()
        
        result['can_fetch'] = rp.can_fetch(user_agent, url)
        
        try:
            result['crawl_delay'] = rp.crawl_delay(user_agent)
        except Exception:
            pass
        
        try:
            result['sitemaps'] = rp.site_maps() or []
        except Exception:
            pass
        
        if verbose:
            status_emoji = "✅" if result['can_fetch'] else "⛔"
            status_text = "ALLOWED" if result['can_fetch'] else "NOT ALLOWED"
            print(f"{status_emoji} SCRAPING IS {status_text}")
            print(f"   URL: {url}")
            print(f"   User-Agent: '{user_agent}'")
            print(f"   robots.txt: {robots_url}")
            
            if result['crawl_delay']:
                print(f"   Crawl Delay: {result['crawl_delay']} seconds")
            if result['sitemaps']:
                print(f"   Sitemaps: {', '.join(result['sitemaps'][:3])}")
                
    except HTTPError as e:
        result['error'] = f"HTTP {e.code}: {e.reason}"
        if verbose:
            print(f"❌ HTTP ERROR: {e.code} - {e.reason}")
    except URLError as e:
        result['error'] = f"Network error: {e.reason}"
        if verbose:
            print(f"❌ NETWORK ERROR: {e.reason}")
    except socket.timeout:
        result['error'] = "Connection timeout"
        if verbose:
            print(f"❌ TIMEOUT: Connection to {robots_url} timed out")
    except Exception as e:
        result['error'] = str(e)
        if verbose:
            print(f"❌ ERROR: {e}")
    
    return result


def batch_check(urls: list, user_agent: str = "*") -> list:
    results = []
    print(f"\n{'='*60}")
    print(f"BATCH CHECK: {len(urls)} URLs")
    print(f"{'='*60}\n")
    
    for i, url in enumerate(urls, 1):
        print(f"[{i}/{len(urls)}] Checking: {url}")
        result = can_scrape(url, user_agent, verbose=True)
        results.append(result)
        print()
    
    allowed = sum(1 for r in results if r['can_fetch'])
    print(f"{'='*60}")
    print(f"SUMMARY: {allowed}/{len(urls)} URLs allowed")
    print(f"{'='*60}")
    
    return results


def main():
    print("🔍 Robots.txt Compliance Checker")
    print("-" * 40)
    
    website_url = input("Enter URL: ").strip()
    
    if not website_url:
        print("❌ No URL provided")
        return
    
    if not website_url.startswith(('http://', 'https://')):
        website_url = 'https://' + website_url
        print(f"ℹ️  Added https:// prefix: {website_url}")
    
    user_agent = input("Enter User-Agent (press Enter for '*'): ").strip()
    if not user_agent:
        user_agent = "*"
    
    print()
    can_scrape(website_url, user_agent)


if __name__ == "__main__":
    main()
