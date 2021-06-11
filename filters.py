""" Provide filters for querying close approaches and limit the generated results. """


def create_filters(date=None, start_date=None, end_date=None,
                   distance_min=None, distance_max=None,
                   velocity_min=None, velocity_max=None,
                   diameter_min=None, diameter_max=None,
                   hazardous=None):
    """ Create a collection of filters from user-specified criteria. """
    dict_filter = dict()
    dict_filter['date'] = date
    dict_filter['start_date'] = start_date
    dict_filter['end_date'] = end_date
    dict_filter['distance_min'] = distance_min
    dict_filter['distance_max'] = distance_max
    dict_filter['velocity_min'] = velocity_min
    dict_filter['velocity_max'] = velocity_max
    dict_filter['diameter_min'] = diameter_min
    dict_filter['diameter_max'] = diameter_max
    dict_filter['hazardous'] = hazardous
    return dict_filter


def limit(iterator, n=None):
    """ Produce a limited stream of values from an iterator. """
    if not n:
        max_results = 10
    elif n < 1 or type(n) != int:
        max_results = 10
    else:
        max_results = n

    if any(True for _ in iterator):
        set_output = set()
        for i in range(max_results):
            my_iter = next(iterator, None)
            if not my_iter:
                continue
            else:
                set_output.add(my_iter)
        return set_output
    else:
        raise AttributeError("Cannot return meaningful output, incorrect input!")
