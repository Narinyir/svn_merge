import logging


def setup_logger():
    logging.basicConfig(
        filename="sync_tool.log",
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        encoding="utf-8"
    )
