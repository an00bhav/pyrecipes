import json

import pytest

from scraper.providers.hellofresh import HelloFreshScraper
from scraper.providers.utils import format_measurements


SAMPLE_JSON_LD = {
    "@context": "http://schema.org/",
    "@type": "Recipe",
    "name": "Sake Don Bowl",
    "description": "A delicious salmon bowl",
    "image": "",
    "totalTime": "30m",
    "recipeYield": 2,
    "recipeCategory": "Hauptgericht",
    "nutrition": {
        "@type": "NutritionInformation",
        "calories": "927 kcal",
        "fatContent": "44.8 g",
        "proteinContent": "45.7 g",
        "carbohydrateContent": "83.4 g",
    },
    "recipeIngredient": [
        "300 g Lachsfilet",
        "200 g geraspelter Rotkohl",
        "1 Stück Brokkoli",
    ],
    "recipeInstructions": [
        {"@type": "HowToStep", "text": "<p>Erhitze Wasser.</p>\n<p>Reis kochen.</p>"},
        {"@type": "HowToStep", "text": "<p>Brokkoli schneiden.</p>"},
    ],
}

SAMPLE_HTML = (
    "<html><head>"
    '<script type="application/ld+json">'
    + json.dumps(SAMPLE_JSON_LD)
    + "</script></head><body></body></html>"
)


class TestHelloFreshScraper:
    def test_extract_json_ld(self):
        scraper = HelloFreshScraper(url="https://example.com")
        result = scraper.extract_json_ld(SAMPLE_HTML)
        assert result is not None
        assert result["@type"] == "Recipe"
        assert result["name"] == "Sake Don Bowl"

    def test_extract_json_ld_missing(self):
        scraper = HelloFreshScraper(url="https://example.com")
        result = scraper.extract_json_ld("<html><body>No recipe</body></html>")
        assert result is None

    def test_format_ingredients(self):
        ingredients = ["300 g Lachsfilet", "200 g Rotkohl", "1 Stück Brokkoli"]
        result = HelloFreshScraper._format_ingredients(ingredients)
        assert result == "300 g Lachsfilet\n200 g Rotkohl\n1 Stück Brokkoli"

    def test_format_ingredients_empty(self):
        assert HelloFreshScraper._format_ingredients([]) == ""

    def test_format_nutrition(self):
        nutrition = {
            "calories": "927 kcal",
            "fatContent": "44.8 g",
            "proteinContent": "45.7 g",
        }
        result = HelloFreshScraper._format_nutrition(nutrition)
        assert "Kalorien: 927 kcal" in result
        assert "Fett: 44.8 g" in result
        assert "Eiweiß: 45.7 g" in result

    def test_format_nutrition_empty(self):
        assert HelloFreshScraper._format_nutrition({}) == ""

    def test_format_directions_strips_html(self):
        instructions = [
            {"@type": "HowToStep", "text": "<p>Erhitze <span>Wasser</span>.</p>"},
            {"@type": "HowToStep", "text": "<p>Reis kochen.</p>"},
        ]
        result = HelloFreshScraper._format_directions(instructions)
        assert "<p>" not in result
        assert "<span>" not in result
        assert result.startswith("1. Erhitze Wasser.")
        assert "2. Reis kochen." in result

    def test_format_directions_numbering(self):
        instructions = [
            {"@type": "HowToStep", "text": "Step A"},
            {"@type": "HowToStep", "text": "Step B"},
            {"@type": "HowToStep", "text": "Step C"},
        ]
        result = HelloFreshScraper._format_directions(instructions)
        assert "1. Step A" in result
        assert "2. Step B" in result
        assert "3. Step C" in result

    def test_format_servings(self):
        assert HelloFreshScraper._format_servings(2) == "2 servings"
        assert HelloFreshScraper._format_servings(4) == "4 servings"
        assert HelloFreshScraper._format_servings(None) == ""


class TestUtils:
    @pytest.mark.parametrize(
        "text,expected",
        [
            ("1 StückFrühlingszwiebel", "1 Stück Frühlingszwiebel"),
            ("20 gIngwer", "20 g Ingwer"),
            ("250 mlKokosmilch", "250 ml Kokosmilch"),
            ("1 StückZitrone", "1 Stück Zitrone"),
            ("1 StückLimette", "1 Stück Limette"),
        ],
    )
    def test_format_measurements(self, text, expected):
        measurements = ["Stück", "ml", "g"]
        assert format_measurements(text, measurements) == expected
