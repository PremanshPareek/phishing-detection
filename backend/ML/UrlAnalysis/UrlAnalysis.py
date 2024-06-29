import pickle
import re
import whois
from datetime import datetime
import requests
import random
from bs4 import BeautifulSoup
import requests
from urllib.parse import urlparse, urlsplit

class UrlAnalysis:
    def __init__(self) -> None:
        with open('model_random_forest.pkl', 'rb') as file:
            self.rf_model = pickle.load(file)
        
    
    def is_phishing(self, url: str) -> bool:
        # check if the mail is phishing
        
        def length_url(url: str) -> int:
            """
            Calculate the length of the URL.
            
            Parameters:
            url (str): The URL to be analyzed.
            
            Returns:
            int: The length of the URL.
            """
            return len(url)


        def length_hostname(url: str) -> int:
            """
            Calculate the length of the hostname of a given URL.
            
            Parameters:
            url (str): The URL to be analyzed.
            
            Returns:
            int: The length of the hostname.
            """
            hostname = urlparse(url).hostname
            return len(hostname) if hostname else 0

        def ip(url: str) -> int:
            """
            Check if the URL uses an IP address instead of a domain name.
            
            Parameters:
            url (str): The URL to be checked.
            
            Returns:
            int: 1 if the URL uses an IP address, 0 otherwise.
            """
            hostname = urlparse(url).hostname
            ip_pattern = re.compile(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$')
            return int(bool(hostname and ip_pattern.match(hostname)))

        def nb_dots(url: str) -> int:
            """
            Count the number of dots in the URL.
            
            Parameters:
            url (str): The URL to be analyzed.
            
            Returns:
            int: The number of dots in the URL.
            """
            return url.count('.')


        def nb_qm(url: str) -> int:
            """
            Count the number of question marks in the URL.
            
            Parameters:
            url (str): The URL to be analyzed.
            
            Returns:
            int: The number of question marks in the URL.
            """
            return url.count('?')


        def nb_eq(url: str) -> int:
            """
            Count the number of '=' symbols in the URL.
            
            Parameters:
            url (str): The URL to be analyzed.
            
            Returns:
            int: The number of '=' symbols in the URL.
            """
            return url.count('=')


        def nb_slash(url: str) -> int:
            """
            Count the number of slashes in the URL.
            
            Parameters:
            url (str): The URL to be analyzed.
            
            Returns:
            int: The number of slashes in the URL.
            """
            return url.count('/')


        def nb_www(url: str) -> int:
            """
            Count the number of 'www' occurrences in the URL.
            
            Parameters:
            url (str): The URL to be analyzed.
            
            Returns:
            int: The number of 'www' occurrences in the URL.
            """
            return url.lower().count('www')


        def ratio_digits_url(url: str) -> float:
            """
            Calculate the ratio of digits in the URL.
            
            Parameters:
            url (str): The URL to be analyzed.
            
            Returns:
            float: The ratio of digits in the URL.
            """
            digits = sum(c.isdigit() for c in url)
            return digits / len(url) if len(url) > 0 else 0


        def ratio_digits_host(url: str) -> float:
            """
            Calculate the ratio of digits in the hostname.
            
            Parameters:
            url (str): The URL to be analyzed.
            
            Returns:
            float: The ratio of digits in the hostname.
            """
            hostname = urlparse(url).hostname
            if hostname:
                digits = sum(c.isdigit() for c in hostname)
                return digits / len(hostname) if len(hostname) > 0 else 0
            return 0


        def tld_in_subdomain(url: str) -> int:
            """
            Check if the TLD is present in the subdomain of the URL.
            
            Parameters:
            url (str): The URL to be analyzed.
            
            Returns:
            bool: True if the TLD is present in the subdomain, False otherwise.
            """
            subdomain = urlparse(url).hostname.split('.')[0]
            tlds = [".com", ".net", ".org", ".info", ".biz", ".io", ".co"]
            return int(any(tld in subdomain.lower() for tld in tlds))


        def prefix_suffix(url: str) ->bool:
            """
            Check if the URL has a prefix-suffix (e.g., '-').
            
            Parameters:
            url (str): The URL to be analyzed.
            
            Returns:
            bool: True if the URL has a prefix-suffix, False otherwise.
            """
            hostname = urlparse(url).hostname
            return int('-' in hostname)


        def shortest_word_host(url)->int:
            hostname = urlparse(url).hostname
            if hostname:
                words = hostname.split('.')
                shortest_word = min(words, key=len)
                return len(shortest_word)
            return 0


        def longest_words_raw(url)->int:
            words = url.split('/')
            longest_word = max(words, key=len)
            return len(longest_word)


        def longest_word_path(url)->int:
            path = urlparse(url).path
            if path:
                words = path.split('/')
                longest_word = max(words, key=len)
                return len(longest_word)
            return 0


        def phish_hints(url: str) -> int:
            """
            Count the number of phishing hints (common phishing keywords) in the URL.
            
            Parameters:
            url (str): The URL to be analyzed.
            
            Returns:
            int: The number of phishing hints in the URL.
            """
            phishing_keywords = ['verify', 'account', 'login', 'update', 'banking', 'secure', 'signin', 'ebayisapi']
            return sum(keyword in url.lower() for keyword in phishing_keywords)


        def nb_hyperlinks(url):
            try:
                response = requests.get(url, timeout=5)
                response.raise_for_status()
                soup = BeautifulSoup(response.content, 'html.parser')
                links = soup.find_all('a')
                return len(links)
            except requests.RequestException:
                return 0  # Return 0 if there is an error fetching the page


        def ratio_intHyperlinks(url):
            try:
                response = requests.get(url, timeout=5)
                response.raise_for_status()
                soup = BeautifulSoup(response.content, 'html.parser')
                links = soup.find_all('a')
                total_links = len(links)
                
                if total_links == 0:
                    return 0.0
                
                domain = urlparse(url).hostname
                internal_links = [link for link in links if domain in link.get('href', '')]
                return len(internal_links) / total_links
            except requests.RequestException:
                return 0.0  # Return 0.0 if there is an error fetching the page


        def empty_title(url)->int:
            try:
                response = requests.get(url, timeout=5)
                response.raise_for_status()  # Check if the request was successful
                soup = BeautifulSoup(response.content, 'html.parser')
                title = soup.title.string if soup.title else ''
                return int(len(title.strip()) == 0)
            except requests.RequestException:
                return 1  # Return 1 if there is an error fetching the page or parsing the title


        def domain_in_title(url):
            try:
                response = requests.get(url, timeout=5)
                response.raise_for_status()
                soup = BeautifulSoup(response.content, 'html.parser')
                title = soup.title.string if soup.title else ''
                domain = urlparse(url).hostname
                return int(domain in title) if domain else 0
            except requests.RequestException:
                return 0  # Return 0 if there is an error fetching the page or parsing the title


        def domain_age(url: str) -> int:
            """
            Calculate the age of the domain (in days) since its creation.
            
            Parameters:
            url (str): The URL to be analyzed.
            
            Returns:
            int: The age of the domain in days.
            """
            domain = urlparse(url).netloc
            try:
                whois_info = whois.whois(domain)
                if whois_info.creation_date:
                    now = datetime.now()
                    domain_age = (now - whois_info.creation_date).days
                    return domain_age
                else:
                    return 0
            except:
                return 0


        def google_index(url: str) -> int:
            """
            Check if the URL is indexed by Google search engine.
            
            Parameters:
            url (str): The URL to be analyzed.
            
            Returns:
            int: 1 if the URL is indexed by Google, 0 otherwise.
            """
            # Placeholder function; actual implementation would involve querying Google's index
            return 0


        def page_rank(url: str) -> int:
            """
            Retrieve the Google PageRank for the URL.
            Note: Google has deprecated the PageRank API, so this function is for historical reference.
            
            Parameters:
            url (str): The URL to be analyzed.
            
            Returns:
            int: The PageRank value (deprecated API).
            """
            # Placeholder function; PageRank API has been deprecated and is no longer functional
            return 0


        def url_features(url: str) -> tuple:
            """
            Extract various features from the given URL.
            
            Parameters:
            url (str): The URL to extract features from.
            
            Returns:
            tuple: A tuple containing the values of all extracted features.
            """
            try:
                response = requests.get(url)
                html_content = response.text if response.status_code == 200 else ""
            except:
                html_content = ""

            features = (
                length_url(url),
                length_hostname(url),
                ip(url),
                nb_dots(url),
                nb_qm(url),
                nb_eq(url),
                nb_slash(url),
                nb_www(url),
                ratio_digits_url(url),
                ratio_digits_host(url),
                tld_in_subdomain(url),
                prefix_suffix(url),
                shortest_word_host(url),
                longest_words_raw(url),
                longest_word_path(url),
                phish_hints(url),
                nb_hyperlinks(url),
                ratio_intHyperlinks(url),
                empty_title(url),
                domain_in_title(url),
                domain_age(url),
                google_index(url),
                page_rank(url)
            )
            return features
        url_temp=url
        premansh=url_features(url_temp)
        chinkal=self.rf_model.predict([premansh])
        return bool(chinkal)





