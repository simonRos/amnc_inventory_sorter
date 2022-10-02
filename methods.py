import csv
import os
import sqlite3

__location__ = os.path.realpath(os.path.join(
    os.getcwd(), os.path.dirname(__file__)))


def create_db():
    create_inventory_command_string = """
    CREATE TABLE IF NOT EXISTS inventory (
    invoitem_invoice_item_id TEXT    UNIQUE
                                        PRIMARY KEY,
    item_cost                REAL    DEFAULT (0.0),
    total_cost               REAL    DEFAULT (0.0),
    markup                   REAL    DEFAULT (0.0),
    s_uom                    TEXT,
    auto_calculate           INTEGER,
    loc_group                TEXT,
    vendor_name              TEXT,
    loc_id                   TEXT,
    average_cost             REAL,
    last_cost                REAL    DEFAULT (0.0),
    inv_desc                 TEXT,
    quanitytunitprice        REAL    DEFAULT (0.0),
    last_purchase_date       DATE,
    on_hand                  REAL    DEFAULT (0.0) 
    );
    """

    create_top_inventory_command_string = """
    CREATE TABLE IF NOT EXISTS top_inventory (
        invoitem_invoice_item_id TEXT PRIMARY KEY
                                    UNIQUE,
        inv_desc                 TEXT,
        col_3,
        col_4
    );
    """

    con = sqlite3.connect('./inventory.db')
    with con:
        con.execute(create_inventory_command_string)
        con.execute(create_top_inventory_command_string)


def load_inventory():
    con = sqlite3.connect('inventory.db')
    con.execute("DELETE FROM inventory")
    cur = con.cursor()

    with open(__location__ + '/inventory.csv', 'r') as fin:  # `with` statement available in 2.5+
        # csv.DictReader uses first line in file for column headings by default
        dr = csv.DictReader(fin)  # comma is default delimiter
        to_db = [
            (
                i['invoitem_invoice_item_id'],
                i['item_cost'],
                i['total_cost'],
                i['markup'],
                i['s_uom'],
                i['auto_calculate'],
                i['loc_group'],
                i['vendor_name'],
                i['loc_id'],
                i['average_cost'],
                i['last_cost'],
                i['inv_desc'],
                i['quanitytunitprice'],
                i['last_purchase_date'],
                i['on_hand']
            ) for i in dr
        ]

    insert_into_command = """
    INSERT INTO inventory (
    invoitem_invoice_item_id,
    item_cost,
    total_cost,
    markup,
    s_uom,
    auto_calculate,
    loc_group,
    vendor_name,
    loc_id,
    average_cost,
    last_cost,
    inv_desc,
    quanitytunitprice,
    last_purchase_date,
    on_hand)
    VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);
    """

    cur.executemany(insert_into_command, to_db)
    con.commit()
    con.close()


def load_top_inventory():
    con = sqlite3.connect('inventory.db')
    con.execute("DELETE FROM top_inventory")
    cur = con.cursor()

    with open(__location__ + '/top.xls', 'r') as fin:
        dr = csv.DictReader(fin)
        to_db = [
            (
                i['invoitem_invoice_item_id'],
                i['inv_desc'],
                i['col_3'],
                i['col_4']
            ) for i in dr
        ]

    insert_into_command = """
    INSERT INTO inventory (
    invoitem_invoice_item_id,
    inv_desc,
    col_3,
    col_4)
    VALUES (?,?,?,?);
    """

    cur.executemany(insert_into_command, to_db)
    con.commit()
    con.close()
