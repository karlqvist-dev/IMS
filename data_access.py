import os
import json

# Define the directory path
data_dir = 'data'

def read_inventory_data():

    # Load data from products.json and warehouses.json for ID-to-Name mapping
    products_data = {}
    warehouses_data = {}

    with open(os.path.join(data_dir, 'products.json'), encoding = "utf-8") as products_file:
        products_data = {item['id']: item['name'] for item in json.load(products_file)}

    with open(os.path.join(data_dir, 'warehouses.json'), encoding = "utf-8") as warehouses_file:
        warehouses_data = {item['id']: item['city'] for item in json.load(warehouses_file)}

    # Load inventory.json
    with open(os.path.join(data_dir, 'inventory.json'), encoding = "utf-8") as inventory_file:
        inventory_data = json.load(inventory_file)

    # Substitute product and warehouse IDs with names
    for item in inventory_data:
        item['product_name'] = products_data.get(item['product_id'], 'N/A')
        item['warehouse_city'] = warehouses_data.get(item['warehouse_id'], 'N/A')

    return inventory_data

def read_products():
    with open(os.path.join(data_dir, 'products.json'), encoding = "utf-8") as products_file:
        return json.load(products_file)

def read_warehouses():
    with open(os.path.join(data_dir, 'warehouses.json'), encoding = "utf-8") as warehouses_file:
        return json.load(warehouses_file)

def read_deliveries_data():
    products_data = {}
    warehouses_data = {}

    with open(os.path.join(data_dir, 'products.json'), encoding="utf-8") as products_file:
        products_data = {item['id']: item['name'] for item in json.load(products_file)}

    with open(os.path.join(data_dir, 'warehouses.json'), encoding="utf-8") as warehouses_file:
        warehouses_data = {item['id']: item['city'] for item in json.load(warehouses_file)}

    with open(os.path.join(data_dir, 'deliveries.json'), encoding="utf-8") as deliveries_file:
        deliveries_data = json.load(deliveries_file)

    # Add product and warehouse names to each delivery entry
    for delivery in deliveries_data:
        delivery['product_name'] = products_data.get(delivery['product_id'], 'N/A')
        delivery['warehouse_name'] = warehouses_data.get(delivery['warehouse_id'], 'N/A')

    # Sort deliveries by incoming status, date, and id where date is the same, to ensure consistency in presentation of data to the user
    deliveries_data.sort(key=lambda x: (x['incoming'], x['date'], x['id']), reverse=True)

    return deliveries_data


def update_inventory(product_id, warehouse_id, date, quantity, incoming):
    # Read existing inventory data
    with open(os.path.join(data_dir, 'inventory.json')) as inventory_file:
        inventory_data = json.load(inventory_file)

    # Find the relevant inventory item based on product and warehouse
    inventory_item = None
    for item in inventory_data:
        if item['product_id'] == product_id and item['warehouse_id'] == int(warehouse_id):
            inventory_item = item
            break

    if inventory_item:
        # Update the existing inventory amount
        inventory_item['amount'] += int(quantity)

        # Write back the updated inventory data
        with open(os.path.join(data_dir, 'inventory.json'), 'w') as inventory_file:
            json.dump(inventory_data, inventory_file, indent=2)

    else:
        # When the inventory item is not found, create a new item
        new_inventory_item = {
            "id": len(inventory_data) + 1,
            "product_id": product_id,
            "warehouse_id": int(warehouse_id),
            "amount": int(quantity)
        }

        # Append the new inventory item to the inventory data
        inventory_data.append(new_inventory_item)

        # Write back the updated inventory data
        with open(os.path.join(data_dir, 'inventory.json'), 'w') as inventory_file:
            json.dump(inventory_data, inventory_file, indent=2)


    # Read existing deliveries data
    with open(os.path.join(data_dir, 'deliveries.json')) as deliveries_file:
        deliveries_data = json.load(deliveries_file)

    # Create a new delivery record
    new_delivery = {
        "id": len(deliveries_data) + 1,
        "date": None if incoming else date,
        "incoming": incoming,
        "product_id": product_id,
        "warehouse_id": int(warehouse_id),
        "amount": int(quantity)
    }

    # Append the new delivery record to the deliveries data
    deliveries_data.append(new_delivery)

    # Write back the updated deliveries data
    with open(os.path.join(data_dir, 'deliveries.json'), 'w') as deliveries_file:
        json.dump(deliveries_data, deliveries_file, indent=2)

    return inventory_data  # Return the updated inventory data

# Update the delivery date for incoming deliveries and set the incoming flag to False
def update_incoming_delivery(delivery_id, date):
    # Read existing deliveries data
    with open(os.path.join(data_dir, 'deliveries.json')) as deliveries_file:
        deliveries_data = json.load(deliveries_file)

    # Find the relevant delivery item based on the ID
    for delivery in deliveries_data:
        if delivery['id'] == delivery_id and delivery['incoming']:
            # Update the delivery date and set the incoming flag to False
            delivery['date'] = date
            delivery['incoming'] = False
            break

    # Write back the updated deliveries data
    with open(os.path.join(data_dir, 'deliveries.json'), 'w') as deliveries_file:
        json.dump(deliveries_data, deliveries_file, indent=2)
