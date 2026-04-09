# pyrecipes

A tool to scrape recipes from HelloFresh and export them as YAML for import into [Paprika](https://paprikaapp.com).

### Usage

```bash
# First time setup
just install

# Scrape a recipe
just scrape "https://www.hellofresh.de/recipes/sake-don-bowl-teriyaki-lachsfilet-64e4647c0989be803362ee35"
```

This generates a `.yml` file in the `src/` directory that you can import directly into Paprika.

### Development

Requires Python 3.12+ and [uv](https://docs.astral.sh/uv/) for dependency management.

```bash
just install   # create venv & install dependencies
just test      # run tests
```

### How it works

The scraper extracts structured [JSON-LD](https://json-ld.org/) recipe data (`schema.org/Recipe`) embedded in HelloFresh pages, which is more reliable than parsing HTML directly.
