import sys
from methods import *

def main():
    try:
        create_db()
        print("db created")
        load_inventory()
        print("inventory loaded")
        load_top_inventory()
        print("top loaded")
    except ValueError as ve:
        return str(ve)


if __name__ == '__main__':
    sys.exit(main())

