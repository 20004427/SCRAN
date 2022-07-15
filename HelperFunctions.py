import pandas


def read_keywords(path, sheet_name, column_headers=None):
    """Function to read a list of words from an excel file.
    Returns a Pandas object.

    :param path: (String) Path to the excel file, this can be relative or absolute
    :param sheet_name: (String)
    :return: (Pandas data_frame) matrix of words
    """
    data_frame = pandas.read_excel(path, sheet_name=sheet_name, header=None)
    return data_frame
