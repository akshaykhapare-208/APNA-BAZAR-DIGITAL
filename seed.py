from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash
from database import get_db

def seed_database(force=False):
    """
    Seeds initial realistic Indian local-store demo data if database is empty or force=True.
    Shop: 'Shree Ganesh General Store'
    """
    db = get_db()

    # Check if admin user already exists
    admin_exists = db.users.find_one({"username": "admin"})
    if admin_exists and not force:
        print("[SEED] Database already contains data. Skipping seeder.")
        return

    print("[SEED] Seeding initial Indian local-shop demo data...")

    # 1. Shop Settings (Shop Profile & App Config)
    db.settings.delete_many({})
    db.settings.insert_one({
        "shop_name": "APNA BAZAR",
        "owner_name": "Akshay Khapare",
        "phone": "+91 98201 23456",
        "email": "apnabazar.mumbai@gmail.com",
        "address": "Shop No. 4, Station Road, Dadar West, Mumbai - 400028",
        "gst_number": "27AAACG1234F1Z5",
        "tax_rate": 5.0,  # 5% default GST
        "currency_symbol": "₹",
        "created_at": datetime.now()
    })

    # 2. Users (Admin and Staff)
    db.users.delete_many({})
    admin_user = {
        "name": "Akshay Khapare (Owner)",
        "username": "admin",
        "email": "admin@apnabazar.com",
        "password_hash": generate_password_hash("admin123"),
        "role": "Admin",
        "phone": "+91 98201 23456",
        "status": "Active",
        "created_at": datetime.now()
    }
    staff_user = {
        "name": "Suresh Sawant (Cashier)",
        "username": "suresh",
        "email": "suresh@ganeshstore.com",
        "password_hash": generate_password_hash("staff123"),
        "role": "Staff",
        "phone": "+91 98199 87654",
        "status": "Active",
        "created_at": datetime.now()
    }
    db.users.insert_many([admin_user, staff_user])

    # 3. Categories
    db.categories.delete_many({})
    cat_docs = [
        {"name": "Grocery", "description": "Daily staples, grains, flours, and pulses", "created_at": datetime.now()},
        {"name": "Beverages", "description": "Tea, coffee, packaged drinking water, juices", "created_at": datetime.now()},
        {"name": "Snacks", "description": "Biscuits, chips, namkeen, chocolates", "created_at": datetime.now()},
        {"name": "Household", "description": "Detergents, cleaners, dish wash", "created_at": datetime.now()},
        {"name": "Personal Care", "description": "Soaps, shampoos, hair oil, toothpaste", "created_at": datetime.now()},
        {"name": "Stationery", "description": "Notebooks, pens, tape, school essentials", "created_at": datetime.now()}
    ]
    res_cats = db.categories.insert_many(cat_docs)
    cat_ids = res_cats.inserted_ids

    # 4. Suppliers
    db.suppliers.delete_many({})
    sup_docs = [
        {
            "name": "Mumbai Wholesale Mart",
            "contact_person": "Kishore Bhai",
            "phone": "+91 98205 11223",
            "email": "orders@mumbaiwholesale.in",
            "address": "APMC Market-2, Vashi, Navi Mumbai",
            "created_at": datetime.now()
        },
        {
            "name": "Fresh Supply Co.",
            "contact_person": "Anil Verma",
            "phone": "+91 97690 44556",
            "email": "freshsupply.mumbai@gmail.com",
            "address": "Plot 18, MIDC, Andheri East, Mumbai",
            "created_at": datetime.now()
        },
        {
            "name": "Local Distributors LLP",
            "contact_person": "Deepak Mehta",
            "phone": "+91 98211 77889",
            "email": "deepak@localdist.co.in",
            "address": "Gala 12, Grain Market, Kurla West, Mumbai",
            "created_at": datetime.now()
        }
    ]
    res_sups = db.suppliers.insert_many(sup_docs)
    sup_ids = res_sups.inserted_ids

    # 5. Customers
    db.customers.delete_many({})
    cust_docs = [
        {
            "name": "Rahul Sharma",
            "phone": "+91 98200 11111",
            "email": "rahul.sharma@gmail.com",
            "address": "B-204, Gokul Dham, Dadar West",
            "total_purchases": 1250.0,
            "total_due": 50.0,
            "created_at": datetime.now()
        },
        {
            "name": "Priya Patil",
            "phone": "+91 98200 22222",
            "email": "priya.patil@yahoo.com",
            "address": "A-12, Sai Kripa Society, Shivaji Park",
            "total_purchases": 840.0,
            "total_due": 0.0,
            "created_at": datetime.now()
        },
        {
            "name": "Amit Shah",
            "phone": "+91 98200 33333",
            "email": "amit.shah@outlook.com",
            "address": "Flat 5, Saraswati Niwas, Mahim",
            "total_purchases": 420.0,
            "total_due": 120.0,
            "created_at": datetime.now()
        },
        {
            "name": "Neha Joshi",
            "phone": "+91 98200 44444",
            "email": "neha.j@gmail.com",
            "address": "101, Om Shanti Tower, Prabhadevi",
            "total_purchases": 310.0,
            "total_due": 0.0,
            "created_at": datetime.now()
        }
    ]
    res_custs = db.customers.insert_many(cust_docs)
    cust_ids = res_custs.inserted_ids

    # 6. Products
    db.products.delete_many({})
    today = datetime.now()
    prd_docs = [
        {
            "product_name": "Kolam Rice (1kg)",
            "product_code": "PRD-1001",
            "category_id": cat_ids[0],
            "supplier_id": sup_ids[0],
            "purchase_price": 50.0,
            "selling_price": 65.0,
            "quantity": 45,
            "minimum_stock": 10,
            "expiry_date": (today + timedelta(days=240)).strftime("%Y-%m-%d"),
            "created_at": datetime.now()
        },
        {
            "product_name": "Chakki Wheat Flour (5kg)",
            "product_code": "PRD-1002",
            "category_id": cat_ids[0],
            "supplier_id": sup_ids[0],
            "purchase_price": 190.0,
            "selling_price": 230.0,
            "quantity": 25,
            "minimum_stock": 8,
            "expiry_date": (today + timedelta(days=90)).strftime("%Y-%m-%d"),
            "created_at": datetime.now()
        },
        {
            "product_name": "Madhur Pure Sugar (1kg)",
            "product_code": "PRD-1003",
            "category_id": cat_ids[0],
            "supplier_id": sup_ids[0],
            "purchase_price": 38.0,
            "selling_price": 46.0,
            "quantity": 6,  # Low stock test item!
            "minimum_stock": 10,
            "expiry_date": (today + timedelta(days=365)).strftime("%Y-%m-%d"),
            "created_at": datetime.now()
        },
        {
            "product_name": "Tata Gold Tea (250g)",
            "product_code": "PRD-1004",
            "category_id": cat_ids[1],
            "supplier_id": sup_ids[1],
            "purchase_price": 115.0,
            "selling_price": 140.0,
            "quantity": 18,
            "minimum_stock": 5,
            "expiry_date": (today + timedelta(days=180)).strftime("%Y-%m-%d"),
            "created_at": datetime.now()
        },
        {
            "product_name": "Parle-G Gold Biscuits (100g)",
            "product_code": "PRD-1005",
            "category_id": cat_ids[2],
            "supplier_id": sup_ids[1],
            "purchase_price": 8.0,
            "selling_price": 10.0,
            "quantity": 60,
            "minimum_stock": 15,
            "expiry_date": (today + timedelta(days=120)).strftime("%Y-%m-%d"),
            "created_at": datetime.now()
        },
        {
            "product_name": "Amul Taaza Milk (500ml)",
            "product_code": "PRD-1006",
            "category_id": cat_ids[1],
            "supplier_id": sup_ids[1],
            "purchase_price": 24.0,
            "selling_price": 28.0,
            "quantity": 4,  # Low stock & expiring soon
            "minimum_stock": 10,
            "expiry_date": (today + timedelta(days=2)).strftime("%Y-%m-%d"),
            "created_at": datetime.now()
        },
        {
            "product_name": "Dettol Bathing Soap (75g)",
            "product_code": "PRD-1007",
            "category_id": cat_ids[4],
            "supplier_id": sup_ids[2],
            "purchase_price": 32.0,
            "selling_price": 40.0,
            "quantity": 30,
            "minimum_stock": 8,
            "expiry_date": (today + timedelta(days=400)).strftime("%Y-%m-%d"),
            "created_at": datetime.now()
        },
        {
            "product_name": "Clinic Plus Shampoo (175ml)",
            "product_code": "PRD-1008",
            "category_id": cat_ids[4],
            "supplier_id": sup_ids[2],
            "purchase_price": 95.0,
            "selling_price": 120.0,
            "quantity": 14,
            "minimum_stock": 5,
            "expiry_date": (today + timedelta(days=300)).strftime("%Y-%m-%d"),
            "created_at": datetime.now()
        },
        {
            "product_name": "Fortune Sunflower Oil (1L Pouch)",
            "product_code": "PRD-1009",
            "category_id": cat_ids[0],
            "supplier_id": sup_ids[0],
            "purchase_price": 125.0,
            "selling_price": 145.0,
            "quantity": 2,  # Low stock test item
            "minimum_stock": 10,
            "expiry_date": (today + timedelta(days=150)).strftime("%Y-%m-%d"),
            "created_at": datetime.now()
        },
        {
            "product_name": "Tata Iodized Salt (1kg)",
            "product_code": "PRD-1010",
            "category_id": cat_ids[0],
            "supplier_id": sup_ids[0],
            "purchase_price": 20.0,
            "selling_price": 26.0,
            "quantity": 50,
            "minimum_stock": 12,
            "expiry_date": (today + timedelta(days=500)).strftime("%Y-%m-%d"),
            "created_at": datetime.now()
        },
        {
            "product_name": "Classmate Long Notebook (172 pgs)",
            "product_code": "PRD-1011",
            "category_id": cat_ids[5],
            "supplier_id": sup_ids[2],
            "purchase_price": 45.0,
            "selling_price": 60.0,
            "quantity": 0,  # Out of stock test item!
            "minimum_stock": 10,
            "expiry_date": (today + timedelta(days=700)).strftime("%Y-%m-%d"),
            "created_at": datetime.now()
        }
    ]
    res_prds = db.products.insert_many(prd_docs)
    prd_ids = res_prds.inserted_ids

    # 7. Purchases History
    db.purchases.delete_many({})
    purchase_doc = {
        "supplier_id": sup_ids[0],
        "supplier_name": "Mumbai Wholesale Mart",
        "items": [
            {
                "product_id": prd_ids[0],
                "product_name": "Kolam Rice (1kg)",
                "quantity": 50,
                "purchase_price": 50.0,
                "total": 2500.0
            },
            {
                "product_id": prd_ids[2],
                "product_name": "Madhur Pure Sugar (1kg)",
                "quantity": 30,
                "purchase_price": 38.0,
                "total": 1140.0
            }
        ],
        "total_amount": 3640.0,
        "note": "Initial monthly restock batch",
        "created_at": today - timedelta(days=5)
    }
    db.purchases.insert_one(purchase_doc)

    # 8. Sales History
    db.sales.delete_many({})
    sales_docs = [
        {
            "invoice_number": "INV-0001",
            "customer_id": cust_ids[0],
            "customer_name": "Rahul Sharma",
            "customer_phone": "+91 98200 11111",
            "items": [
                {
                    "product_id": prd_ids[0],
                    "product_name": "Kolam Rice (1kg)",
                    "product_code": "PRD-1001",
                    "quantity": 2,
                    "selling_price": 65.0,
                    "purchase_price": 50.0,
                    "total": 130.0
                },
                {
                    "product_id": prd_ids[3],
                    "product_name": "Tata Gold Tea (250g)",
                    "product_code": "PRD-1004",
                    "quantity": 1,
                    "selling_price": 140.0,
                    "purchase_price": 115.0,
                    "total": 140.0
                }
            ],
            "subtotal": 270.0,
            "discount": 20.0,
            "tax": 0.0,
            "grand_total": 250.0,
            "paid_amount": 200.0,
            "due_amount": 50.0,
            "payment_status": "Partial",
            "status": "Completed",
            "created_by": "admin",
            "created_at": today - timedelta(days=1, hours=2)
        },
        {
            "invoice_number": "INV-0002",
            "customer_id": cust_ids[1],
            "customer_name": "Priya Patil",
            "customer_phone": "+91 98200 22222",
            "items": [
                {
                    "product_id": prd_ids[1],
                    "product_name": "Chakki Wheat Flour (5kg)",
                    "product_code": "PRD-1002",
                    "quantity": 2,
                    "selling_price": 230.0,
                    "purchase_price": 190.0,
                    "total": 460.0
                },
                {
                    "product_id": prd_ids[8],
                    "product_name": "Fortune Sunflower Oil (1L Pouch)",
                    "product_code": "PRD-1009",
                    "quantity": 1,
                    "selling_price": 145.0,
                    "purchase_price": 125.0,
                    "total": 145.0
                }
            ],
            "subtotal": 605.0,
            "discount": 5.0,
            "tax": 0.0,
            "grand_total": 600.0,
            "paid_amount": 600.0,
            "due_amount": 0.0,
            "payment_status": "Paid",
            "status": "Completed",
            "created_by": "admin",
            "created_at": today
        },
        {
            "invoice_number": "INV-0003",
            "customer_id": cust_ids[2],
            "customer_name": "Amit Shah",
            "customer_phone": "+91 98200 33333",
            "items": [
                {
                    "product_id": prd_ids[7],
                    "product_name": "Clinic Plus Shampoo (175ml)",
                    "product_code": "PRD-1008",
                    "quantity": 1,
                    "selling_price": 120.0,
                    "purchase_price": 95.0,
                    "total": 120.0
                }
            ],
            "subtotal": 120.0,
            "discount": 0.0,
            "tax": 0.0,
            "grand_total": 120.0,
            "paid_amount": 0.0,
            "due_amount": 120.0,
            "payment_status": "Due",
            "status": "Completed",
            "created_by": "suresh",
            "created_at": today
        }
    ]
    db.sales.insert_many(sales_docs)

    # 9. Stock Movements Audit Log
    db.stock_movements.delete_many({})
    movements = [
        {
            "product_id": prd_ids[0],
            "product_name": "Kolam Rice (1kg)",
            "type": "IN",
            "quantity": 50,
            "reason": "Purchase Entry (Mumbai Wholesale Mart)",
            "reference_id": "PUR-0001",
            "created_at": today - timedelta(days=5)
        },
        {
            "product_id": prd_ids[0],
            "product_name": "Kolam Rice (1kg)",
            "type": "OUT",
            "quantity": 2,
            "reason": "Sale (INV-0001)",
            "reference_id": "INV-0001",
            "created_at": today - timedelta(days=1, hours=2)
        }
    ]
    db.stock_movements.insert_many(movements)

    print("[SEED] [OK] Successfully seeded Indian local store data with 30-module sample records!")

if __name__ == "__main__":
    seed_database(force=True)
