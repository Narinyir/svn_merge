import configparser
import os


class ConfigManager:
    def __init__(self, path="sync_tool.ini"):
        self.path = path
        self.config = configparser.ConfigParser()

        if os.path.exists(self.path):
            self.config.read(self.path)
        else:
            self.config["PATHS"] = {
                "main_wc": "",
                "out_wc": "",
                "sync_folder": ""
            }
            self.config["SYNC"] = {
                "last_main_rev": "",
                "last_out_rev": ""
            }
            self.save()

    def save(self):
        with open(self.path, "w", encoding="utf-8") as f:
            self.config.write(f)

    def get(self, section, key):
        return self.config.get(section, key, fallback="")

    def set(self, section, key, value):
        self.config[section][key] = str(value)
        self.save()
