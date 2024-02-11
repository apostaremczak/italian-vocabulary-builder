"""
Parser for .credentials
Reads secrets for used APIs
"""

import logging
from dataclasses import dataclass


@dataclass
class AppConfig:
    """Container for APIs' secrets"""

    pons_api_secret: str


def parse_config_from_credentials(file_path: str = ".credentials"):
    """Read .credentials and obtain secrets for used APIs"""
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            lines = file.readlines()
    except FileNotFoundError:
        logging.error("Missing .credentials file")

    credentials = {}
    for line in lines:
        key, value = line.strip().split("=")
        credentials[key] = value

    try:
        pons_api_secret = credentials["PONS_API_SECRET"]
    except KeyError as missing_pons_key_error:
        raise missing_pons_key_error

    return AppConfig(pons_api_secret=pons_api_secret)
