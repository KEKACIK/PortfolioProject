import os
from contextlib import suppress
from pathlib import Path

from yaml import load

from .exceptions import LangNotFound, TextNotFound
from .locale import Locale

try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader


class LocaleManager:
    def __init__(self, locales_dir: Path):
        self.locales = self.load_locales(locales_dir)

    def get_locale(self, lang: str):
        for locale in self.locales:
            if locale.lang == lang:
                return locale

        raise LangNotFound

    def get_buttons(self, name: str):
        buttons = []

        for locale in self.locales:
            with suppress(TextNotFound):
                buttons.append(locale.get(f"buttons.{name}"))

        return buttons

    @staticmethod
    def load_locales(locales_dir: Path):
        files = os.listdir(locales_dir)
        locale_files = [filename for filename in files if filename.endswith(".yml")]

        locales = []

        for filename in locale_files:
            with open(locales_dir / filename, "r", encoding="utf-8") as file:
                values = load(file, Loader)
                locale = Locale(values, lang=filename.replace(".yml", "", 1))
                locales.append(locale)

        return locales
