import os
import sqlite3



create_inventory_command_string = """CREATE TABLE IF NOT EXISTS inventory (
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
);"""

con = sqlite3.connect('./inventory.db')
with con:
    con.execute(create_inventory_command_string)