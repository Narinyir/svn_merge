from config_manager import ConfigManager
from svn_adapter import SVNAdapter
from logger_manager import setup_logger


class SyncController:

    def __init__(self):
        self.config = ConfigManager()
        setup_logger()

    def initialize(self):
        main_wc = self.config.get("PATHS", "main_wc")
        out_wc = self.config.get("PATHS", "out_wc")

        if not main_wc or not out_wc:
            raise Exception("Не указаны пути к рабочим копиям.")

        if not SVNAdapter.is_working_copy_clean(main_wc):
            raise Exception("Рабочая копия MAIN содержит изменения.")

        if not SVNAdapter.is_working_copy_clean(out_wc):
            raise Exception("Рабочая копия OUTSOURCE содержит изменения.")

    def get_head_info(self):
        main_wc = self.config.get("PATHS", "main_wc")
        out_wc = self.config.get("PATHS", "out_wc")

        main_rev = SVNAdapter.get_head_revision(main_wc)
        out_rev = SVNAdapter.get_head_revision(out_wc)

        return main_rev, out_rev
    def scan_changes(self):
        main_wc = self.config.get("PATHS", "main_wc")
        out_wc = self.config.get("PATHS", "out_wc")
        sync_folder = self.config.get("PATHS", "sync_folder")

        last_main_rev = self.config.get("SYNC", "last_main_rev")
        last_out_rev = self.config.get("SYNC", "last_out_rev")

        if not last_main_rev:
            last_main_rev = SVNAdapter.get_head_revision(main_wc)

        if not last_out_rev:
            last_out_rev = SVNAdapter.get_head_revision(out_wc)

        engine = SyncEngine(
            main_wc,
            out_wc,
            sync_folder,
            last_main_rev,
            last_out_rev
        )
        return engine.scan()