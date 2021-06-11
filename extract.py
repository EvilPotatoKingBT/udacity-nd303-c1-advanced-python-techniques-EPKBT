""" Extract data on near-Earth objects and close approaches from CSV and JSON files. """
import csv
import json


def load_neos(filename):
    """ Read near-Earth object information from a CSV file. :filename = default path to a CSV file. """
    with open(filename, 'r') as file_input:
        reader = csv.DictReader(file_input)
        # headers = reader.fieldnames
        # dictionary approach that get flagged as error when doing tests. not sure why as the data gets loaded just fine
        objects = [{key: value for key, value in rows.items()} for rows in reader]

    # return headers, objects  # this will return both headers and objects
    return objects  # this will not return headers


def load_approaches(filename):
    """ Read close approach data from a JSON file.. :filename = default path to a JSON file. """
    with open(filename, 'r') as file_input:
        structure = json.load(file_input)
        # info = structure['signature']  # signature not used, keeping for later possible use
        headers = structure['fields']   # headers for our data
        data = structure['data']        # data without headers
        objects = [dict(zip(headers, rows)) for rows in data]

    # return info, headers, objects  # this will return both headers and objects with additional info in signature
    return objects  # this will not return headers nor info
