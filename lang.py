import glob
import json

class Locale:
    lang = []
    locale_code = "vi_vn"

    @staticmethod
    def load(lang_dir = "./locales/"):
        for locale in glob.glob("*.json", root_dir=lang_dir):
            locale_code = locale.split(".json")[0]
            with open(lang_dir + locale, 'r', encoding='utf-8') as f:
                Locale.lang[locale_code] = json.load(f)

    @staticmethod
    def set_locale(code):
        Locale.locale_code = code

Locale.load()
