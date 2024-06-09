"""
This module contains utility functions that are used by the nodes.
"""
import io

import openpyxl


def excel_to_json(excel_bytes: bytes) -> list[dict]:
    """
    Converts an Excel file to a JSON object.

    Args:
        excel_bytes (bytes): The Excel file in bytes format.

    Returns:
        list[dict]: A list of dictionaries representing the data in the Excel file converted to JSON format.

    Raises:
        None.

    Note:
        - The Excel file should have the following structure:
            - The first row contains the keys for each column.
            - The second row contains the values for each key.
            - The third row onwards contains the data for each key.
        - The first key in the first row is expected to be a date in the format '%Y-%m-%d %H:%M:%S'.
        - Empty cells in the Excel file will be converted to None in the JSON object.
        - The units for each environmental variable will be extracted from the keys in the first row.
        - The resulting JSON object will include a 'units' field for each environmental variable.
    """

    # Load the workbook from the BytesIO object
    workbook: openpyxl.Workbook = openpyxl.load_workbook(filename=io.BytesIO(excel_bytes))

    # Get the active worksheet
    worksheet: openpyxl.worksheet.worksheet.Worksheet = workbook.active

    keys_units: list = [cell.value for cell in worksheet[1]]

    # Get the keys from the second row of the worksheet
    keys_values: list = [cell.value for cell in worksheet[2]]

    keys_units[0] = keys_values[0] + " [%Y-%m-%d %H:%M:%S]"
    keys_units[len(keys_units) - 1] = keys_values[len(keys_values) - 1]

    keys_name = [
        "date",
        "temperature",
        "dew_point",
        "solar_radiation",
        "vapor_pressure_deficit",
        "relative_humidity",
        "precipitation",
        "wind_speed",
        "wind_gust",
        "wind_direction",
        "solar_panel",
        "battery",
        "delta_t",
        "sun_duration",
        "evapotranspiration",
    ]

    # Create a dictionary of units for each environmental variable
    units_dict = {}
    for key_unit in keys_units:
        if key_unit:
            key, unit = key_unit.split('[')
            unit = unit.rstrip(']')
            units_dict[key.strip()] = unit

    # Initialize the JSON data
    json_data: list = []

    # Convert each row in the worksheet to a JSON object
    for row in worksheet.iter_rows(min_row=3, values_only=True):
        obj: dict = {key: value if value != '' else None for key, value in zip(keys_units, row) if key is not None}
        data: dict = {keys_name[i]: value for i, value in enumerate(obj.values())}
        data_units: dict = {keys_name[i]: units_dict[key] for i, key in enumerate(units_dict.keys())}
        data["units"] = data_units
        json_data.append(data)

    # Return the JSON data
    return json_data
