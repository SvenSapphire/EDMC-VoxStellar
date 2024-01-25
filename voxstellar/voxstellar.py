from threading import Thread
from time import sleep

from voxstellar.application_sender import ApplicationSender
from voxstellar.config import Config
from queue import Queue
from config import appversion, config

TIME_WORKER_PERIOD_S = 2


class VoxStellar:
    """
    The main class for the plugin.
    """

    def __init__(self, plugin_name: str, logger):
        """
        Initialize the plugin.

        :param plugin_name: The name of the plugin.
        """
        self.plugin_name: str = plugin_name
        self.logger = logger
        self.queue = Queue()

    def plugin_start(self, plugin_dir: str):
        """
        The plugin is starting up. Initialise all our objects.
        """
        self.plugin_dir = plugin_dir

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

        allowed_events = ['Scan', 'FSDTarget', 'FSDJump', 'FSSDiscoveryScan', 'SAASignalsFound', 'ScanOrganic',
                          'ScanBaryCentre', 'CodexEntry']

        if entry['event'] in allowed_events:
            self.queue.put((cmdrname, entry))

    def _worker(self) -> None:
        """
        Handle thread work
        """
        self.logger.debug("Starting VoxStellar Worker...")

        while True:
            if config.shutting_down:
                self.logger.debug("Shutting down VoxStellar Worker...")
                return

            if not self.queue.empty():
                cmdrname, entry = self.queue.get()
                try:
                    self.application_sender.send(cmdrname, entry, self.logger)
                except Exception as e:
                    self.logger.error(f"Error sending data: {e}")
                finally:
                    self.queue.task_done()

            sleep(TIME_WORKER_PERIOD_S)
