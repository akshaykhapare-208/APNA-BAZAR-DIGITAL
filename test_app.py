import unittest
from datetime import datetime
from app import app
from database import get_db, to_object_id
from seed import seed_database
from werkzeug.security import check_password_hash

class TestInventoryBillingSystem(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        app.config["TESTING"] = True
        app.config["WTF_CSRF_ENABLED"] = False
        seed_database(force=True)

    def setUp(self):
        self.client = app.test_client()
        self.db = get_db()

    def test_01_login_authentication(self):
        """Test Module 1: Admin Login & Session Handling"""
        # Test wrong credentials
        res = self.client.post("/login", data={"username": "admin", "password": "wrongpassword"})
        self.assertEqual(res.status_code, 200)

        # Test valid credentials
        res = self.client.post("/login", data={"username": "admin", "password": "admin123"}, follow_redirects=True)
        self.assertEqual(res.status_code, 200)
        self.assertIn(b"Welcome back", res.data)

    def test_02_dashboard_live_mongodb_data(self):
        """Test Module 3: Dashboard retrieves live data from MongoDB"""
        with self.client.session_transaction() as sess:
            sess["user_id"] = "test_user_id"
            sess["username"] = "admin"
            sess["user_role"] = "Admin"

        res = self.client.get("/dashboard")
        self.assertEqual(res.status_code, 200)
        self.assertIn(b"Shop Overview", res.data)
        self.assertIn(b"Today's Sales", res.data)

    def test_03_category_crud(self):
        """Test Module 5: Category CRUD"""
        with self.client.session_transaction() as sess:
            sess["user_id"] = "test_user_id"
            sess["username"] = "admin"
            sess["user_role"] = "Admin"

        # Add Category
        res = self.client.post("/categories/add", data={
            "name": "Dairy & Milk",
            "description": "Daily fresh milk and butter"
        }, follow_redirects=True)
        self.assertEqual(res.status_code, 200)
        cat = self.db.categories.find_one({"name": "Dairy & Milk"})
        self.assertIsNotNone(cat)

        # Edit Category
        res = self.client.post(f"/categories/edit/{cat['_id']}", data={
            "name": "Dairy & Paneer",
            "description": "Fresh milk, curd, and paneer"
        }, follow_redirects=True)
        self.assertEqual(res.status_code, 200)
        cat_updated = self.db.categories.find_one({"_id": cat["_id"]})
        self.assertEqual(cat_updated["name"], "Dairy & Paneer")

        # Delete Category
        res = self.client.get(f"/categories/delete/{cat['_id']}", follow_redirects=True)
        self.assertEqual(res.status_code, 200)
        self.assertIsNone(self.db.categories.find_one({"_id": cat["_id"]}))

    def test_04_product_crud_and_search(self):
        """Test Module 6, 7 & 12: Product Management, Search, and Code"""
        with self.client.session_transaction() as sess:
            sess["user_id"] = "test_user_id"
            sess["username"] = "admin"
            sess["user_role"] = "Admin"

        cat = self.db.categories.find_one()
        # Add Product
        res = self.client.post("/products/add", data={
            "product_name": "Moong Dal (1kg)",
            "product_code": "PRD-9999",
            "category_id": str(cat["_id"]),
            "purchase_price": "80.0",
            "selling_price": "100.0",
            "quantity": "20",
            "minimum_stock": "5",
            "expiry_date": "2027-01-01"
        }, follow_redirects=True)
        self.assertEqual(res.status_code, 200)

        prd = self.db.products.find_one({"product_code": "PRD-9999"})
        self.assertIsNotNone(prd)
        self.assertEqual(prd["quantity"], 20)

        # Search Product by Code
        res = self.client.get("/products?q=PRD-9999")
        self.assertIn(b"Moong Dal (1kg)", res.data)

        # Edit Product
        res = self.client.post(f"/products/edit/{prd['_id']}", data={
            "product_name": "Moong Dal Premium (1kg)",
            "product_code": "PRD-9999",
            "category_id": str(cat["_id"]),
            "purchase_price": "85.0",
            "selling_price": "110.0",
            "quantity": "25",
            "minimum_stock": "6",
            "expiry_date": "2027-01-01"
        }, follow_redirects=True)
        self.assertEqual(res.status_code, 200)
        prd_updated = self.db.products.find_one({"_id": prd["_id"]})
        self.assertEqual(prd_updated["product_name"], "Moong Dal Premium (1kg)")
        self.assertEqual(prd_updated["selling_price"], 110.0)

        # Delete Product
        res = self.client.get(f"/products/delete/{prd['_id']}", follow_redirects=True)
        self.assertEqual(res.status_code, 200)
        self.assertIsNone(self.db.products.find_one({"_id": prd["_id"]}))

    def test_05_supplier_and_customer_crud(self):
        """Test Module 13 & 16: Supplier & Customer Management"""
        with self.client.session_transaction() as sess:
            sess["user_id"] = "test_user_id"
            sess["username"] = "admin"
            sess["user_role"] = "Admin"

        # Add Supplier
        res = self.client.post("/suppliers/add", data={
            "name": "Navi Mumbai Wholesale",
            "contact_person": "Sunil Patil",
            "phone": "+91 99999 11111",
            "email": "sunil@nmw.in",
            "address": "Sector 19, Vashi"
        }, follow_redirects=True)
        self.assertEqual(res.status_code, 200)
        sup = self.db.suppliers.find_one({"name": "Navi Mumbai Wholesale"})
        self.assertIsNotNone(sup)

        # Add Customer
        res = self.client.post("/customers/add", data={
            "name": "Sunita Kamble",
            "phone": "+91 98888 22222",
            "email": "sunita@gmail.com",
            "address": "Dadar Central"
        }, follow_redirects=True)
        self.assertEqual(res.status_code, 200)
        cust = self.db.customers.find_one({"name": "Sunita Kamble"})
        self.assertIsNotNone(cust)

        # Customer Search (Module 17)
        res = self.client.get("/customers?q=98888")
        self.assertIn(b"Sunita Kamble", res.data)

    def test_06_stock_cycle_test(self):
        """
        CRITICAL TEST REQUIRED BY SPEC:
        Initial stock: 10 Rice
        Purchase: 5 Rice -> Expected: 15 Rice
        Sell: 3 Rice -> Expected: 12 Rice
        Cancel sale -> Expected: 15 Rice
        """
        with self.client.session_transaction() as sess:
            sess["user_id"] = "test_user_id"
            sess["username"] = "admin"
            sess["user_role"] = "Admin"

        cat = self.db.categories.find_one()
        sup = self.db.suppliers.find_one()

        # 1. Create a dedicated test product with exact stock 10
        res = self.db.products.insert_one({
            "product_name": "Basmati Rice Test",
            "product_code": "TEST-RICE-01",
            "category_id": cat["_id"],
            "supplier_id": sup["_id"],
            "purchase_price": 60.0,
            "selling_price": 80.0,
            "quantity": 10,
            "minimum_stock": 5,
            "created_at": datetime.now()
        })
        test_prd_id = res.inserted_id

        # Verify Initial: 10
        prd = self.db.products.find_one({"_id": test_prd_id})
        self.assertEqual(prd["quantity"], 10, "Initial stock should be 10")

        # 2. Purchase: 5 Rice -> Expected: 15 Rice
        self.client.post("/purchases/new", data={
            "supplier_id": str(sup["_id"]),
            "purchase_date": "2026-09-11",
            "note": "Test purchase 5 units",
            "product_id[]": [str(test_prd_id)],
            "quantity[]": ["5"],
            "price[]": ["60.0"]
        }, follow_redirects=True)

        prd = self.db.products.find_one({"_id": test_prd_id})
        self.assertEqual(prd["quantity"], 15, "Stock after purchase of 5 should be 15")

        # 3. Sell: 3 Rice -> Expected: 12 Rice
        res_sale = self.client.post("/sales/new", data={
            "invoice_number": "TEST-INV-999",
            "customer_name": "Test Customer",
            "customer_phone": "+91 99999 00000",
            "product_id[]": [str(test_prd_id)],
            "quantity[]": ["3"],
            "price[]": ["80.0"],
            "discount": "0",
            "tax_percent": "0",
            "paid_amount": "240.0"
        }, follow_redirects=True)

        prd = self.db.products.find_one({"_id": test_prd_id})
        self.assertEqual(prd["quantity"], 12, "Stock after sale of 3 should be 12")

        # 4. Cancel Sale -> Expected: 15 Rice (Stock Restitution)
        sale_doc = self.db.sales.find_one({"invoice_number": "TEST-INV-999"})
        self.assertIsNotNone(sale_doc)
        self.client.get(f"/sales/{sale_doc['_id']}/cancel", follow_redirects=True)

        prd = self.db.products.find_one({"_id": test_prd_id})
        self.assertEqual(prd["quantity"], 15, "Stock after cancelling sale should be restored to 15")

        # Verify sale status is marked Cancelled
        updated_sale = self.db.sales.find_one({"_id": sale_doc["_id"]})
        self.assertEqual(updated_sale["status"], "Cancelled")

    def test_07_bill_calculation_test(self):
        """
        CRITICAL TEST REQUIRED BY SPEC:
        Product A: ₹100 × 2 = ₹200
        Product B: ₹50 × 3 = ₹150
        Subtotal: ₹350
        Discount: ₹20
        Tax: ₹0
        Grand Total: ₹330
        Paid: ₹300
        Due: ₹30
        Payment status: Partial
        """
        with self.client.session_transaction() as sess:
            sess["user_id"] = "test_user_id"
            sess["username"] = "admin"
            sess["user_role"] = "Admin"

        cat = self.db.categories.find_one()

        # Create Product A (Price 100, Qty 10)
        prdA = self.db.products.insert_one({
            "product_name": "Product A",
            "product_code": "PRD-A",
            "category_id": cat["_id"],
            "purchase_price": 80.0,
            "selling_price": 100.0,
            "quantity": 10,
            "minimum_stock": 2,
            "created_at": datetime.now()
        })
        # Create Product B (Price 50, Qty 10)
        prdB = self.db.products.insert_one({
            "product_name": "Product B",
            "product_code": "PRD-B",
            "category_id": cat["_id"],
            "purchase_price": 40.0,
            "selling_price": 50.0,
            "quantity": 10,
            "minimum_stock": 2,
            "created_at": datetime.now()
        })

        # Submit Bill
        res = self.client.post("/sales/new", data={
            "invoice_number": "CALC-INV-001",
            "customer_name": "Test Calc Customer",
            "customer_phone": "+91 91111 22222",
            "product_id[]": [str(prdA.inserted_id), str(prdB.inserted_id)],
            "quantity[]": ["2", "3"],
            "price[]": ["100.0", "50.0"],
            "discount": "20.0",
            "tax_percent": "0.0",
            "paid_amount": "300.0"
        }, follow_redirects=True)

        self.assertEqual(res.status_code, 200)

        # Verify Document Calculations in MongoDB
        bill = self.db.sales.find_one({"invoice_number": "CALC-INV-001"})
        self.assertIsNotNone(bill)
        self.assertEqual(bill["subtotal"], 350.0, "Subtotal must be ₹350.00")
        self.assertEqual(bill["discount"], 20.0, "Discount must be ₹20.00")
        self.assertEqual(bill["tax"], 0.0, "Tax must be ₹0.00")
        self.assertEqual(bill["grand_total"], 330.0, "Grand Total must be ₹330.00")
        self.assertEqual(bill["paid_amount"], 300.0, "Paid Amount must be ₹300.00")
        self.assertEqual(bill["due_amount"], 30.0, "Due Amount must be ₹30.00")
        self.assertEqual(bill["payment_status"], "Partial", "Payment status must be 'Partial'")

    def test_08_reports_and_analytics(self):
        """Test Modules 26, 27, 28, 29: Daily, Monthly, Top Products, Profit Reports"""
        with self.client.session_transaction() as sess:
            sess["user_id"] = "test_user_id"
            sess["username"] = "admin"
            sess["user_role"] = "Admin"

        res = self.client.get("/reports/daily")
        self.assertEqual(res.status_code, 200)
        self.assertIn(b"Daily Sales Summary", res.data)

        res = self.client.get("/reports/monthly")
        self.assertEqual(res.status_code, 200)
        self.assertIn(b"Monthly Sales Analysis", res.data)

        res = self.client.get("/reports/top-products")
        self.assertEqual(res.status_code, 200)
        self.assertIn(b"Highest Volume Items", res.data)

        res = self.client.get("/reports/profit")
        self.assertEqual(res.status_code, 200)
        self.assertIn(b"Estimated Profit", res.data)

if __name__ == "__main__":
    unittest.main()
