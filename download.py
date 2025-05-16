import logging
import os
import requests
import xml.etree.ElementTree as ET
from urllib.parse import urlparse

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

RSS = "composing-with-process.rss"
DIR = "content/"

def make_directory():
    if not os.path.isdir(DIR):
        os.mkdir(DIR)

def process(item):
    enc = item.find('enclosure')
    if enc is not None and enc.get('url'):
        title = item.find('title').text
        log.info(f"Downloading {title}")
        url = urlparse(enc.get('url'))
        _, filename = url.path.rsplit('/', 1)

        with open(DIR+filename, 'wb') as fd:
            mimetype = None
            try:
                res = requests.get(url.geturl(), allow_redirects=True)
                log.debug(res)
                mimetype = res.headers.get('content-type')
                fd.write(res.content)
            except:
                log.warning(f"❌ failed {url}")
            finally:
                match mimetype:
                    case "audio/mpeg":
                        log.info(f"👂 {title}")
                    case "application/pdf":
                        log.info(f"👁 {title}")
                    case _:
                        log.info(f"👃 {mimetype}")

def compose():
    tree = ET.parse(RSS)
    root = tree.getroot()
    make_directory()
    for item in list(root.iter('item'))[::-1]:
        process(item)


if __name__ == "__main__":
    compose()
