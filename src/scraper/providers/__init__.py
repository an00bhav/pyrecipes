import json
from dataclasses import dataclass, field

import requests
from bs4 import BeautifulSoup


@dataclass
class BaseScraper:
    url: str
    headers: dict = field(
        default_factory=lambda: {"User-Agent": "github.com/anubhavcodes/pyrecipes"}
    )

    def fetch_page(self) -> str:
        r = requests.get(self.url, headers=self.headers)
        r.raise_for_status()
        return r.text

    def get_soup(self, html: str) -> BeautifulSoup:
        return BeautifulSoup(html, "html.parser")

    def extract_json_ld(self, html: str) -> dict | None:
        soup = self.get_soup(html)
        for script in soup.find_all("script", {"type": "application/ld+json"}):
            try:
                data = json.loads(script.string)
                if isinstance(data, dict) and data.get("@type") == "Recipe":
                    return data
                if isinstance(data, list):
                    for item in data:
                        if isinstance(item, dict) and item.get("@type") == "Recipe":
                            return item
            except (json.JSONDecodeError, TypeError):
                continue
        return None

    def scrape(self) -> dict:
        raise NotImplementedError
