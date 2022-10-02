__author__ = "Simon Rosner"
__credits__ = ["Simon Rosner"]
__license__ = "GNU GENERAL PUBLIC LICENSE Version 3, 29 June 2007"
__version__ = "1.0.0"
__maintainer__ = "Simon Rosner"
__email__ = "simon.h.rosner@gmail.com"
__status__ = "Production"

import sys
from methods import *

def main():
    try:
        create_db()
        load_inventory()
        load_top_inventory()
        write_joined_data()
    except ValueError as ve:
        return str(ve)


if __name__ == '__main__':
    sys.exit(main())

