import csv
from fileinput import filename
import os
import sqlite3
import time
import tkinter
from tkinter.filedialog import askopenfilename, asksaveasfilename
from dif import *

tkinter.Tk().withdraw()

__location__ = os.path.realpath(os.path.join(
    os.getcwd(), os.path.dirname(__file__)))
db_path = os.path.join(__location__, 'inventory.db')

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
        invoiceitemid TEXT PRIMARY KEY,
        description TEXT,
        compute_0003,
        compute_0004
    );
    """
    con = sqlite3.connect(db_path)
    with con:
        con.execute(create_inventory_command_string)
        con.execute(create_top_inventory_command_string)


def load_inventory():

    inv_path = askopenfilename(title="Select inventory file", filetypes=[("csv, *.csv")])
    con = sqlite3.connect(db_path)
    con.execute("DELETE FROM inventory")
    cur = con.cursor()
    with open(inv_path, 'r') as fin:  # `with` statement available in 2.5+
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
    top_path = askopenfilename(title="Select top inventory file", filetypes=[("dif, *.dif")])
    con = sqlite3.connect(db_path)
    con.execute("DELETE FROM top_inventory")
    cur = con.cursor()
    with open(top_path, 'r') as fin:
        dr = DIF(fin)
        to_db = [
            (
                i[0],
                i[1],
                i[2],
                i[3]
            ) for i in dr.data
        ]

    insert_into_command = """
    INSERT OR IGNORE INTO top_inventory (
    invoiceitemid,
    description,
    compute_0003,
    compute_0004)
    VALUES (?,?,?,?);
    """
    cur.executemany(insert_into_command, to_db)
    con.commit()
    con.close()


def write_joined_data():
    outfile_path = asksaveasfilename(title="Save output as", filetypes=[("csv, *.csv")], defaultextension=[("csv, *.csv")])
    #outfile_path = askopenfilename(title="Save output as", filetypes=[("csv, *.csv")])
    join_command = """
    select 
        i.invoitem_invoice_item_id as "Invoice Item ID",
        i.item_cost as "Item Cost",
        i.total_cost as "Total Cost",
        i.markup as "Markup",
        i.s_uom as "Item Quantifier",
        i.auto_calculate,
        i.loc_group,
        i.vendor_name as "Vendor Name",
        i.loc_id,
        i.average_cost as "Average Cost",
        i.last_cost as "Last Cost",
        i.inv_desc as "Item Description",
        (
            select
                t.description
            where
                i.inv_desc != t.description
        ) as "AKA",
        i.quanitytunitprice as "Quantity Unit Price",
        i.last_purchase_date as "Last Purchased",
        i.on_hand as "On Hand",
        t.compute_0003,
        t.compute_0004
    from 
        top_inventory as t
    join 
        inventory as i
    on 
        i.invoitem_invoice_item_id = t.invoiceitemid
    order by
        i.inv_desc
    """
    con = sqlite3.connect(db_path)
    cur = con.cursor()
    cur.execute(join_command)
    #output_file_name = "combined_table_" + str(round(time.time())) + ".csv"
    #outfile_path = os.path.join(__location__, output_file_name)
    with open(outfile_path, "w", newline='') as outfile:
        writer = csv.writer(outfile, delimiter="|")
        writer.writerow([i[0] for i in cur.description])
        writer.writerows(cur)
