import csv
import os
import sqlite3

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))


con = sqlite3.connect('inventory.db')
con.execute("DELETE FROM INVENTORY")
cur = con.cursor()

with open(__location__ + '/inventory.csv','r') as fin: # `with` statement available in 2.5+
    # csv.DictReader uses first line in file for column headings by default
    dr = csv.DictReader(fin) # comma is default delimiter
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

insert_into_command = """INSERT INTO inventory (
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

