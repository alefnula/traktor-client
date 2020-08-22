import os
from pathlib import Path
from configparser import ConfigParser

from traktor_client import errors


class Config:
    def __init__(self):
        # Path to the configuration file
        self.config_dir = (Path("~").expanduser() / ".traktor").absolute()
        self.config_file = self.config_dir / "traktor.ini"

        # Server
        self.server_host = "127.0.0.1"
        self.server_port = 5000

        # Load the values from configuration file
        self.load()

    def load(self):
        """Load configuration."""
        if not os.path.isfile(self.config_file):
            return
        try:
            cp = ConfigParser()
            cp.read(self.config_file)
            if cp.has_option("server", "host"):
                self.server_host = cp.get("server", "host")
            if cp.has_option("server", "port"):
                self.server_port = cp.getint("server", "port")
        except Exception as e:
            raise errors.InvalidConfiguration(
                message=f"Cannot read the config file '{self.config_file}'. "
                f"Error: {e}"
            )

    @property
    def server_url(self):
        return f"{self.server_host}:{self.server_port}"


config = Config()
