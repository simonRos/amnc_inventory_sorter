import sys
from methods import *

def main():
    try:
        create_db()
        load_inventory()
        load_top_inventory()
    except ValueError as ve:
        return str(ve)


if __name__ == '__main__':
    sys.exit(main())
