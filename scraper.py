from urllib.request import Request, urlopen
from html.parser import HTMLParser
from datetime import date

HEADERS = {"User-Agent": "Mozilla/5.0"}


def _fetch_html(url):
    request = Request(url, headers=HEADERS)
    with urlopen(request) as response:
        return response.read().decode("utf-8", errors="replace")


class _ClassTextParser(HTMLParser):
    def __init__(self, class_name):
        super().__init__()
        self.class_name = class_name
        self._capture = False
        self.text = ""

    def handle_starttag(self, tag, attrs):
        classes = dict(attrs).get("class", "").split()
        if self.class_name in classes and not self._capture:
            self._capture = True

    def handle_data(self, data):
        if self._capture:
            self.text += data

    def handle_endtag(self, tag):
        if self._capture:
            self._capture = False


def _class_text(html, class_name):
    parser = _ClassTextParser(class_name)
    parser.feed(html)
    return parser.text or None

def scrape_amazon(url, product_name):
    price_text = _class_text(_fetch_html(url), "a-price-whole")
    price = float(price_text.replace(",", "").strip()) if price_text else None

    return {
        "product": product_name,
        "source": "amazon",
        "price": price,
        "date": date.today()
    }

def scrape_flipkart(url, product_name):
    price_text = _class_text(_fetch_html(url), "_30jeq3")
    price = float(price_text.replace("₹", "").replace(",", "").strip()) if price_text else None

    return {
        "product": product_name,
        "source": "flipkart",
        "price": price,
        "date": date.today()
    }