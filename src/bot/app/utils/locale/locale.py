from .exceptions import TextNotFound


class Locale:
    def __init__(self, values: dict, lang: str):
        self.__values = values
        self.lang = lang

    def get(self, name: str, **kwargs):
        try:
            group, text_id = name.split(".")
            return self.__values[group][text_id].format(**kwargs)
        except KeyError:
            raise TextNotFound
