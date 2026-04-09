import re
from base64 import b64encode

import requests

from scraper.providers import BaseScraper


class HelloFreshScraper(BaseScraper):
    def scrape(self) -> dict:
        html = self.fetch_page()
        recipe = self.extract_json_ld(html)
        if not recipe:
            raise ValueError(f"No Recipe JSON-LD found at {self.url}")

        return {
            "name": recipe["name"],
            "ingredients": self._format_ingredients(recipe.get("recipeIngredient", [])),
            "nutritional_info": self._format_nutrition(recipe.get("nutrition", {})),
            "directions": self._format_directions(recipe.get("recipeInstructions", [])),
            "source_url": self.url,
            "servings": self._format_servings(recipe.get("recipeYield")),
            "categories": [recipe.get("recipeCategory", "HelloFresh")],
            "cook_time": recipe.get("totalTime", ""),
            "total_time": recipe.get("totalTime", ""),
            "description": recipe.get("description", ""),
            "photo": self._download_photo(recipe.get("image", "")),
        }

    @staticmethod
    def _format_ingredients(ingredients: list[str]) -> str:
        return "\n".join(ingredients)

    @staticmethod
    def _format_nutrition(nutrition: dict) -> str:
        if not nutrition:
            return ""
        parts = []
        labels = {
            "calories": "Kalorien",
            "fatContent": "Fett",
            "saturatedFatContent": "Gesättigte Fettsäuren",
            "carbohydrateContent": "Kohlenhydrate",
            "sugarContent": "Zucker",
            "proteinContent": "Eiweiß",
            "fiberContent": "Ballaststoffe",
            "sodiumContent": "Natrium",
        }
        for key, label in labels.items():
            value = nutrition.get(key)
            if value:
                parts.append(f"{label}: {value}")
        return "\n".join(parts)

    @staticmethod
    def _format_directions(instructions: list[dict]) -> str:
        steps = []
        for i, step in enumerate(instructions, 1):
            text = step.get("text", "")
            text = re.sub(r"<[^>]+>", "", text)
            text = re.sub(r"\n+", "\n", text).strip()
            steps.append(f"{i}. {text}")
        return "\n\n".join(steps)

    @staticmethod
    def _format_servings(recipe_yield) -> str:
        if recipe_yield is None:
            return ""
        return f"{recipe_yield} servings"

    def _download_photo(self, url: str) -> str:
        if not url:
            return ""
        r = requests.get(url, headers=self.headers)
        r.raise_for_status()
        return b64encode(r.content).decode("utf-8")
