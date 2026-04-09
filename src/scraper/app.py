import sys

import yaml

from scraper.providers.hellofresh import HelloFreshScraper


def main(recipe_url: str):
    scraper = HelloFreshScraper(url=recipe_url)
    data = scraper.scrape()

    filename = data.get("name", "recipe") + ".yml"
    with open(filename, "w", encoding="utf-8") as f:
        yaml.dump(data, f, allow_unicode=True, default_flow_style=False)

    print(f"Recipe saved to {filename}")


def cli():
    if len(sys.argv) < 2:
        print("Usage: pyrecipes <recipe-url>", file=sys.stderr)
        sys.exit(1)
    main(sys.argv[1])


if __name__ == "__main__":
    cli()
