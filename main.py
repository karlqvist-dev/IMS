from flask import Flask, render_template, request, redirect, url_for
import data_access
import os

app = Flask(__name__)

# Routes for navigation

@app.route("/")
def index():
    inventory_data = data_access.read_inventory_data()
    products = data_access.read_products()
    warehouses = data_access.read_warehouses()
    return render_template("index.html", inventory_data=inventory_data, products=products, warehouses=warehouses)

@app.route("/deliveries")
def deliveries():
    deliveries_data = data_access.read_deliveries_data()
    incoming_deliveries = [delivery for delivery in deliveries_data if delivery['incoming']]
    return render_template("deliveries.html", deliveries_data=deliveries_data, incoming_deliveries=incoming_deliveries)




# Routes for data update

@app.route("/update_inventory", methods=["POST"])
def update_inventory():
    # Access form data
    product_id = request.form.get('product')
    warehouse_id = request.form.get('warehouse')
    date = request.form.get('date')
    quantity = request.form.get('quantity')
    incoming = 'incoming' in request.form

    # If any of the required fields are missing, redirect back to the index page
    if not (product_id and warehouse_id and quantity):
        return redirect(url_for('index'))

    # Update inventory
    data_access.update_inventory(product_id, warehouse_id, date, quantity, incoming)

    # Redirect back to the index page with updated inventory
    return redirect(url_for('index'))

@app.route("/update_incoming_delivery", methods=["POST"])
def update_incoming_delivery():
    delivery_id = int(request.form.get('delivery_id'))
    date = request.form.get('date')

    # If any of the required fields are missing, redirect back to the index page
    if not (delivery_id and date):
        return redirect(url_for('deliveries'))

    # Update the delivery in data_access.py
    data_access.update_incoming_delivery(delivery_id, date)

    # Redirect back to the deliveries page
    return redirect(url_for('deliveries'))



# Route for data export

@app.route("/export", methods=["GET"])
def export_data():
    sheet_type = request.args.get('type')

    if sheet_type == 'inventory':
        # Fetch inventory data (replace this with your actual inventory data retrieval logic)
        inventory_data = data_access.read_inventory_data()

        # Edit the data such that warehouse_city becomes Färdigvarulager, product_name becomes Produkt, amount becomes Lagersaldo and the remaining attributes are removed
        for item in inventory_data:
            item['Warehouse'] = item['warehouse_city']
            item['Product'] = item['product_name']
            item['Amount'] = item['amount']
            item.pop('warehouse_city')
            item.pop('product_name')
            item.pop('amount')
            item.pop('product_id')
            item.pop('warehouse_id')
            item.pop('id')

        return inventory_data

    elif sheet_type == 'deliveries':
        # Fetch deliveries data (replace this with your actual deliveries data retrieval logic)
        deliveries_data = data_access.read_deliveries_data()

        # Edit the data such that date becomes Datum, product_name becomes Produkt, warehouse_name becomes Till/från, amount becomes Antal, incoming becomes Ingående and the remaining attributes are removed
        # Change the values of Ingående to Ja/Nej
        for item in deliveries_data:
            item['Date'] = item['date']
            item['Product'] = item['product_name']
            item['Warehouse'] = item['warehouse_name']
            item['Amount'] = item['amount']
            item['Incoming'] = 'Ja' if item['incoming'] else 'Nej'
            item.pop('date')
            item.pop('product_name')
            item.pop('warehouse_name')
            item.pop('amount')
            item.pop('incoming')
            item.pop('product_id')
            item.pop('warehouse_id')
            item.pop('id')

        return deliveries_data

    else:
        return [
            {
                "error": "Unknown sheet type"
            }
        ]




# Entry point for the application
# Debug mode is used as this application is intended for testing purposes
if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000))
