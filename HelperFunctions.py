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


def print_traceback_location(exception):
    """
    A method to print traceback location.
    Would use the traceback package. However, I wanted to print none fatal errors,
    And the traceback package always prints exceptions in red text. Which makes the exceptions look like
    they are fatal.

    :param exception:
    :return: none
    """
    traceback = exception.__traceback__
    while traceback:
        print(f"{traceback.tb_frame.f_code.co_filename}: {traceback.tb_lineno}")
        traceback = traceback.tb_next


def get_traceback_location(exception):
    """
    A method to get traceback location.
    Would use the traceback package. However, I wanted to print none fatal errors,
    And the traceback package always prints exceptions in red text. Which makes the exceptions look like
    they are fatal.

    :param exception:
    :return: (String)
    """
    traceback = exception.__traceback__
    ret = ""
    while traceback:
        ret += f"{traceback.tb_frame.f_code.co_filename}: {traceback.tb_lineno}\n"
        traceback = traceback.tb_next
    return ret
