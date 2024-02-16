import logging
from tabulate import tabulate

import logging
from tabulate import tabulate

def vizualization(func):
    def inner(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            if isinstance(result, list) and result:
                info_row = [f"Query Info: {func.__doc__}"]
                table_data = [list(item) for item in result]
                table = tabulate(table_data, headers=info_row, tablefmt="pretty")
                logging.info('\n' + table)
                return result
            elif not result:
                logging.info("Returned data are empty!")
            else:
                logging.error(f"Can't proceed. The type of returned data is {type(result)}")
        except Exception as ex:
            logging.exception(f"An error occurred while executing query: {ex}")

    return inner

