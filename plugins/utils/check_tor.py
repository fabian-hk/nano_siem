from pathlib import Path
import logging
import urllib.request
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class CheckTor:
    def __init__(self):
        self._prepare_tor_exit_node()

    def _prepare_tor_exit_node(self):
        app_folder = Path.home() / ".nano_siem"
        app_folder.mkdir(parents=True, exist_ok=True)
        tor_lst_file = app_folder / "tor_exit_nodes.txt"

        # check if file exists
        if tor_lst_file.exists():
            modified_date = datetime.fromtimestamp(tor_lst_file.stat().st_mtime)
            # download new file and replace only if exists more than a day
            if modified_date < datetime.now() - timedelta(days=1):
                urllib.request.urlretrieve(
                    "https://check.torproject.org/torbulkexitlist",
                    str(tor_lst_file.resolve()),
                )
        else:
            urllib.request.urlretrieve(
                "https://check.torproject.org/torbulkexitlist",
                str(tor_lst_file.resolve()),
            )

        data = tor_lst_file.read_text()
        self.tor_exit_nodes_ip = set(data.split("\n"))

    def is_tor_exit_node(self, input: str) -> bool:
        if input in self.tor_exit_nodes_ip:
            return True
        else:
            return False
