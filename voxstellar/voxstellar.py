from threading import Thread
from time import sleep

from voxstellar.application_sender import ApplicationSender
from voxstellar.debug import Debug
from voxstellar.config import Config
from config import appversion, config

TIME_WORKER_PERIOD_S = 60


class VoxStellar:
    """
    The main class for the plugin.
    """

    def __init__(self, plugin_name: str):
        """
        Initialize the plugin.

        :param plugin_name: The name of the plugin.
        """
        self.plugin_name: str = plugin_name

    def plugin_start(self, plugin_dir: str):
        """
        The plugin is starting up. Initialise all our objects.
        """
        self.plugin_dir = plugin_dir

        self.debug: Debug = Debug(self)
        self.config: Config = Config(self)
        self.application_sender: ApplicationSender = ApplicationSender(self)

        self.thread: Thread = Thread(target=self._worker, name="VoxStellar worker")
        self.thread.daemon = True
        self.thread.start()

    def plugin_stop(self):
        """
        The plugin is shutting down.
        """
        return

    def journal_entry(self, cmdrname: str, is_beta: bool, system: str, station: str, entry: dict, state: dict) -> None:
        """
        Handle the given journal entry.

        :param cmdrname:
        :param is_beta:
        :param system:
        :param station:
        :param entry:
        :param state:
        :return: None
        """

        # Testing purposes
        # self.application_sender.send(cmdrname, entry)

        if entry['event'] == 'Scan' or entry['event'] == 'FSDJump' or entry['event'] == 'FSSDiscoveryScan' or entry['event'] == 'SAASignalsFound' or entry['event'] == 'ScanOrganic':
            self.application_sender.send(cmdrname, entry)

    def _worker(self) -> None:
        """
        Handle thread work
        """
        Debug.logger.debug("Starting VoxStellar Worker...")

        while True:
            if config.shutting_down:
                Debug.logger.debug("Shutting down VoxStellar Worker...")
                return

            sleep(TIME_WORKER_PERIOD_S)
