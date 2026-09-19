"""
=========================================================
  JASUS PROXY - Multi-Source Elite Proxy Harvester
  Author: EEM
=========================================================
"""

import os
import re
import sys
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed

# Fix Windows console UnicodeEncodeError for emojis
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

SOURCES = [
    # HTTP / HTTPS
    "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt",
    "https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/http.txt",
    "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/http.txt",
    "https://raw.githubusercontent.com/roosterkid/openproxylist/main/HTTPS_RAW.txt",
    "https://raw.githubusercontent.com/sunny9577/proxy-scraper/master/proxies.txt",
    "https://raw.githubusercontent.com/MuRongPIG/Proxy-Master/main/http.txt",
    "https://raw.githubusercontent.com/prxchk/proxy-list/main/http.txt",
    "https://raw.githubusercontent.com/Zaeem20/FREE_PROXIES_LIST/master/http.txt",
    "https://raw.githubusercontent.com/Zaeem20/FREE_PROXIES_LIST/master/https.txt",
    "https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=10000&country=all&ssl=all&anonymity=all",
    
    # SOCKS4
    "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/socks4.txt",
    "https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/socks4.txt",
    "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/socks4.txt",
    "https://raw.githubusercontent.com/roosterkid/openproxylist/main/SOCKS4_RAW.txt",
    "https://raw.githubusercontent.com/MuRongPIG/Proxy-Master/main/socks4.txt",
    "https://raw.githubusercontent.com/prxchk/proxy-list/main/socks4.txt",
    "https://raw.githubusercontent.com/Zaeem20/FREE_PROXIES_LIST/master/socks4.txt",
    "https://api.proxyscrape.com/v2/?request=getproxies&protocol=socks4&timeout=10000&country=all",
    
    # SOCKS5
    "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/socks5.txt",
    "https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/socks5.txt",
    "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/socks5.txt",
    "https://raw.githubusercontent.com/roosterkid/openproxylist/main/SOCKS5_RAW.txt",
    "https://raw.githubusercontent.com/hookzof/socks5_list/master/proxy.txt",
    "https://raw.githubusercontent.com/MuRongPIG/Proxy-Master/main/socks5.txt",
    "https://raw.githubusercontent.com/prxchk/proxy-list/main/socks5.txt",
    "https://raw.githubusercontent.com/Zaeem20/FREE_PROXIES_LIST/master/socks5.txt",
    "https://api.proxyscrape.com/v2/?request=getproxies&protocol=socks5&timeout=10000&country=all"
]

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
}

def fetch_single_source(url, log_func):
    source_name = url.split('/')[3] if 'github' in url else 'ProxyScrape'
    filename = url.split('/')[-1].split('?')[0]
    display_name = f"{source_name} ({filename})"
    try:
        response = requests.get(url, headers=HEADERS, timeout=12)
        if response.status_code == 200:
            found = re.findall(r'\b(?:\d{1,3}\.){3}\d{1,3}:\d{2,5}\b', response.text)
            log_func(f"✅ [{display_name}] Found {len(found)} proxies")
            return found
        else:
            log_func(f"⚠️ [{display_name}] HTTP {response.status_code}")
    except Exception as e:
        log_func(f"❌ [{display_name}] Error: {str(e)[:40]}")
    return []

def fetch_proxies(output_file="raw_proxies.txt", log_callback=None, max_workers=10):
    def log(msg):
        if log_callback:
            log_callback(msg)
        else:
            print(msg)

    log("🕵️‍♂️ Starting Jasus Proxy Harvester... Hunting for elite live sources.")
    
    all_proxies = []
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(fetch_single_source, url, log) for url in SOURCES]
        for future in as_completed(futures):
            try:
                res = future.result()
                if res:
                    all_proxies.extend(res)
            except Exception:
                pass

    # Remove duplicates while preserving format
    unique_proxies = sorted(list(set(all_proxies)))
    
    if output_file:
        with open(output_file, "w", encoding="utf-8") as f:
            f.write("\n".join(unique_proxies))
    
    log("-" * 40)
    log(f"🎉 HARVEST COMPLETE!")
    log(f"🔥 Total unique proxies harvested: {len(unique_proxies):,}")
    if output_file:
        log(f"📁 Saved to: {os.path.abspath(output_file)}")
    log("🚀 Ready to filter live proxies with Jasus Proxy!")
    
    return unique_proxies

if __name__ == "__main__":
    fetch_proxies()
