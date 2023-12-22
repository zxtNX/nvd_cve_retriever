import logging
from colorama import Fore, Style, init
from nvd_cve_retriever.utils.utils import create_and_get_log_directory
from nvd_cve_retriever.logs.logger_interface import ILogger


class ColoredLogger(ILogger):
    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        init(autoreset=True)

    def info(self, message: str):
        if self.verbose:
            print(f"{Fore.BLUE}[*] {message}{Style.RESET_ALL}")

    def success(self, message: str):
        if self.verbose:
            print(f"{Fore.GREEN}[+] {message}{Style.RESET_ALL}")

    def warning(self, message: str):
        if self.verbose:
            print(f"{Fore.YELLOW}[!] {message}{Style.RESET_ALL}")

    def error(self, message: str):
        if self.verbose:
            print(f"{Fore.RED}[X] {message}{Style.RESET_ALL}")


logger = ColoredLogger(verbose=True)


def configure_logging(verbose_level: bool):
    log_directory = create_and_get_log_directory(logger)
    log_file_path = log_directory / "nvd_cve_retriever.log"

    logging_level = logging.DEBUG if verbose_level else logging.ERROR
    logging.basicConfig(filename=str(log_file_path), level=logging_level)
