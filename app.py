import os
from datetime import datetime, timedelta
from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from bson.objectid import ObjectId

from config import Config
from database import get_db, to_object_id
from seed import seed_database
from utils.helpers import (
    login_required,
    admin_required,
    format_currency,
    format_datetime,
    get_stock_status,
    generate_invoice_number
)

app = Flask(__name__)
app.config.from_object(Config)

# Automatically ensure demo data is seeded upon first startup
with app.app_context():
    try:
        seed_database(force=False)
    except Exception as e:
        print(f"[APP] Initial database seed notice: {e}")

# -------------------------------------------------------------
# Global Template Context Processor (Header & Sidebar Data)
# -------------------------------------------------------------
@app.context_processor
def inject_global_data():
    """Provides shop profile and active low-stock badge count to all templates."""
    db = get_db()
    profile = db.settings.find_one() or {
        "shop_name": "APNA BAZAR",
        "owner_name": "Akshay Khapare",
        "phone": "+91 98201 23456",
        "email": "apnabazar.mumbai@gmail.com",
        "address": "Shop 4, Station Road, Dadar West, Mumbai - 400028",
        "gst_number": "27AAACG1234F1Z5",
        "tax_rate": 5.0
    }
    
    # Calculate count of items with qty <= minimum_stock
    all_products = list(db.products.find())
    low_count = sum(1 for p in all_products if p.get("quantity", 0) <= p.get("minimum_stock", 0))
    
    return {
        "shop_profile": profile,
        "low_stock_count": low_count
    }


# =============================================================
# MODULE 1: Admin Login & Authentication
# =============================================================
@app.route("/login", methods=["GET", "POST"])
def login():
    """Admin and Staff session-based login."""
    if "user_id" in session:
        return redirect(url_for("dashboard"))

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()

        db = get_db()
        user = db.users.find_one({"$or": [{"username": username}, {"email": username}]})

        if user and check_password_hash(user.get("password_hash", ""), password):
            session["user_id"] = str(user["_id"])
            session["username"] = user["username"]
            session["user_name"] = user.get("name", user["username"])
            session["user_role"] = user.get("role", "Staff")
            flash(f"Welcome back, {session['user_name']}!", "success")
            return redirect(url_for("dashboard"))
        else:
            flash("Invalid username or password. Please try again.", "error")

    return render_template("login.html")

@app.route("/logout")
def logout():
    """Clear session and log out."""
    session.clear()
    flash("You have been successfully logged out.", "success")
    return redirect(url_for("login"))


# =============================================================
# MODULE 2: User Management (Admin Only)
# =============================================================
@app.route("/users")
@admin_required
def users():
    """List all registered system users."""
    db = get_db()
    all_users = list(db.users.find().sort("created_at", -1))
    return render_template("users/index.html", users=all_users)

@app.route("/users/add", methods=["GET", "POST"])
@admin_required
def add_user():
    """Add new staff or admin user."""
    db = get_db()
    if request.method == "POST":
        username = request.form.get("username", "").strip().lower()
        password = request.form.get("password", "").strip()
        name = request.form.get("name", "").strip()
        role = request.form.get("role", "Staff")
        phone = request.form.get("phone", "").strip()
        email = request.form.get("email", "").strip()

        if db.users.find_one({"username": username}):
            flash("Username is already taken. Choose another.", "error")
            return render_template("users/form.html", edit_user=None)

        new_user = {
            "name": name,
            "username": username,
            "password_hash": generate_password_hash(password),
            "role": role,
            "phone": phone,
            "email": email,
            "status": "Active",
            "created_at": datetime.now()
        }
        db.users.insert_one(new_user)
        flash("New user account created successfully.", "success")
        return redirect(url_for("users"))

    return render_template("users/form.html", edit_user=None)

@app.route("/users/edit/<user_id>", methods=["GET", "POST"])
@admin_required
def edit_user(user_id):
    """Edit existing user details."""
    db = get_db()
    obj_id = to_object_id(user_id)
    user = db.users.find_one({"_id": obj_id})
    if not user:
        flash("User not found.", "error")
        return redirect(url_for("users"))

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        role = request.form.get("role", "Staff")
        phone = request.form.get("phone", "").strip()
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "").strip()

        update_fields = {
            "name": name,
            "role": role,
            "phone": phone,
            "email": email
        }
        if password:
            update_fields["password_hash"] = generate_password_hash(password)

        db.users.update_one({"_id": obj_id}, {"$set": update_fields})
        flash("User details updated successfully.", "success")
        return redirect(url_for("users"))

    return render_template("users/form.html", edit_user=user)

@app.route("/users/delete/<user_id>")
@admin_required
def delete_user(user_id):
    """Delete a user account."""
    db = get_db()
    obj_id = to_object_id(user_id)
    user = db.users.find_one({"_id": obj_id})
    if user and user.get("username") == "admin":
        flash("Primary admin account cannot be deleted.", "error")
    else:
        db.users.delete_one({"_id": obj_id})
        flash("User deleted successfully.", "success")
    return redirect(url_for("users"))


# =============================================================
# MODULE 3: Dashboard (Real MongoDB Metrics & Sales Chart)
# =============================================================
@app.route("/")
@app.route("/dashboard")
@login_required
def dashboard():
    """Main dashboard with genuine database statistics and Chart.js 7-day trend."""
    db = get_db()

    # Calculate Today's Sales
    today_start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    today_sales_cursor = db.sales.find({
        "status": {"$ne": "Cancelled"},
        "created_at": {"$gte": today_start}
    })
    today_sales_list = list(today_sales_cursor)
    today_revenue = sum(s.get("grand_total", 0) for s in today_sales_list)
    today_bills_count = len(today_sales_list)

    # Counts
    total_products_count = db.products.count_documents({})
    total_categories_count = db.categories.count_documents({})
    total_customers_count = db.customers.count_documents({})

    # Recent Sales (latest 5)
    recent_sales = list(db.sales.find().sort("created_at", -1).limit(5))

    # Low Stock Products (qty <= minimum_stock)
    all_products = list(db.products.find())
    category_map = {str(c["_id"]): c["name"] for c in db.categories.find()}
    
    low_stock_products = []
    for p in all_products:
        p["category_name"] = category_map.get(str(p.get("category_id")), "General")
        if p.get("quantity", 0) <= p.get("minimum_stock", 0):
            low_stock_products.append(p)

    # 7-Day Chart.js Trend
    chart_labels = []
    chart_values = []
    for i in range(6, -1, -1):
        day_date = datetime.now() - timedelta(days=i)
        day_start = day_date.replace(hour=0, minute=0, second=0, microsecond=0)
        day_end = day_date.replace(hour=23, minute=59, second=59, microsecond=999999)
        day_sales = list(db.sales.find({
            "status": {"$ne": "Cancelled"},
            "created_at": {"$gte": day_start, "$lte": day_end}
        }))
        chart_labels.append(day_date.strftime("%d %b"))
        chart_values.append(round(sum(s.get("grand_total", 0) for s in day_sales), 2))

    return render_template(
        "dashboard.html",
        today_sales_formatted=format_currency(today_revenue),
        today_bills_count=today_bills_count,
        total_products_count=total_products_count,
        total_categories_count=total_categories_count,
        total_customers_count=total_customers_count,
        low_stock_count=len(low_stock_products),
        recent_sales=recent_sales,
        low_stock_products=low_stock_products[:6],
        chart_labels=chart_labels,
        chart_values=chart_values
    )


# =============================================================
# MODULE 4 & 30: Shop Profile & Settings
# =============================================================
@app.route("/settings", methods=["GET", "POST"])
@login_required
def settings():
    """Shop profile configuration and preferences."""
    db = get_db()
    if request.method == "POST":
        shop_name = request.form.get("shop_name", "").strip()
        owner_name = request.form.get("owner_name", "").strip()
        phone = request.form.get("phone", "").strip()
        email = request.form.get("email", "").strip()
        address = request.form.get("address", "").strip()
        gst_number = request.form.get("gst_number", "").strip()
        tax_rate = float(request.form.get("tax_rate", 5.0) or 5.0)

        db.settings.update_one(
            {},
            {"$set": {
                "shop_name": shop_name,
                "owner_name": owner_name,
                "phone": phone,
                "email": email,
                "address": address,
                "gst_number": gst_number,
                "tax_rate": tax_rate,
                "updated_at": datetime.now()
            }},
            upsert=True
        )
        flash("Shop profile and invoice settings saved successfully.", "success")
        return redirect(url_for("settings"))

    profile = db.settings.find_one()
    return render_template("settings/index.html", profile=profile)

@app.route("/settings/reset-demo")
@admin_required
def reset_demo_data():
    """Reloads the clean Indian local shop demo dataset."""
    seed_database(force=True)
    flash("Demo database has been successfully reseeded with default records.", "success")
    return redirect(url_for("dashboard"))


# =============================================================
# MODULE 5: Category Management (CRUD)
# =============================================================
@app.route("/categories")
@login_required
def categories():
    """List all categories."""
    db = get_db()
    all_cats = list(db.categories.find().sort("name", 1))
    # Count products per category
    for cat in all_cats:
        cat["product_count"] = db.products.count_documents({"category_id": cat["_id"]})
        cat["created_at_formatted"] = format_datetime(cat.get("created_at"), "%d %b %Y")
    return render_template("categories/index.html", categories=all_cats)

@app.route("/categories/add", methods=["GET", "POST"])
@login_required
def add_category():
    """Add a new product category."""
    db = get_db()
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        description = request.form.get("description", "").strip()

        if db.categories.find_one({"name": {"$regex": f"^{name}$", "$options": "i"}}):
            flash(f"Category '{name}' already exists.", "error")
            return render_template("categories/form.html", category=None)

        db.categories.insert_one({
            "name": name,
            "description": description,
            "created_at": datetime.now()
        })
        flash(f"Category '{name}' added successfully.", "success")
        return redirect(url_for("categories"))

    return render_template("categories/form.html", category=None)

@app.route("/categories/edit/<cat_id>", methods=["GET", "POST"])
@login_required
def edit_category(cat_id):
    """Edit existing category."""
    db = get_db()
    obj_id = to_object_id(cat_id)
    cat = db.categories.find_one({"_id": obj_id})
    if not cat:
        flash("Category not found.", "error")
        return redirect(url_for("categories"))

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        description = request.form.get("description", "").strip()

        db.categories.update_one(
            {"_id": obj_id},
            {"$set": {"name": name, "description": description, "updated_at": datetime.now()}}
        )
        flash("Category updated successfully.", "success")
        return redirect(url_for("categories"))

    return render_template("categories/form.html", category=cat)

@app.route("/categories/delete/<cat_id>")
@login_required
def delete_category(cat_id):
    """Delete a category if no products belong to it."""
    db = get_db()
    obj_id = to_object_id(cat_id)
    count = db.products.count_documents({"category_id": obj_id})
    if count > 0:
        flash(f"Cannot delete category: {count} product(s) are linked to it. Reassign them first.", "error")
    else:
        db.categories.delete_one({"_id": obj_id})
        flash("Category deleted successfully.", "success")
    return redirect(url_for("categories"))


# =============================================================
# MODULE 6, 7 & 12: Product Management, Product Search & Barcode
# =============================================================
@app.route("/products")
@login_required
def products():
    """List products with search by name, product code/barcode, or category."""
    db = get_db()
    query = request.args.get("q", "").strip()
    selected_category = request.args.get("category_id", "").strip()

    filter_dict = {}
    if query:
        filter_dict["$or"] = [
            {"product_name": {"$regex": query, "$options": "i"}},
            {"product_code": {"$regex": query, "$options": "i"}}
        ]
    if selected_category:
        filter_dict["category_id"] = to_object_id(selected_category)

    product_list = list(db.products.find(filter_dict).sort("product_name", 1))

    # Enrich with category and supplier names
    cat_map = {str(c["_id"]): c["name"] for c in db.categories.find()}
    sup_map = {str(s["_id"]): s["name"] for s in db.suppliers.find()}

    for p in product_list:
        p["category_name"] = cat_map.get(str(p.get("category_id")), "General")
        p["supplier_name"] = sup_map.get(str(p.get("supplier_id")), "Local Vendor")

    all_categories = list(db.categories.find().sort("name", 1))
    return render_template(
        "products/index.html",
        products=product_list,
        categories=all_categories,
        query=query,
        selected_category=selected_category
    )

@app.route("/products/add", methods=["GET", "POST"])
@login_required
def add_product():
    """Create a new product."""
    db = get_db()
    if request.method == "POST":
        product_name = request.form.get("product_name", "").strip()
        product_code = request.form.get("product_code", "").strip().upper()
        category_id = to_object_id(request.form.get("category_id"))
        supplier_id = to_object_id(request.form.get("supplier_id"))
        purchase_price = float(request.form.get("purchase_price", 0) or 0)
        selling_price = float(request.form.get("selling_price", 0) or 0)
        quantity = int(request.form.get("quantity", 0) or 0)
        minimum_stock = int(request.form.get("minimum_stock", 5) or 5)
        expiry_date = request.form.get("expiry_date", "").strip()

        # Check unique product code
        if db.products.find_one({"product_code": product_code}):
            flash(f"Product code '{product_code}' already exists. Please choose a unique code.", "error")
            return redirect(url_for("add_product"))

        new_product = {
            "product_name": product_name,
            "product_code": product_code,
            "category_id": category_id,
            "supplier_id": supplier_id,
            "purchase_price": purchase_price,
            "selling_price": selling_price,
            "quantity": quantity,
            "minimum_stock": minimum_stock,
            "expiry_date": expiry_date,
            "created_at": datetime.now()
        }
        res = db.products.insert_one(new_product)

        # Record initial stock movement if quantity > 0
        if quantity > 0:
            db.stock_movements.insert_one({
                "product_id": res.inserted_id,
                "product_name": product_name,
                "type": "IN",
                "quantity": quantity,
                "reason": "Initial Stock Setup",
                "reference_id": "SETUP",
                "created_at": datetime.now()
            })

        flash(f"Product '{product_name}' added successfully.", "success")
        return redirect(url_for("products"))

    # Auto generate recommended next code
    count = db.products.count_documents({})
    default_code = f"PRD-{1001 + count}"
    categories = list(db.categories.find().sort("name", 1))
    suppliers = list(db.suppliers.find().sort("name", 1))

    return render_template(
        "products/form.html",
        product=None,
        default_code=default_code,
        categories=categories,
        suppliers=suppliers
    )

@app.route("/products/edit/<prd_id>", methods=["GET", "POST"])
@login_required
def edit_product(prd_id):
    """Edit existing product."""
    db = get_db()
    obj_id = to_object_id(prd_id)
    product = db.products.find_one({"_id": obj_id})
    if not product:
        flash("Product not found.", "error")
        return redirect(url_for("products"))

    if request.method == "POST":
        product_name = request.form.get("product_name", "").strip()
        product_code = request.form.get("product_code", "").strip().upper()
        category_id = to_object_id(request.form.get("category_id"))
        supplier_id = to_object_id(request.form.get("supplier_id"))
        purchase_price = float(request.form.get("purchase_price", 0) or 0)
        selling_price = float(request.form.get("selling_price", 0) or 0)
        quantity = int(request.form.get("quantity", 0) or 0)
        minimum_stock = int(request.form.get("minimum_stock", 5) or 5)
        expiry_date = request.form.get("expiry_date", "").strip()

        # Check unique product code if changed
        existing = db.products.find_one({"product_code": product_code, "_id": {"$ne": obj_id}})
        if existing:
            flash(f"Product code '{product_code}' is taken by another product.", "error")
            return redirect(url_for("edit_product", prd_id=prd_id))

        db.products.update_one(
            {"_id": obj_id},
            {"$set": {
                "product_name": product_name,
                "product_code": product_code,
                "category_id": category_id,
                "supplier_id": supplier_id,
                "purchase_price": purchase_price,
                "selling_price": selling_price,
                "quantity": quantity,
                "minimum_stock": minimum_stock,
                "expiry_date": expiry_date,
                "updated_at": datetime.now()
            }}
        )
        flash("Product updated successfully.", "success")
        return redirect(url_for("products"))

    categories = list(db.categories.find().sort("name", 1))
    suppliers = list(db.suppliers.find().sort("name", 1))
    return render_template(
        "products/form.html",
        product=product,
        categories=categories,
        suppliers=suppliers
    )

@app.route("/products/delete/<prd_id>")
@login_required
def delete_product(prd_id):
    """Delete a product."""
    db = get_db()
    obj_id = to_object_id(prd_id)
    db.products.delete_one({"_id": obj_id})
    flash("Product removed from catalog.", "success")
    return redirect(url_for("products"))


# =============================================================
# MODULE 8 & 9: Stock Management & Low Stock Alert
# =============================================================
@app.route("/stock")
@login_required
def stock_management():
    """Overview of all stock levels and statuses."""
    db = get_db()
    all_products = list(db.products.find().sort("quantity", 1))
    cat_map = {str(c["_id"]): c["name"] for c in db.categories.find()}
    for p in all_products:
        p["category_name"] = cat_map.get(str(p.get("category_id")), "General")

    return render_template(
        "products/stock.html",
        products=all_products,
        only_low=False
    )

@app.route("/stock/low")
@login_required
def low_stock():
    """Module 9: Low stock alerts (quantity <= minimum_stock)."""
    db = get_db()
    all_products = list(db.products.find().sort("quantity", 1))
    cat_map = {str(c["_id"]): c["name"] for c in db.categories.find()}

    low_items = []
    for p in all_products:
        p["category_name"] = cat_map.get(str(p.get("category_id")), "General")
        if p.get("quantity", 0) <= p.get("minimum_stock", 0):
            low_items.append(p)

    return render_template(
        "products/stock.html",
        products=low_items,
        only_low=True
    )


# =============================================================
# MODULE 10: Stock Adjustment (Manual Increase/Decrease with Reason)
# =============================================================
@app.route("/stock/adjustment", methods=["GET", "POST"])
@login_required
def stock_adjustment():
    """Module 10: Manually increase or decrease product stock with audit trail."""
    db = get_db()
    selected_prd_id = request.args.get("product_id", "")

    if request.method == "POST":
        product_id = to_object_id(request.form.get("product_id"))
        action_type = request.form.get("action_type")  # INCREASE or DECREASE
        qty_change = int(request.form.get("quantity", 0) or 0)
        reason = request.form.get("reason", "").strip()
        note = request.form.get("note", "").strip()

        product = db.products.find_one({"_id": product_id})
        if not product:
            flash("Product not found.", "error")
            return redirect(url_for("stock_adjustment"))

        current_qty = product.get("quantity", 0)
        if action_type == "DECREASE":
            if qty_change > current_qty:
                flash(f"Cannot decrease by {qty_change}. Current stock is only {current_qty}.", "error")
                return redirect(url_for("stock_adjustment", product_id=str(product_id)))
            new_qty = current_qty - qty_change
            movement_type = "OUT"
        else:
            new_qty = current_qty + qty_change
            movement_type = "IN"

        # Update product stock
        db.products.update_one({"_id": product_id}, {"$set": {"quantity": new_qty, "updated_at": datetime.now()}})

        # Record movement audit log
        full_reason = f"{reason} ({note})" if note else reason
        db.stock_movements.insert_one({
            "product_id": product_id,
            "product_name": product.get("product_name"),
            "type": movement_type,
            "quantity": qty_change,
            "reason": full_reason,
            "reference_id": "MANUAL-ADJ",
            "created_by": session.get("username", "admin"),
            "created_at": datetime.now()
        })

        flash(f"Stock adjusted successfully for '{product.get('product_name')}'. New balance: {new_qty} units.", "success")
        return redirect(url_for("stock_management"))

    all_products = list(db.products.find().sort("product_name", 1))
    recent_movements = list(db.stock_movements.find().sort("created_at", -1).limit(15))
    for m in recent_movements:
        m["created_at_formatted"] = format_datetime(m.get("created_at"), "%d %b, %I:%M %p")

    return render_template(
        "products/adjustment.html",
        products=all_products,
        movements=recent_movements,
        selected_product_id=selected_prd_id
    )


# =============================================================
# MODULE 11: Expiry Tracking
# =============================================================
@app.route("/stock/expiry")
@login_required
def expiry_tracking():
    """Module 11: Products that have expired or will expire soon (within 30 days)."""
    db = get_db()
    all_products = list(db.products.find({"expiry_date": {"$ne": ""}}).sort("expiry_date", 1))
    cat_map = {str(c["_id"]): c["name"] for c in db.categories.find()}

    today = datetime.now().date()
    expired_list = []
    expiring_soon_list = []

    for p in all_products:
        p["category_name"] = cat_map.get(str(p.get("category_id")), "General")
        exp_str = p.get("expiry_date")
        if exp_str:
            try:
                exp_date = datetime.strptime(exp_str, "%Y-%m-%d").date()
                days_diff = (exp_date - today).days
                p["days_left"] = days_diff

                if days_diff < 0:
                    expired_list.append(p)
                elif days_diff <= 30:
                    expiring_soon_list.append(p)
            except ValueError:
                continue

    return render_template(
        "products/expiry.html",
        expired_products=expired_list,
        expiring_soon_products=expiring_soon_list
    )


# =============================================================
# MODULE 13: Supplier Management (CRUD)
# =============================================================
@app.route("/suppliers")
@login_required
def suppliers():
    """List all registered wholesale suppliers."""
    db = get_db()
    sup_list = list(db.suppliers.find().sort("name", 1))
    return render_template("suppliers/index.html", suppliers=sup_list)

@app.route("/suppliers/add", methods=["GET", "POST"])
@login_required
def add_supplier():
    """Add a new supplier."""
    db = get_db()
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        contact_person = request.form.get("contact_person", "").strip()
        phone = request.form.get("phone", "").strip()
        email = request.form.get("email", "").strip()
        address = request.form.get("address", "").strip()

        db.suppliers.insert_one({
            "name": name,
            "contact_person": contact_person,
            "phone": phone,
            "email": email,
            "address": address,
            "created_at": datetime.now()
        })
        flash(f"Supplier '{name}' registered successfully.", "success")
        return redirect(url_for("suppliers"))

    return render_template("suppliers/form.html", supplier=None)

@app.route("/suppliers/edit/<sup_id>", methods=["GET", "POST"])
@login_required
def edit_supplier(sup_id):
    """Edit supplier details."""
    db = get_db()
    obj_id = to_object_id(sup_id)
    sup = db.suppliers.find_one({"_id": obj_id})
    if not sup:
        flash("Supplier not found.", "error")
        return redirect(url_for("suppliers"))

    if request.method == "POST":
        db.suppliers.update_one(
            {"_id": obj_id},
            {"$set": {
                "name": request.form.get("name", "").strip(),
                "contact_person": request.form.get("contact_person", "").strip(),
                "phone": request.form.get("phone", "").strip(),
                "email": request.form.get("email", "").strip(),
                "address": request.form.get("address", "").strip(),
                "updated_at": datetime.now()
            }}
        )
        flash("Supplier updated successfully.", "success")
        return redirect(url_for("suppliers"))

    return render_template("suppliers/form.html", supplier=sup)

@app.route("/suppliers/delete/<sup_id>")
@login_required
def delete_supplier(sup_id):
    """Delete a supplier."""
    db = get_db()
    obj_id = to_object_id(sup_id)
    db.suppliers.delete_one({"_id": obj_id})
    flash("Supplier deleted.", "success")
    return redirect(url_for("suppliers"))


# =============================================================
# MODULE 14 & 15: Purchase Entry & Purchase History
# =============================================================
@app.route("/purchases/new", methods=["GET", "POST"])
@login_required
def new_purchase():
    """
    Module 14: Record purchases.
    CRITICAL DATABASE RULE: When purchase is saved, INCREASE PRODUCT STOCK!
    """
    db = get_db()
    if request.method == "POST":
        supplier_id = to_object_id(request.form.get("supplier_id"))
        supplier = db.suppliers.find_one({"_id": supplier_id})
        supplier_name = supplier.get("name") if supplier else "General Supplier"

        purchase_date_str = request.form.get("purchase_date")
        note = request.form.get("note", "").strip()

        product_ids = request.form.getlist("product_id[]")
        quantities = request.form.getlist("quantity[]")
        prices = request.form.getlist("price[]")

        items = []
        grand_total = 0.0

        for p_id_str, qty_str, price_str in zip(product_ids, quantities, prices):
            if not p_id_str:
                continue
            p_obj_id = to_object_id(p_id_str)
            qty = int(qty_str or 0)
            price = float(price_str or 0)
            line_total = qty * price
            grand_total += line_total

            prd = db.products.find_one({"_id": p_obj_id})
            prd_name = prd.get("product_name") if prd else "Unknown Product"

            items.append({
                "product_id": p_obj_id,
                "product_name": prd_name,
                "quantity": qty,
                "purchase_price": price,
                "total": line_total
            })

            # IMPORTANT RULE: INCREASE PRODUCT STOCK
            db.products.update_one(
                {"_id": p_obj_id},
                {
                    "$inc": {"quantity": qty},
                    "$set": {"purchase_price": price, "updated_at": datetime.now()}
                }
            )

            # Record Stock Movement
            db.stock_movements.insert_one({
                "product_id": p_obj_id,
                "product_name": prd_name,
                "type": "IN",
                "quantity": qty,
                "reason": f"Purchase from {supplier_name}",
                "reference_id": "PURCHASE",
                "created_by": session.get("username", "admin"),
                "created_at": datetime.now()
            })

        if not items:
            flash("Please add at least one product to the purchase.", "error")
            return redirect(url_for("new_purchase"))

        # Save Purchase Document
        db.purchases.insert_one({
            "supplier_id": supplier_id,
            "supplier_name": supplier_name,
            "items": items,
            "total_amount": grand_total,
            "note": note,
            "created_by": session.get("username", "admin"),
            "created_at": datetime.now()
        })

        flash(f"Purchase recorded successfully! Stock increased for {len(items)} product(s).", "success")
        return redirect(url_for("purchase_history"))

    suppliers_list = list(db.suppliers.find().sort("name", 1))
    products_list = list(db.products.find().sort("product_name", 1))
    today_str = datetime.now().strftime("%Y-%m-%d")
    selected_sup = request.args.get("supplier_id", "")

    return render_template(
        "purchases/new.html",
        suppliers=suppliers_list,
        products=products_list,
        today_str=today_str,
        selected_supplier_id=selected_sup
    )

@app.route("/purchases/history")
@login_required
def purchase_history():
    """Module 15: Purchase History with search and date filter."""
    db = get_db()
    q = request.args.get("q", "").strip()
    date_filter = request.args.get("date", "").strip()

    filter_dict = {}
    if q:
        filter_dict["$or"] = [
            {"supplier_name": {"$regex": q, "$options": "i"}},
            {"note": {"$regex": q, "$options": "i"}}
        ]
    if date_filter:
        try:
            d_start = datetime.strptime(date_filter, "%Y-%m-%d").replace(hour=0, minute=0, second=0)
            d_end = datetime.strptime(date_filter, "%Y-%m-%d").replace(hour=23, minute=59, second=59)
            filter_dict["created_at"] = {"$gte": d_start, "$lte": d_end}
        except ValueError:
            pass

    purchases_list = list(db.purchases.find(filter_dict).sort("created_at", -1))
    for p in purchases_list:
        p["created_at_formatted"] = format_datetime(p.get("created_at"), "%d %b %Y, %I:%M %p")

    return render_template(
        "purchases/index.html",
        purchases=purchases_list,
        query=q,
        selected_date=date_filter
    )


# =============================================================
# MODULE 16, 17, 18 & 19: Customer Management, Search, History & Due Tracking
# =============================================================
@app.route("/customers")
@login_required
def customers():
    """List customers with search by name or phone (Module 17)."""
    db = get_db()
    query = request.args.get("q", "").strip()

    filter_dict = {}
    if query:
        filter_dict["$or"] = [
            {"name": {"$regex": query, "$options": "i"}},
            {"phone": {"$regex": query, "$options": "i"}}
        ]

    customer_list = list(db.customers.find(filter_dict).sort("name", 1))
    return render_template("customers/index.html", customers=customer_list, query=query)

@app.route("/customers/add", methods=["GET", "POST"])
@login_required
def add_customer():
    """Add new customer."""
    db = get_db()
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        phone = request.form.get("phone", "").strip()
        email = request.form.get("email", "").strip()
        address = request.form.get("address", "").strip()

        db.customers.insert_one({
            "name": name,
            "phone": phone,
            "email": email,
            "address": address,
            "total_purchases": 0.0,
            "total_due": 0.0,
            "created_at": datetime.now()
        })
        flash(f"Customer '{name}' added successfully.", "success")
        return redirect(url_for("customers"))

    return render_template("customers/form.html", customer=None)

@app.route("/customers/edit/<cust_id>", methods=["GET", "POST"])
@login_required
def edit_customer(cust_id):
    """Edit customer details."""
    db = get_db()
    obj_id = to_object_id(cust_id)
    cust = db.customers.find_one({"_id": obj_id})
    if not cust:
        flash("Customer not found.", "error")
        return redirect(url_for("customers"))

    if request.method == "POST":
        db.customers.update_one(
            {"_id": obj_id},
            {"$set": {
                "name": request.form.get("name", "").strip(),
                "phone": request.form.get("phone", "").strip(),
                "email": request.form.get("email", "").strip(),
                "address": request.form.get("address", "").strip(),
                "updated_at": datetime.now()
            }}
        )
        flash("Customer updated successfully.", "success")
        return redirect(url_for("customers"))

    return render_template("customers/form.html", customer=cust)

@app.route("/customers/delete/<cust_id>")
@login_required
def delete_customer(cust_id):
    """Delete a customer."""
    db = get_db()
    obj_id = to_object_id(cust_id)
    db.customers.delete_one({"_id": obj_id})
    flash("Customer deleted.", "success")
    return redirect(url_for("customers"))

@app.route("/customers/<cust_id>/history")
@login_required
def customer_history(cust_id):
    """
    Module 18: Customer Purchase History.
    Module 19: Customer Due / Payment Tracking.
    """
    db = get_db()
    obj_id = to_object_id(cust_id)
    customer = db.customers.find_one({"_id": obj_id})
    if not customer:
        flash("Customer not found.", "error")
        return redirect(url_for("customers"))

    # Fetch bills linked to this customer
    sales = list(db.sales.find({"customer_id": obj_id}).sort("created_at", -1))
    for s in sales:
        s["created_at_formatted"] = format_datetime(s.get("created_at"), "%d %b %Y, %I:%M %p")

    lifetime_billed = sum(s.get("grand_total", 0) for s in sales if s.get("status") != "Cancelled")

    return render_template(
        "customers/history.html",
        customer=customer,
        customer_sales=sales,
        lifetime_billed=lifetime_billed
    )


# =============================================================
# MODULE 20, 21, 22, 23, 24 & 25: New Billing, Invoicing, Sales History & Returns
# =============================================================
@app.route("/sales/new", methods=["GET", "POST"])
@login_required
def new_sale():
    """
    MODULE 20: New Billing
    MODULE 21: Automatic Invoice Number
    MODULE 22: Automatic Bill Calculation
    CRITICAL DATABASE RULE: Stock DECREASES on sale. Prevents negative stock.
    """
    db = get_db()

    if request.method == "POST":
        invoice_no = request.form.get("invoice_number") or generate_invoice_number(db)
        customer_id_str = request.form.get("customer_id")
        customer_id = to_object_id(customer_id_str) if customer_id_str else None
        customer_name = request.form.get("customer_name", "Walk-in Customer").strip()
        customer_phone = request.form.get("customer_phone", "").strip()

        # Arrays of item rows
        product_ids = request.form.getlist("product_id[]")
        quantities = request.form.getlist("quantity[]")
        prices = request.form.getlist("price[]")

        subtotal = 0.0
        items = []

        # 1. Validation: Verify Stock Before Committing
        for p_id_str, qty_str, price_str in zip(product_ids, quantities, prices):
            if not p_id_str:
                continue
            p_obj_id = to_object_id(p_id_str)
            qty = int(qty_str or 0)
            selling_price = float(price_str or 0)
            line_total = qty * selling_price

            prd = db.products.find_one({"_id": p_obj_id})
            if not prd:
                flash("One or more selected products are invalid.", "error")
                return redirect(url_for("new_sale"))

            if prd.get("quantity", 0) < qty:
                flash(f"Insufficient stock for '{prd.get('product_name')}'. Available: {prd.get('quantity', 0)}.", "error")
                return redirect(url_for("new_sale"))

            items.append({
                "product_id": p_obj_id,
                "product_name": prd.get("product_name"),
                "product_code": prd.get("product_code"),
                "quantity": qty,
                "selling_price": selling_price,
                "purchase_price": prd.get("purchase_price", 0.0),
                "total": line_total
            })
            subtotal += line_total

        if not items:
            flash("Please add at least one item to generate an invoice.", "error")
            return redirect(url_for("new_sale"))

        # 2. Bill Calculation (Module 22)
        discount = float(request.form.get("discount", 0) or 0)
        tax_percent = float(request.form.get("tax_percent", 0) or 0)
        discounted_subtotal = max(0.0, subtotal - discount)
        tax = (discounted_subtotal * tax_percent) / 100.0
        grand_total = discounted_subtotal + tax

        paid_amount = float(request.form.get("paid_amount", 0) or 0)
        due_amount = max(0.0, grand_total - paid_amount)

        # Payment Status (Module 19)
        if paid_amount >= grand_total:
            payment_status = "Paid"
        elif paid_amount > 0:
            payment_status = "Partial"
        else:
            payment_status = "Due"

        # 3. Commit: Decrement Product Stock and Create Stock Movement Log
        for itm in items:
            db.products.update_one(
                {"_id": itm["product_id"]},
                {"$inc": {"quantity": -itm["quantity"]}, "$set": {"updated_at": datetime.now()}}
            )
            db.stock_movements.insert_one({
                "product_id": itm["product_id"],
                "product_name": itm["product_name"],
                "type": "OUT",
                "quantity": itm["quantity"],
                "reason": f"Sale ({invoice_no})",
                "reference_id": invoice_no,
                "created_by": session.get("username", "admin"),
                "created_at": datetime.now()
            })

        # 4. Save Sales Document
        sale_doc = {
            "invoice_number": invoice_no,
            "customer_id": customer_id,
            "customer_name": customer_name,
            "customer_phone": customer_phone,
            "items": items,
            "subtotal": subtotal,
            "discount": discount,
            "tax": tax,
            "grand_total": grand_total,
            "paid_amount": paid_amount,
            "due_amount": due_amount,
            "payment_status": payment_status,
            "payment_mode": request.form.get("payment_mode", "Cash"),
            "status": "Completed",
            "created_by": session.get("username", "admin"),
            "created_at": datetime.now()
        }
        res_sale = db.sales.insert_one(sale_doc)

        # 5. Update Customer Ledger if linked
        if customer_id:
            db.customers.update_one(
                {"_id": customer_id},
                {
                    "$inc": {
                        "total_purchases": grand_total,
                        "total_due": due_amount
                    }
                }
            )

        flash(f"Invoice {invoice_no} completed successfully! Stock decreased.", "success")
        return redirect(url_for("view_invoice", sale_id=str(res_sale.inserted_id)))

    # GET Request: Load new bill screen
    next_inv = generate_invoice_number(db)
    customers_list = list(db.customers.find().sort("name", 1))
    products_list = list(db.products.find().sort("product_name", 1))
    selected_customer = request.args.get("customer_id", "")

    return render_template(
        "sales/new.html",
        next_invoice_number=next_inv,
        customers=customers_list,
        products=products_list,
        selected_customer_id=selected_customer
    )

@app.route("/sales/<sale_id>/invoice")
@login_required
def view_invoice(sale_id):
    """Module 23: Print / Download Invoice layout."""
    db = get_db()
    obj_id = to_object_id(sale_id)
    sale = db.sales.find_one({"_id": obj_id})
    if not sale:
        flash("Invoice not found.", "error")
        return redirect(url_for("sales_history"))

    sale["created_at_formatted"] = format_datetime(sale.get("created_at"), "%d %b %Y, %I:%M %p")
    return render_template("sales/invoice.html", sale=sale)

@app.route("/sales/history")
@login_required
def sales_history():
    """Module 24: Sales History with filter and search."""
    db = get_db()
    q = request.args.get("q", "").strip()
    status_filter = request.args.get("status", "").strip()
    date_filter = request.args.get("date", "").strip()

    filter_dict = {}
    if q:
        filter_dict["$or"] = [
            {"invoice_number": {"$regex": q, "$options": "i"}},
            {"customer_name": {"$regex": q, "$options": "i"}}
        ]
    if status_filter:
        filter_dict["payment_status"] = status_filter
    if date_filter:
        try:
            d_start = datetime.strptime(date_filter, "%Y-%m-%d").replace(hour=0, minute=0, second=0)
            d_end = datetime.strptime(date_filter, "%Y-%m-%d").replace(hour=23, minute=59, second=59)
            filter_dict["created_at"] = {"$gte": d_start, "$lte": d_end}
        except ValueError:
            pass

    sales_list = list(db.sales.find(filter_dict).sort("created_at", -1))
    for s in sales_list:
        s["created_at_formatted"] = format_datetime(s.get("created_at"), "%d %b %Y, %I:%M %p")

    return render_template(
        "sales/index.html",
        sales=sales_list,
        query=q,
        selected_status=status_filter,
        selected_date=date_filter
    )

@app.route("/sales/<sale_id>/cancel")
@login_required
def cancel_sale(sale_id):
    """
    MODULE 25: Sales Return / Cancel Bill.
    CRITICAL DATABASE RULE: When a sale is cancelled, RESTORE sold quantity back to stock!
    Sale status is updated to 'Cancelled'.
    """
    db = get_db()
    obj_id = to_object_id(sale_id)
    sale = db.sales.find_one({"_id": obj_id})

    if not sale:
        flash("Sale invoice not found.", "error")
        return redirect(url_for("sales_history"))

    if sale.get("status") == "Cancelled":
        flash("This sale invoice is already marked as Cancelled/Returned.", "warning")
        return redirect(url_for("sales_history"))

    # 1. Restore Sold Quantities Back to Product Stock
    for item in sale.get("items", []):
        p_id = item.get("product_id")
        qty = item.get("quantity", 0)
        db.products.update_one(
            {"_id": p_id},
            {"$inc": {"quantity": qty}, "$set": {"updated_at": datetime.now()}}
        )
        # Record Stock Restitution
        db.stock_movements.insert_one({
            "product_id": p_id,
            "product_name": item.get("product_name"),
            "type": "IN",
            "quantity": qty,
            "reason": f"Sale Return / Cancelled Bill ({sale.get('invoice_number')})",
            "reference_id": sale.get("invoice_number"),
            "created_by": session.get("username", "admin"),
            "created_at": datetime.now()
        })

    # 2. Update Customer Ledger Due balance if linked
    if sale.get("customer_id") and sale.get("due_amount", 0) > 0:
        db.customers.update_one(
            {"_id": sale["customer_id"]},
            {"$inc": {"total_due": -sale["due_amount"]}}
        )

    # 3. Update Status to 'Cancelled' (Never delete audit records)
    db.sales.update_one(
        {"_id": obj_id},
        {"$set": {
            "status": "Cancelled",
            "cancelled_at": datetime.now(),
            "cancelled_by": session.get("username", "admin")
        }}
    )

    flash(f"Invoice {sale.get('invoice_number')} cancelled. Sold quantities have been restored back to inventory.", "success")
    return redirect(url_for("sales_history"))

@app.route("/sales/returns")
@login_required
def returns_list():
    """Module 25: View all returned / cancelled sales."""
    db = get_db()
    cancelled = list(db.sales.find({"status": "Cancelled"}).sort("created_at", -1))
    for s in cancelled:
        s["created_at_formatted"] = format_datetime(s.get("created_at"), "%d %b %Y, %I:%M %p")
    return render_template("sales/returns.html", cancelled_sales=cancelled)


# =============================================================
# MODULE 26, 27, 28 & 29: Reports
# =============================================================
@app.route("/reports/daily")
@login_required
def daily_report():
    """Module 26: Daily Sales Report (Bills count, total sales, items sold, table)."""
    db = get_db()
    date_str = request.args.get("date", datetime.now().strftime("%Y-%m-%d"))

    try:
        selected_date = datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        selected_date = datetime.now()
        date_str = selected_date.strftime("%Y-%m-%d")

    day_start = selected_date.replace(hour=0, minute=0, second=0, microsecond=0)
    day_end = selected_date.replace(hour=23, minute=59, second=59, microsecond=999999)

    sales = list(db.sales.find({
        "status": {"$ne": "Cancelled"},
        "created_at": {"$gte": day_start, "$lte": day_end}
    }).sort("created_at", 1))

    total_revenue = sum(s.get("grand_total", 0) for s in sales)
    total_bills = len(sales)
    total_items = sum(sum(item.get("quantity", 0) for item in s.get("items", [])) for s in sales)

    for s in sales:
        s["created_at_time"] = format_datetime(s.get("created_at"), "%I:%M %p")

    return render_template(
        "reports/daily.html",
        selected_date_str=date_str,
        sales=sales,
        total_bills=total_bills,
        total_revenue=total_revenue,
        total_items_sold=total_items
    )

@app.route("/reports/monthly")
@login_required
def monthly_report():
    """Module 27: Monthly Sales Report with Chart.js visualization."""
    db = get_db()
    month_str = request.args.get("month", datetime.now().strftime("%Y-%m"))

    try:
        year, month = map(int, month_str.split("-"))
    except ValueError:
        now = datetime.now()
        year, month = now.year, now.month
        month_str = now.strftime("%Y-%m")

    month_start = datetime(year, month, 1, 0, 0, 0)
    # Determine days in month
    if month == 12:
        month_end = datetime(year + 1, 1, 1, 0, 0, 0) - timedelta(microseconds=1)
    else:
        month_end = datetime(year, month + 1, 1, 0, 0, 0) - timedelta(microseconds=1)

    sales = list(db.sales.find({
        "status": {"$ne": "Cancelled"},
        "created_at": {"$gte": month_start, "$lte": month_end}
    }))

    total_revenue = sum(s.get("grand_total", 0) for s in sales)
    total_bills = len(sales)
    total_items = sum(sum(item.get("quantity", 0) for item in s.get("items", [])) for s in sales)

    # Day-wise distribution for Chart.js
    days_count = (month_end - month_start).days + 1
    daily_revenue = {d: 0.0 for d in range(1, days_count + 1)}
    for s in sales:
        dt = s.get("created_at")
        if isinstance(dt, datetime):
            daily_revenue[dt.day] += s.get("grand_total", 0)

    chart_labels = [f"Day {d}" for d in range(1, days_count + 1)]
    chart_values = [round(daily_revenue[d], 2) for d in range(1, days_count + 1)]

    return render_template(
        "reports/monthly.html",
        selected_month_str=month_str,
        month_display=month_start.strftime("%B %Y"),
        total_bills=total_bills,
        total_revenue=total_revenue,
        total_items_sold=total_items,
        chart_labels=chart_labels,
        chart_values=chart_values
    )

@app.route("/reports/top-products")
@login_required
def top_products_report():
    """Module 28: Top Selling Products ranked by quantity sold and revenue."""
    db = get_db()
    sales = list(db.sales.find({"status": {"$ne": "Cancelled"}}))

    product_stats = {}
    for s in sales:
        for itm in s.get("items", []):
            name = itm.get("product_name", "Unknown")
            code = itm.get("product_code", "—")
            qty = itm.get("quantity", 0)
            amount = itm.get("total", 0)

            if name not in product_stats:
                product_stats[name] = {"product_name": name, "product_code": code, "quantity_sold": 0, "sales_amount": 0.0}
            product_stats[name]["quantity_sold"] += qty
            product_stats[name]["sales_amount"] += amount

    sorted_products = sorted(product_stats.values(), key=lambda x: x["quantity_sold"], reverse=True)[:10]

    chart_labels = [p["product_name"] for p in sorted_products[:5]]
    chart_values = [p["quantity_sold"] for p in sorted_products[:5]]

    return render_template(
        "reports/top_products.html",
        top_products=sorted_products,
        chart_labels=chart_labels,
        chart_values=chart_values
    )

@app.route("/reports/profit")
@login_required
def profit_report():
    """Module 29: Estimated Profit & Inventory Valuation Report."""
    db = get_db()
    sales = list(db.sales.find({"status": {"$ne": "Cancelled"}}))

    total_revenue = 0.0
    total_cost = 0.0

    for s in sales:
        total_revenue += s.get("grand_total", 0)
        for itm in s.get("items", []):
            qty = itm.get("quantity", 0)
            purchase_price = itm.get("purchase_price", 0)
            total_cost += (qty * purchase_price)

    estimated_profit = total_revenue - total_cost
    profit_margin = (estimated_profit / total_revenue * 100) if total_revenue > 0 else 0.0

    # Current Inventory Valuation
    products = list(db.products.find())
    inventory_cost_value = sum(p.get("quantity", 0) * p.get("purchase_price", 0) for p in products)
    inventory_retail_value = sum(p.get("quantity", 0) * p.get("selling_price", 0) for p in products)

    # Category Breakdown
    categories = list(db.categories.find().sort("name", 1))
    category_breakdown = []
    for cat in categories:
        cat_products = [p for p in products if str(p.get("category_id")) == str(cat["_id"])]
        cat_units = sum(p.get("quantity", 0) for p in cat_products)
        cat_cost = sum(p.get("quantity", 0) * p.get("purchase_price", 0) for p in cat_products)
        cat_retail = sum(p.get("quantity", 0) * p.get("selling_price", 0) for p in cat_products)

        category_breakdown.append({
            "name": cat.get("name"),
            "product_count": len(cat_products),
            "total_units": cat_units,
            "cost_value": cat_cost,
            "retail_value": cat_retail
        })

    return render_template(
        "reports/profit.html",
        total_revenue=total_revenue,
        total_cost=total_cost,
        estimated_profit=estimated_profit,
        profit_margin=profit_margin,
        inventory_cost_value=inventory_cost_value,
        inventory_retail_value=inventory_retail_value,
        category_breakdown=category_breakdown
    )


# -------------------------------------------------------------
# Error Handling (Module 23 requirement: Friendly error messages)
# -------------------------------------------------------------
@app.errorhandler(404)
def page_not_found(e):
    return render_template("base.html"), 404

@app.errorhandler(500)
def server_error(e):
    print(f"[ERROR 500] Internal server error: {e}")
    flash("Something went wrong. Please try again.", "error")
    return redirect(url_for("dashboard"))


# -------------------------------------------------------------
# Application Runner
# -------------------------------------------------------------
if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    print(f"[APP] Starting Inventory & Billing Management System on http://127.0.0.1:{port}")
    app.run(host="0.0.0.0", port=port, debug=Config.DEBUG)
