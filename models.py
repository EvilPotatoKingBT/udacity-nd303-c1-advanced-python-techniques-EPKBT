""" Represent models for near-Earth objects and their close approaches. """

from helpers import cd_to_datetime, datetime_to_str
import math


class NearEarthObject:
    """ A near-Earth object (NEO). It maintains a collection of its close approaches. """
    def __init__(self, **info):
        """Create a new `NearEarthObject` from a dictionary of excess keyword arguments - info """
        self.designation = info['pdes']         # is unique and I assume error handling is not needed.
        self._full_name = info['full_name']     # assume it should be error free

        if info['name'] == '':
            self.name = None
        elif not info['name']:
            self.name = None
        else:
            self.name = info['name']

        # self.diameter_original = info['diameter']
        try:
            self.diameter = float(info['diameter'])
        except ValueError:
            self.diameter = float('nan')
        except TypeError:
            self.diameter = float('nan')

        if info['pha'] == 'N':
            self.hazardous = False
        elif not info['pha']:
            self.hazardous = False
        else:
            self.hazardous = True

        # Create an empty initial collection of linked approaches.
        self.approaches = set()

    def serialize(self):
        v_diameter = self.diameter
        if math.isnan(v_diameter) or math.isinf(v_diameter) or v_diameter == float('nan'):
            v_diameter = None  # self.neo.diameter_original

        return dict(designation=self.designation, name=self.name, diameter_km=v_diameter,
                    potentially_hazardous=self.hazardous)

    @property
    def fullname(self):
        """Return a representation of the full name of this NEO."""
        return self._full_name

    @property
    def str_hazard(self):
        if self.hazardous:
            return 'is potentially'
        else:
            return 'is NOT potentially'

    def __str__(self):
        """Return `str(self)`."""
        if not self.name and math.isnan(self.diameter):
            return f"NearEarthObject({self.designation!r}): It has no name, its diameter is unknown and " \
                   f"{self.str_hazard} hazardous. Its full name is {self.fullname!r}"
        elif not self.name:
            return f"NearEarthObject({self.designation!r}): It has no name, has diameter of {self.diameter:.3f} km " \
                   f"and {self.str_hazard} hazardous. Its full name is {self.fullname!r}"
        elif math.isnan(self.diameter):
            return f"NearEarthObject({self.designation!r}): It's name is {self.name!r}, its diameter is unknown and " \
                   f"{self.str_hazard} hazardous. Its full name is {self.fullname!r}"
        else:
            return f"NearEarthObject({self.designation!r}): It's name is {self.name!r}, " \
                   f"has diameter of {self.diameter:.3f} km and {self.str_hazard} hazardous."

    def __repr__(self):
        """Return `repr(self)`, a computer-readable string representation of this object."""
        return f"NearEarthObject(designation={self.designation!r}, name={self.name!r}, diameter={self.diameter:.3f}, " \
               f"hazardous={self.hazardous!r}"


class CloseApproach:
    """ A close approach to Earth by an NEO. It maintains a reference to it. """
    def __init__(self, **info):
        """Create a new `CloseApproach` from a dictionary of excess keyword arguments - info """
        self._designation = info['des']
        self._orbit_id = info['orbit_id']
        self.distance = 0.0
        # self.distance_original = 0.0
        self.velocity = 0.0
        # self.velocity_original = 0.0
        self._cd = info['cd']
        self.time = cd_to_datetime(self._cd)

        # self.distance_original = info['dist']
        try:
            value = float(info['dist'])
        except ValueError:
            pass
        except TypeError:
            pass
        else:
            if not math.isnan(value) and not math.isinf(value):
                self.distance = value
            else:
                self.distance = float('nan')

        # self.velocity_original = info['v_rel']
        try:
            value = float(info['v_rel'])
        except ValueError:
            pass
        except TypeError:
            pass
        else:
            if not math.isnan(value) and not math.isinf(value):
                self.velocity = value
            else:
                self.velocity = float('nan')

        # Create an attribute for the referenced NEO, originally None.
        self.neo = None

    def serialize(self):

        v_distance = self.distance
        if math.isnan(v_distance) or math.isinf(v_distance) or v_distance == float('nan'):
            v_distance = None  # self.distance_original

        v_velocity = self.velocity
        if math.isnan(v_velocity) or math.isinf(v_velocity) or v_velocity == float('nan'):
            v_velocity = None  # self.velocity_original

        v_diameter = self.neo.diameter
        if math.isnan(v_diameter) or math.isinf(v_diameter) or v_diameter == float('nan'):
            v_diameter = None  # self.neo.diameter_original

        return dict(datetime_utc=self.time_str, distance_au=v_distance, velocity_km_s=v_velocity,
                    neo=dict(designation=self.neo.designation, name=self.neo.name, diameter_km=v_diameter,
                             potentially_hazardous=self.neo.hazardous))

    @property
    def designation(self):
        return self._designation

    @property
    def time_str(self):
        """Return a formatted representation of this `CloseApproach`'s approach time. Format = "YYYY-MM-DD HH:MM" """
        return datetime_to_str(self.time)

    def __str__(self):
        """Return `str(self)`."""
        return f"Close approach of {self.designation!r} on {self.time_str!r} at distance of " \
               f"{self.distance:.2f} AU and a velocity of {self.velocity:.2f} km/s."  # neo={self.neo!r}"

    def __repr__(self):
        """
        Return `repr(self)`, a computer-readable string representation of this object.
        """
        return (f"CloseApproach(time={self.time_str!r}, distance={self.distance:.2f} AU, "
                f"velocity={self.velocity:.2f} km/s.")
