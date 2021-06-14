""" Write a stream of close approaches to CSV or to JSON. """
import pathlib
import csv
import json

output_folder = pathlib.Path(__file__).parent.resolve() / 'output'


def write_to_csv(results, filename):
    """ Write an iterable of `CloseApproach` objects to a CSV file. filename: where the data should be saved. """
    fieldnames = ('datetime_utc', 'distance_au', 'velocity_km_s', 'designation', 'name', 'diameter_km',
                  'potentially_hazardous')

    with open(str(output_folder) + "/" + str(filename), 'w', newline='') as f:
        write = csv.writer(f)
        write.writerow(fieldnames)
        write.writerows([(r.time_str, r.distance, r.velocity, r.neo.designation, r.neo.name, r.neo.diameter,
                          r.neo.hazardous) for r in results])


def write_to_json(results, filename):
    """ Write an iterable of `CloseApproach` objects to a JSON file. filename: where the data should be saved. """
    dict_list = []
    for r in results:
        dict_list.append(r.serialize())

    with open(str(output_folder) + "/" + str(filename), 'w') as f:
        json.dump(dict_list, f, indent=2)
