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

insert_into_inventory_command = """
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

insert_into_top_inventory_command = """
    INSERT OR IGNORE INTO top_inventory (
    invoiceitemid,
    description,
    compute_0003,
    compute_0004)
    VALUES (?,?,?,?);
    """

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
