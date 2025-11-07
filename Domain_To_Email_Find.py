#!/usr/bin/env python3
# encoding: UTF-8

"""
    Domain To Email Finder
    Extract email addresses from domains using search engines
    Developed by chowdhuryvai
"""

import argparse
import sys
import time
import requests
import re
import os
import validators
from termcolor import colored

try:
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse

# Initialize colorama for Windows
if sys.platform == 'win32':
    try:
        import colorama
        colorama.init()
    except ImportError:
        pass

class EmailParser:
    def __init__(self):
        self.temp = []
        
    def extract(self, results, domain):
        self.results = results
        self.domain = domain

    def clean_results(self):
        # Remove HTML tags and special characters
        for tag in ['<', '>', '/', '\\', ';', ':', '=', '&', '%']:
            self.results = self.results.replace(tag, ' ')
        
    def find_emails(self):
        self.clean_results()
        # Improved email regex pattern
        email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]*' + re.escape(self.domain)
        self.temp = re.findall(email_pattern, self.results)
        return list(set(self.temp))

class SearchEngine:
    def __init__(self, user_agent, proxy=None):
        self.user_agent = user_agent
        self.proxy = proxy
        self.parser = EmailParser()
        
    def google_search(self, domain, limit):
        print(colored("[1] Searching Google...", 'yellow'))
        emails = []
        try:
            for start in range(0, min(limit, 100), 10):
                url = f"https://www.google.com/search?q=%40{domain}&start={start}"
                headers = {'User-Agent': self.user_agent}
                
                proxies = None
                if self.proxy:
                    proxies = {self.proxy.scheme: f"http://{self.proxy.netloc}"}
                
                response = requests.get(url, headers=headers, proxies=proxies, timeout=15)
                
                if response.status_code == 200:
                    self.parser.extract(response.text, domain)
                    found_emails = self.parser.find_emails()
                    emails.extend(found_emails)
                    print(colored(f"[1] Google: Found {len(found_emails)} emails", 'green'))
                
                time.sleep(2)  # Respect rate limits
                
        except Exception as e:
            print(colored(f"[1] Google error: {str(e)}", 'red'))
            
        return list(set(emails))
    
    def bing_search(self, domain, limit):
        print(colored("[2] Searching Bing...", 'yellow'))
        emails = []
        try:
            for offset in range(0, min(limit, 50), 10):
                url = f"https://www.bing.com/search?q=%40{domain}&first={offset}"
                headers = {'User-Agent': self.user_agent}
                
                proxies = None
                if self.proxy:
                    proxies = {self.proxy.scheme: f"http://{self.proxy.netloc}"}
                
                response = requests.get(url, headers=headers, proxies=proxies, timeout=15)
                
                if response.status_code == 200:
                    self.parser.extract(response.text, domain)
                    found_emails = self.parser.find_emails()
                    emails.extend(found_emails)
                    print(colored(f"[2] Bing: Found {len(found_emails)} emails", 'green'))
                
                time.sleep(1)
                
        except Exception as e:
            print(colored(f"[2] Bing error: {str(e)}", 'red'))
            
        return list(set(emails))
    
    def baidu_search(self, domain, limit):
        print(colored("[3] Searching Baidu...", 'yellow'))
        emails = []
        try:
            url = f"https://www.baidu.com/s?wd=%40{domain}"
            headers = {'User-Agent': self.user_agent}
            
            proxies = None
            if self.proxy:
                proxies = {self.proxy.scheme: f"http://{self.proxy.netloc}"}
            
            response = requests.get(url, headers=headers, proxies=proxies, timeout=15)
            
            if response.status_code == 200:
                self.parser.extract(response.text, domain)
                found_emails = self.parser.find_emails()
                emails.extend(found_emails)
                print(colored(f"[3] Baidu: Found {len(found_emails)} emails", 'green'))
            
            time.sleep(1)
                
        except Exception as e:
            print(colored(f"[3] Baidu error: {str(e)}", 'red'))
            
        return list(set(emails))
    
    def duckduckgo_search(self, domain, limit):
        print(colored("[4] Searching DuckDuckGo...", 'yellow'))
        emails = []
        try:
            url = f"https://html.duckduckgo.com/html/?q=%40{domain}"
            headers = {'User-Agent': self.user_agent}
            
            proxies = None
            if self.proxy:
                proxies = {self.proxy.scheme: f"http://{self.proxy.netloc}"}
            
            response = requests.get(url, headers=headers, proxies=proxies, timeout=15)
            
            if response.status_code == 200:
                self.parser.extract(response.text, domain)
                found_emails = self.parser.find_emails()
                emails.extend(found_emails)
                print(colored(f"[4] DuckDuckGo: Found {len(found_emails)} emails", 'green'))
            
            time.sleep(1)
                
        except Exception as e:
            print(colored(f"[4] DuckDuckGo error: {str(e)}", 'red'))
            
        return list(set(emails))

class DomainEmailFinder:
    def __init__(self, user_agent, proxy=None):
        self.user_agent = user_agent
        self.proxy = proxy
        self.searcher = SearchEngine(user_agent, proxy)
        
    def find_all_emails(self, domain, limit):
        all_emails = []
        
        print(colored("\n=== STARTING EMAIL SEARCH ===", 'cyan', attrs=['bold']))
        
        # Search with all engines
        all_emails.extend(self.searcher.google_search(domain, limit))
        all_emails.extend(self.searcher.bing_search(domain, limit))
        all_emails.extend(self.searcher.baidu_search(domain, limit))
        all_emails.extend(self.searcher.duckduckgo_search(domain, limit))
        
        return list(set(all_emails))
    
    def search_with_selection(self, domain, limit, choices):
        all_emails = []
        
        print(colored("\n=== STARTING SELECTED SEARCHES ===", 'cyan', attrs=['bold']))
        
        if '1' in choices:
            all_emails.extend(self.searcher.google_search(domain, limit))
        if '2' in choices:
            all_emails.extend(self.searcher.bing_search(domain, limit))
        if '3' in choices:
            all_emails.extend(self.searcher.baidu_search(domain, limit))
        if '4' in choices:
            all_emails.extend(self.searcher.duckduckgo_search(domain, limit))
        
        return list(set(all_emails))

def print_banner():
    banner = """
╔════════════════════════════════════════════════════════════════╗
║ ██████╗  ██████╗ ███╗   ███╗ █████╗ ██╗███╗   ██╗            ║
║ ██╔══██╗██╔═══██╗████╗ ████║██╔══██╗██║████╗  ██║            ║
║ ██║  ██║██║   ██║██╔████╔██║███████║██║██╔██╗ ██║            ║
║ ██║  ██║██║   ██║██║╚██╔╝██║██╔══██║██║██║╚██╗██║            ║
║ ██████╔╝╚██████╔╝██║ ╚═╝ ██║██║  ██║██║██║ ╚████║            ║
║ ╚═════╝  ╚═════╝ ╚═╝     ╚═╝╚═╝  ╚═╝╚═╝╚═╝  ╚═══╝            ║
║                                                                ║
║              DOMAIN TO EMAIL FINDER v2.0                      ║
║                  Developed by chowdhuryvai                    ║
╚════════════════════════════════════════════════════════════════╝
    """
    print(colored(banner, 'magenta'))
    print(colored("Contact Info:", 'yellow'))
    print(colored("Telegram: https://t.me/darkvaiadmin", 'cyan'))
    print(colored("Channel: https://t.me/windowspremiumkey", 'cyan'))
    print(colored("Website: https://crackyworld.com/", 'cyan'))
    print(colored("=" * 60, 'green'))

def main():
    print_banner()
    
    # Get domain input
    domain = input(colored("\n[?] Enter target domain (e.g., google.com): ", 'yellow')).strip()
    
    if not domain:
        print(colored("[-] Domain is required!", 'red'))
        return
    
    # Validate domain
    try:
        if not validators.domain(domain):
            print(colored("[-] Invalid domain format!", 'red'))
            return
    except:
        # If validators not available, basic check
        if '.' not in domain or len(domain) < 4:
            print(colored("[-] Invalid domain format!", 'red'))
            return
    
    # Get search limit
    try:
        limit = int(input(colored("[?] Enter search limit (default 50): ", 'yellow')) or "50")
    except:
        limit = 50
    
    # Select search engines
    print(colored("\n[?] Select search engines:", 'yellow'))
    print(colored("1. Google", 'cyan'))
    print(colored("2. Bing", 'cyan'))
    print(colored("3. Baidu", 'cyan'))
    print(colored("4. DuckDuckGo", 'cyan'))
    print(colored("5. All engines", 'cyan'))
    
    choice = input(colored("\n[?] Enter your choice (1,2,3,4,5 or multiple like 1,3): ", 'yellow')).strip()
    
    if not choice:
        print(colored("[-] Please select at least one search engine!", 'red'))
        return
    
    # Setup user agent and proxy
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    
    # Proxy configuration
    proxy_input = input(colored("[?] Enter proxy (optional, e.g., http://127.0.0.1:8080): ", 'yellow')).strip()
    proxy = None
    if proxy_input:
        try:
            proxy = urlparse(proxy_input)
            if proxy.scheme not in ('http', 'https') or not proxy.netloc:
                print(colored("[-] Invalid proxy format!", 'red'))
                return
        except:
            print(colored("[-] Invalid proxy format!", 'red'))
            return
    
    # Output file
    save_file = input(colored("[?] Save results to file (optional, enter filename): ", 'yellow')).strip()
    
    # Initialize finder
    finder = DomainEmailFinder(user_agent, proxy)
    
    # Perform search based on selection
    if choice == '5':
        emails = finder.find_all_emails(domain, limit)
    else:
        choices = [c.strip() for c in choice.split(',')]
        valid_choices = ['1', '2', '3', '4']
        if not all(c in valid_choices for c in choices):
            print(colored("[-] Invalid choice! Please select from 1,2,3,4", 'red'))
            return
        emails = finder.search_with_selection(domain, limit, choices)
    
    # Display results
    print(colored("\n" + "="*60, 'green'))
    print(colored(f"📧 SEARCH RESULTS FOR: {domain}", 'magenta', attrs=['bold']))
    print(colored("="*60, 'green'))
    
    if not emails:
        print(colored("[-] No email addresses found!", 'red'))
        return
    
    print(colored(f"[+] Found {len(emails)} unique email addresses:", 'green'))
    print()
    
    for i, email in enumerate(emails, 1):
        print(colored(f"{i:2d}. {email}", 'cyan'))
    
    # Save to file if requested
    if save_file:
        try:
            if not save_file.endswith('.txt'):
                save_file += '.txt'
            
            with open(save_file, 'w', encoding='utf-8') as f:
                f.write(f"Domain Email Finder Results\n")
                f.write(f"Target Domain: {domain}\n")
                f.write(f"Search Date: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"Total Emails Found: {len(emails)}\n")
                f.write("="*50 + "\n\n")
                
                for email in emails:
                    f.write(email + "\n")
            
            print(colored(f"\n[+] Results saved to: {save_file}", 'green'))
            
        except Exception as e:
            print(colored(f"[-] Error saving file: {str(e)}", 'red'))
    
    print(colored("\n[+] Search completed successfully!", 'green', attrs=['bold']))

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print(colored("\n[!] Process interrupted by user", 'yellow'))
    except Exception as e:
        print(colored(f"\n[-] Unexpected error: {str(e)}", 'red'))
