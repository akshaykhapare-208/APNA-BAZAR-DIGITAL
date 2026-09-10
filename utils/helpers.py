from functools import wraps
from datetime import datetime
from flask import session, redirect, url_for, flash

def login_required(f):
    """Decorator to ensure user is logged in."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_id" not in session:
            flash("Please log in to access this page.", "error")
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    """Decorator to ensure user has Admin role."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_id" not in session:
            flash("Please log in to access this page.", "error")
            return redirect(url_for("login"))
        if session.get("user_role") != "Admin":
            flash("Access denied. Admin privileges required.", "error")
            return redirect(url_for("dashboard"))
        return f(*args, **kwargs)
    return decorated_function

def format_currency(val):
    """Format numeric value as Indian Rupee string."""
    try:
        val = float(val or 0)
        return f"₹{val:,.2f}"
    except (ValueError, TypeError):
        return "₹0.00"

def format_datetime(val, format_str="%d %b %Y, %I:%M %p"):
    """Format datetime object or ISO string."""
    if not val:
        return "—"
    if isinstance(val, str):
        try:
            val = datetime.fromisoformat(val)
        except Exception:
            return val
    if isinstance(val, datetime):
        return val.strftime(format_str)
    return str(val)

def get_stock_status(quantity, minimum_stock):
    """Determine stock status based on current quantity and minimum threshold."""
    try:
        qty = float(quantity or 0)
        min_qty = float(minimum_stock or 0)
    except (ValueError, TypeError):
        qty, min_qty = 0, 0

    if qty <= 0:
        return "Out of Stock", "danger"
    elif qty <= min_qty:
        return "Low Stock", "warning"
    else:
        return "In Stock", "success"

def generate_invoice_number(db):
    """
    Generate sequential invoice number: INV-0001, INV-0002, etc.
    Finds the highest existing invoice number and increments it.
    """
    try:
        # Find last sale sorted by created_at descending
        last_sale = db.sales.find_one(sort=[("created_at", -1)])
        if not last_sale or "invoice_number" not in last_sale:
            return "INV-0001"

        last_no = last_sale["invoice_number"]
        if last_no.startswith("INV-"):
            num_part = int(last_no.replace("INV-", ""))
            return f"INV-{num_part + 1:04d}"
        return "INV-0001"
    except Exception:
        # Fallback based on count
        count = db.sales.count_documents({})
        return f"INV-{count + 1:04d}"
