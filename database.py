""" A database encapsulating collections of near-Earth objects and their close approaches. """
import collections
from models import NearEarthObject, CloseApproach


class NEODatabase:
    """ A database of near-Earth objects and their close approaches. """
    def __init__(self, neos, approaches):
        """ Create a new `NEODatabase` from loaded NearEarthObject & CloseApproach data """
        self._approaches_dict = collections.defaultdict(set)

        self._neos = set()
        for neo in neos:
            self._neos.add(NearEarthObject(**neo))

        for neo in self._neos:
            neo.approaches = set()

        self._approaches = set()
        for approach in approaches:
            self._approaches.add(CloseApproach(**approach))

        # Add all related approaches under 'designation' ID as a dictionary
        # Not sure yet if both structures are needed or if only dict will be enough
        for approach in self._approaches:
            self._approaches_dict[approach.designation].add(approach)

        self._neos_dict = collections.defaultdict(NearEarthObject)
        for neo in self._neos:
            self._neos_dict[neo.designation] = neo

        # Attempt to add same neo to values of approaches_dict at once and therefore link them
        for key, value in self._approaches_dict.items():
            find_neo = self._neos_dict[key]  # directly accessing new defaultdict object
            for approach in value:
                approach.neo = find_neo

        # Attempt to feed all related approaches to NEOs
        # Less accessing time since approaches_dict is way smaller than original 400k rows
        for neo in self._neos:
            neo.approaches = set()
            for approach in self._approaches_dict[neo.designation]:
                neo.approaches.add(approach)
            neo.approaches_count = len(neo.approaches)

    def get_neo_by_designation(self, designation):
        """Find and return an NEO by its primary designation. If no match is found, return `None` instead. """
        neo = None
        for n in self._neos:
            if n.designation == designation:
                neo = n
        if not neo:
            return None
        else:
            return neo

    def get_neo_by_name(self, name):
        """ Find and return an NEO by its name. If no match is found, return `None` instead."""
        neo = None
        for n in self._neos:
            name_str = str(n.name).lower()
            if name_str == name.lower():
                neo = n
        if not neo:
            return None
        else:
            return neo

    def query(self, filters):
        """ Query close approaches to generate those that match a collection of filters. """
        date = filters['date']
        start_date = filters['start_date']
        end_date = filters['end_date']
        distance_min = filters['distance_min']
        distance_max = filters['distance_max']
        velocity_min = filters['velocity_min']
        velocity_max = filters['velocity_max']
        diameter_min = filters['diameter_min']
        diameter_max = filters['diameter_max']
        hazardous = filters['hazardous']

        # if filter is missing, then that row of code is all 'True' for all approaches
        # if filter is not missing then second part of the row has to be 'True' for code to return valid results
        output = (
                approach for approach in self._approaches if
                ((not date) or (approach.time.date() == date)) and
                ((not start_date) or (approach.time.date() >= start_date)) and
                ((not end_date) or (approach.time.date() <= end_date)) and
                ((not distance_min) or (approach.distance >= distance_min)) and
                ((not distance_max) or (approach.distance <= distance_max)) and
                ((not velocity_min) or (approach.velocity >= velocity_min)) and
                ((not velocity_max) or (approach.velocity <= velocity_max)) and
                ((not diameter_min) or (approach.neo.diameter >= diameter_min)) and
                ((not diameter_max) or (approach.neo.diameter <= diameter_max)) and
                ((not hazardous) or (approach.neo.hazardous == hazardous))
                )
        return output
