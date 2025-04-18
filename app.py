from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os

app = Flask(__name__)

def get_items():
    connection = sqlite3.connect('main.db')
    cursor = connection.cursor()
    cursor.execute("SELECT name, unit, current_stock, alert_threshold FROM items")
    items = cursor.fetchall()
    connection.close()
    return items

@app.route('/')
def index():
    items = get_items()
    low_stock_items = [item for item in items if item[2] < item[3]]  # 在庫が閾値を下回る商品を抽出
    return render_template('index.html', items=items, low_stock_items=low_stock_items)

def update_stock(item_id, quantity, movement_type):
    connection = sqlite3.connect('main.db')
    cursor = connection.cursor()

    # Update stock_movements table
    cursor.execute(
        "INSERT INTO stock_movements (item_id, movement_type, quantity) VALUES (?, ?, ?)",
        (item_id, movement_type, quantity)
    )

    # Update items table
    if movement_type == 'in':
        cursor.execute(
            "UPDATE items SET current_stock = current_stock + ? WHERE id = ?",
            (quantity, item_id)
        )
    elif movement_type == 'out':
        cursor.execute(
            "UPDATE items SET current_stock = current_stock - ? WHERE id = ?",
            (quantity, item_id)
        )

    connection.commit()
    connection.close()

@app.route('/update_stock', methods=['POST'])
def update_stock_route():
    item_id = request.form['item_id']
    quantity = float(request.form['quantity'])
    movement_type = request.form['movement_type']

    update_stock(item_id, quantity, movement_type)
    return redirect(url_for('index'))

@app.route('/edit_item/<int:item_id>', methods=['GET', 'POST'])
def edit_item(item_id):
    connection = sqlite3.connect('main.db')
    cursor = connection.cursor()

    if request.method == 'POST':
        name = request.form['name']
        unit = request.form['unit']
        alert_threshold = float(request.form['alert_threshold'])

        # Update the item in the database
        cursor.execute(
            "UPDATE items SET name = ?, unit = ?, alert_threshold = ? WHERE id = ?",
            (name, unit, alert_threshold, item_id)
        )
        connection.commit()
        connection.close()
        return redirect(url_for('index'))

    # Fetch the current item details
    cursor.execute("SELECT name, unit, alert_threshold FROM items WHERE id = ?", (item_id,))
    item = cursor.fetchone()
    connection.close()

    return render_template('edit_item.html', item=item, item_id=item_id)

# 🔧 ここがRender用の起動設定です！
