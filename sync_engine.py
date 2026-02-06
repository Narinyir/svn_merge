from collections import defaultdict
from svn_adapter import SVNAdapter


class ChangeItem:
    def __init__(self, path):
        self.path = path
        self.main_action = None
        self.out_action = None
        self.type = "safe"  # safe | conflict
        self.details = ""


class SyncEngine:

    def __init__(self, main_wc, out_wc, sync_folder, last_main_rev, last_out_rev):
        self.main_wc = main_wc
        self.out_wc = out_wc
        self.sync_folder = sync_folder
        self.last_main_rev = last_main_rev
        self.last_out_rev = last_out_rev

    def scan(self):
        main_head = SVNAdapter.get_head_revision(self.main_wc)
        out_head = SVNAdapter.get_head_revision(self.out_wc)

        main_changes = SVNAdapter.get_log_summary(
            self.main_wc,
            self.last_main_rev,
            main_head
        )

        out_changes = SVNAdapter.get_log_summary(
            self.out_wc,
            self.last_out_rev,
            out_head
        )

        return self._classify(main_changes, out_changes)

    def _classify(self, main_changes, out_changes):

        items = {}

        # Фильтр по папке синка
        def in_sync_folder(path):
            return self.sync_folder in path

        for change in main_changes:
            path = change["path"]
            if not in_sync_folder(path):
                continue

            if path not in items:
                items[path] = ChangeItem(path)

            items[path].main_action = change["action"]

        for change in out_changes:
            path = change["path"]
            if not in_sync_folder(path):
                continue

            if path not in items:
                items[path] = ChangeItem(path)

            items[path].out_action = change["action"]

        # Классификация
        for item in items.values():

            if item.main_action and item.out_action:
                item.type = "conflict"
                item.details = "Изменён в обоих репозиториях"
            else:
                item.type = "safe"

        safe = [i for i in items.values() if i.type == "safe"]
        conflicts = [i for i in items.values() if i.type == "conflict"]

        return safe, conflicts
