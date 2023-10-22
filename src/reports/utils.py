"""File for utility functions used in reports app."""

import os

import ipinfo


def get_ip_info(ip_address: str) -> dict:
    """
    Retrieves information about an IP address using the ipinfo library.

    Args:
        ip_address (str): The IP address for which information is to be retrieved.

    Returns:
        dict: A dictionary containing information about the IP address, such as the country, city, and organization.
    """
    access_token = os.environ['IPINFO_ACCESS_TOKEN']
    handler = ipinfo.getHandler(access_token)
    return handler.getDetails(ip_address)
