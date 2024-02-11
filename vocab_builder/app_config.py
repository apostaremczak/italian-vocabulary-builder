import logging
from dataclasses import dataclass


@dataclass
class AppConfig:
    pons_api_secret: str


def parse_config_from_credentials(file_path: str = ".credentials"):
    try:
        with open(file_path, "r") as file:
            lines = file.readlines()
    except FileNotFoundError:
        logging.error("Missing .credentials file")

    credentials = {}
    for line in lines:
        key, value = line.strip().split("=")
        credentials[key] = value

    try:
        pons_api_secret = credentials["PONS_API_SECRET"]
    except KeyError:
        logging.error("Missing PONS_API_SECRET from the .credentials file")

    return AppConfig(pons_api_secret=pons_api_secret)
