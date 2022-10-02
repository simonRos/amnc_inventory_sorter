import csv
from fileinput import filename
import os
import sqlite3
import tkinter
from dif import *
from sqlite_commands import *
from tkinter.filedialog import askopenfilename, asksaveasfilename


tkinter.Tk().withdraw()

__location__ = os.path.realpath(os.path.join(
    os.getcwd(), os.path.dirname(__file__)))
db_path = os.path.join(__location__, 'inventory.db')


def create_db():
    '''Create sqlite database with needed tables'''
    con = sqlite3.connect(db_path)
    with con:
        con.execute(create_inventory_command_string)
        con.execute(create_top_inventory_command_string)


def load_inventory():
    '''Load inventory file into db'''
    inv_path = askopenfilename(
        title="Select inventory file", filetypes=[("csv, *.csv")])
    con = sqlite3.connect(db_path)
    con.execute("DELETE FROM inventory")
    cur = con.cursor()
    with open(inv_path, 'r') as fin:
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

    cur.executemany(insert_into_inventory_command, to_db)
    con.commit()
    con.close()


def load_top_inventory():
    '''Load top selling inventory'''
    top_path = askopenfilename(
        title="Select top inventory file", filetypes=[("dif, *.dif")])
    con = sqlite3.connect(db_path)
    con.execute("DELETE FROM top_inventory")
    cur = con.cursor()
    with open(top_path, 'r') as fin:
        # Dear future people,
        # This file comes in a format called Data Interchange Format
        # https://en.wikipedia.org/wiki/Data_Interchange_Format
        # It is difficult to parse, not human readable, and as far as I could tell not supported by vanilla python packages
        # To parse this file, I took this:
        # https://github.com/Solomoriah/dif
        # and made some changes to get it to work with python 3
        # The linked package claims that it works with NAVY DIF but it seems to work fine with DIF.
        dr = DIF(fin)
        to_db = [
            (
                i[0],
                i[1],
                i[2],
                i[3]
            ) for i in dr.data
        ]

    cur.executemany(insert_into_top_inventory_command, to_db)
    con.commit()
    con.close()


def write_joined_data():
    '''Run the join command and write out to a csv file'''
    outfile_path = asksaveasfilename(title="Save output as", filetypes=[
                                     ("csv, *.csv")], defaultextension=[("csv, *.csv")])
    con = sqlite3.connect(db_path)
    cur = con.cursor()
    cur.execute(join_command)
    with open(outfile_path, "w", newline='') as outfile:
        writer = csv.writer(outfile, delimiter="|")
        writer.writerow([i[0] for i in cur.description])
        writer.writerows(cur)
