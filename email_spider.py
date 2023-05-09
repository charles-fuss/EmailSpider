import validators
import re
import requests
import requests.exceptions
from urllib.parse import urlsplit, urljoin
from lxml import html
import sys
import csv


class EmailCrawler:
    processed_urls = set()
    unprocessed_urls = []
    emails = set()

    def __init__(self, name, website):
        self.name = name
        self.website = website
        self.unprocessed_urls = [website]
        self.headers = {
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/78.0.3904.70 Chrome/78.0.3904.70 Safari/537.36',
        }
        print(self.website)
        self.base_url = urlsplit(self.website).netloc
        self.outputfile = (self.base_url.replace('.','_')+'.csv')
        # we will use this list to skip urls that contain one of these extension. This will save us a lot of bandwidth and speedup the crawling process
        # for example: www.example.com/image.png --> this url is useless for us. we cannot possibly parse email from images and all other types of files.
        self.garbage_extensions = ['.aif','.cda','.mid','.midi','.mp3','.mpa','.ogg','.wav','.wma','.wpl','.7z','.arj','.deb','.pkg','.rar','.rpm','.tar.gz','.z','.zip','.bin','.dmg','.iso','.toast','.vcd','.csv','.dat','.db','.dbf','.log','.mdb','.sav','.sql','.tar','.apk','.bat','.bin','.cgi','.pl','.exe','.gadget','.jar','.py','.wsf','.fnt','.fon','.otf','.ttf','.ai','.bmp','.gif','.ico','.jpeg','.jpg','.png','.ps','.psd','.svg','.tif','.tiff','.asp','.cer','.cfm','.cgi','.pl','.part','.py','.rss','.key','.odp','.pps','.ppt','.pptx','.c','.class','.cpp','.cs','.h','.java','.sh','.swift','.vb','.ods','.xlr','.xls','.xlsx','.bak','.cab','.cfg','.cpl','.cur','.dll','.dmp','.drv','.icns','.ico','.ini','.lnk','.msi','.sys','.tmp','.3g2','.3gp','.avi','.flv','.h264','.m4v','.mkv','.mov','.mp4','.mpg','.mpeg','.rm','.swf','.vob','.wmv','.doc','.docx','.odt','.pdf','.rtf','.tex','.txt','.wks','.wps','.wpd']
        self.email_count = 0
        self.emails = []
        self.clean_url_tree(self.website)

    def crawl(self):
        """
        It will continue crawling untill the list unprocessed urls list is empty
        """
        try: #lazy fix for empty list
            url = self.unprocessed_urls.pop()
        except:
            return (self.name, self.email_count, self.emails)
        print("CRAWL : {}".format(url))
        couldntParseURL = self.parse_emails(url)
        if couldntParseURL == 'nil':
            return (self.name, self.email_count, self.emails)
        

        if len(self.emails)<20 and len(self.unprocessed_urls) > 1: # keep goin til u run out of urls
            self.crawl()
        else:
            print('End of crawling for {} '.format(self.website))
            print('Total urls visited {}'.format(len(self.processed_urls)))
            print('Total Emails found {}'.format(self.email_count))
            print("Finished")
        return (self.name, self.email_count, self.emails)
    

    def clean_url_tree(self, current_url):
        print('cleaning tree')
        try:
            response = requests.get(current_url, timeout=5)
            response2 = requests.get(current_url, headers=self.headers, timeout=5)
            if len(response2.content) > len(response.content):
                response=response2
        except:
            return []
        try:
            tree = html.fromstring(response.content)
        except:
            return 0
        urls = tree.xpath('//a/@href')  # getting all urls in the page
        print(f"raw urls: {urls}")
        # removing duplicates
        urls = list(set(urls))
        
        print(f"Raw urls: {urls}")
        # filtering urls that point to files such as images, videos and other as listed on garbage_extensions
        # here will loop through all the urls and skip them if they contain one of the extension
        parsed_url = []
        for url in urls:
            skip = False
            for extension in self.garbage_extensions:
                if not url.endswith(extension) and not url.endswith(extension+'/'):
                    pass
                else:
                    skip = True
                    break
            if (validators.url(f"{self.website}{url}") or validators.url(url)) and url not in parsed_url and skip!=True:
                # we do this because sometimes the tree request returns "/../../default.aspx" instead of https://example.com/../../default.aspx
                if validators.url(f"{self.website}{url}"):
                    parsed_url.append(f"{self.website}{url}")
                else:
                    parsed_url.append(url)
        
        # first, add all urls. next, push urls that contain juicy email keywords to the bottom of the queue, since the script uses .pop
        for url in parsed_url:
            if 'contact' in url or 'about' in url or 'utility' in url or 'utilities' in url or 'water' in url or 'team' in url or 'employee' in url or 'staff' in url:
                parsed_url.remove(url)
                parsed_url.append(url)
        print(f"Final URL list: {parsed_url}")
        self.unprocessed_urls = parsed_url

    # cleans email up given an instance of EmailCrawler. parses a URL, identifies all emails on the page, and cleans em all up
    def parse_emails(self, url):
        """
        scans the given texts to find email address and then writes them to csv
        Input:
            text: text to parse emails from
        Returns:
            bool: True or false (True if email was found on page)
        """
        try:
            response = requests.get(url, headers=self.headers, timeout=5)
        except:
            try:
                response = requests.get(url,timeout=5)
            except:
                return 'nil'
        self.processed_urls.add(self.website)
        text = response.text
        # parsing emails and then saving to csv
        emails = set(re.findall(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+', text, re.I))
        #TODO: sometime "gFJS3amhZEg_z39D5EErVg@2x.png" gets accepted as email with the above regex. so for now i will check if email ends with jpeg,png and jpg

        for email in emails:
            skip_email = False
            for checker in ['jpg','jpeg','png']:
                if email.endswith(checker):
                    skip_email = True
                    break

            if not skip_email:    
                if email not in self.emails:
                    self.email_count +=1
                    self.emails.append(email)
                    print(' {} Email found {}'.format(self.email_count,email))

        if len(emails)!=0:
            return True
        else:
            return False
