# Inventory & Billing Management Software for Local Shops
**TY BSc IT — Community Engagement Project (CEP)**

A practical, clean, and reliable web-based Inventory and Point of Sale (POS) Billing Management System specifically engineered for small, local retail shops (such as general stores, provision stores, and grocery marts) to replace manual notebook-based accounts with a modern digital ledger.

---

## 1. Project Overview & Objectives

Small, family-owned retail stores frequently encounter stock discrepancies, untracked customer dues (Khata), missed item expiries, and time-consuming manual billing calculations on paper. 

This project delivers:
- **Fast, Automated POS Checkout**: Instant item total, tax (GST), and discount calculation with printable invoices.
- **Strict Stock Lifecycle Control**: Automatic stock decrements on sale, stock increments on purchase, and automatic replenishment when a bill is cancelled or returned.
- **Khata / Due Ledger Tracking**: Tracking customer outstanding balances and payment statuses (`Paid`, `Partial`, `Due`).
- **Low-Stock & Expiry Surveillance**: Real-time alerts when inventory drops below safety thresholds or nears expiration dates.
- **Examiner-Friendly Architecture**: Built with clear Python Flask routes, PyMongo, and standard HTML5/CSS/JavaScript with no unnecessary enterprise bloat.

---

## 2. Technology Stack

- **Backend**: Python 3, Flask (RESTful routing & session-based auth)
- **Database**: MongoDB & MongoDB Atlas (PyMongo 4.x with automatic local fallback)
- **Frontend**: HTML5, CSS3, JavaScript (ES6)
- **UI Design System**: Tailwind CSS (CDN), Lucide Line Icons, Minimalist Monochrome palette
- **Data Visualization**: Chart.js (7-day sales line chart, monthly revenue bar chart, top-products bar chart)
- **Security**: Werkzeug password hashing (`scrypt`/`pbkdf2`), HTTP sessions
- **Deployment Target**: Render / Any standard Python WSGI host

---

## 3. Exactly 30 Functional Modules Checklist

| Module # | Module Name | Description & Viva Explanation |
|---|---|---|
| **Module 1** | **Admin Login** | Secure username/email login with password hashing via Werkzeug and Flask session management. |
| **Module 2** | **User Management** | CRUD operations to manage store staff and cashiers with `Admin` and `Staff` roles. |
| **Module 3** | **Dashboard** | Real-time overview cards (Today's Sales, Total Products, Customers, Low Stock Alerts) + Chart.js trends. |
| **Module 4** | **Shop Profile** | Store configuration (Name, Owner, Address, Phone, Email, GSTIN) dynamically printed on tax invoices. |
| **Module 5** | **Category Management** | Full CRUD to classify goods (e.g. Grocery, Beverages, Snacks, Personal Care, Household). |
| **Module 6** | **Product Management** | Catalog management including product name, purchase price, selling price, stock, and expiry date. |
| **Module 7** | **Product Search** | Real-time search by product name, product code, or category dropdown filter. |
| **Module 8** | **Stock Management** | Central inventory view displaying current quantities, minimum thresholds, and status badges. |
| **Module 9** | **Low Stock Alert** | Automatically identifies and highlights items where `Current Quantity <= Minimum Stock`. |
| **Module 10** | **Stock Adjustment** | Manual count corrections (+ / -) for damaged goods, lost items, or audit count reconciliations. |
| **Module 11** | **Expiry Tracking** | Monitors expired items (flagged in red) and perishable items expiring within the next 30 days. |
| **Module 12** | **Product Code / Barcode** | Unique alphanumeric codes (`PRD-1001`) assigned to every product for rapid billing lookup. |
| **Module 13** | **Supplier Management** | Directory of wholesale vendors and distributors with contact numbers and warehouse addresses. |
| **Module 14** | **Purchase Entry** | Records inward shipments from suppliers; **automatically increments product inventory counts**. |
| **Module 15** | **Purchase History** | Searchable audit ledger of previous wholesale procurements with date filters. |
| **Module 16** | **Customer Management** | Customer directory tracking personal contacts, total lifetime purchases, and due balances. |
| **Module 17** | **Customer Search** | Instant filter by customer name or 10-digit mobile number. |
| **Module 18** | **Customer Purchase History** | Ledger view showing all previous bills and payments for a specific customer. |
| **Module 19** | **Customer Due / Payment Tracking**| Tracks bill grand totals, paid amounts, and due balances with statuses (`Paid`, `Partial`, `Due`). |
| **Module 20** | **New Billing (POS Screen)** | Interactive point-of-sale interface to select customers and add multiple products to a cart. |
| **Module 21** | **Automatic Invoice Number** | Generates unique, sequential invoice codes (`INV-0001`, `INV-0002`) on bill completion. |
| **Module 22** | **Automatic Bill Calculation** | Real-time calculation: `Item Total = Qty × Rate`, `Subtotal`, `Discount`, `Tax (GST%)`, `Grand Total`, `Due`. |
| **Module 23** | **Print / Download Invoice** | Clean, printable tax invoice format with `@media print` CSS hiding navigation bars. |
| **Module 24** | **Sales History** | Comprehensive sales ledger with filters for invoice number, payment status, and sale date. |
| **Module 25** | **Sales Return / Cancel Bill** | Cancels an invoice, flags status as `Cancelled`, and **automatically restores sold stock back to inventory**. |
| **Module 26** | **Daily Sales Report** | Day-wise breakdown of total invoices generated, revenue collected, and units sold. |
| **Module 27** | **Monthly Sales Report** | Month-by-month sales summary with a daily distribution bar chart powered by Chart.js. |
| **Module 28** | **Top Selling Products** | Identifies top-performing products ranked by quantity sold and revenue generated. |
| **Module 29** | **Profit & Inventory Report** | Estimated Gross Profit (`Revenue - Purchase Cost`) and total inventory valuation at cost & retail. |
| **Module 30** | **Settings & Demo Seeder** | Global application preferences and one-click button to reload default Indian local store demo data. |

---

## 4. Key Database Lifecycle Rules

### Rule 1: Purchase Inward
$$\text{Product Stock} \leftarrow \text{Product Stock} + \text{Purchased Quantity}$$

### Rule 2: Sale Checkout
$$\text{Product Stock} \leftarrow \text{Product Stock} - \text{Sold Quantity}$$
*(Checkout is blocked if $\text{Sold Quantity} > \text{Available Stock}$)*

### Rule 3: Sale Cancellation / Return
$$\text{Product Stock} \leftarrow \text{Product Stock} + \text{Sold Quantity}$$
*(Sale status is updated to `Cancelled`—audit trail is never permanently erased)*

### Rule 4: Financial Calculation
$$\text{Item Total} = \text{Quantity} \times \text{Selling Price}$$
$$\text{Subtotal} = \sum \text{Item Totals}$$
$$\text{Discounted Subtotal} = \max(0, \text{Subtotal} - \text{Discount})$$
$$\text{Tax (GST)} = \frac{\text{Discounted Subtotal} \times \text{Tax Rate \%}}{100}$$
$$\text{Grand Total} = \text{Discounted Subtotal} + \text{Tax}$$
$$\text{Due Amount} = \max(0, \text{Grand Total} - \text{Paid Amount})$$

---

## 5. Database Schema (MongoDB Collections)

```
inventory_billing_db
├── users             # Admin and staff credentials (hashed password, role)
├── categories        # Category names, descriptions, timestamps
├── products          # Name, code, category_id, supplier_id, buy/sell prices, stock, min_stock, expiry
├── suppliers         # Name, contact person, phone, email, address
├── purchases         # Supplier, item list, total_amount, purchase_date, memo
├── customers         # Name, phone, email, address, total_purchases, total_due
├── sales             # Invoice number, customer, item array, subtotal, tax, discount, grand total, paid, due
├── stock_movements   # Product_id, type (IN/OUT), quantity, reason, reference_id, timestamp
└── settings          # Shop profile (name, owner, phone, email, address, GSTIN, default tax)
```

---

## 6. Installation & How to Run Locally

### Prerequisites
- Python 3.9 or higher
- pip package manager

### Step 1: Clone or Open Project Folder
```bash
cd d:/11-09-2026
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Configure Environment Variables
Create or verify your `.env` file:
```env
MONGO_URI=mongodb+srv://mernstudent:Akshay20@cluster0.vwp0bzh.mongodb.net/inventory_billing_db?retryWrites=true&w=majority
SECRET_KEY=dev_secret_key_student_cep_2026
FLASK_APP=app.py
FLASK_ENV=development
PORT=5000
```

> **Note on MongoDB Atlas**:
> The application connects to MongoDB Atlas using your configured `MONGO_URI`. If your laptop is offline or if MongoDB Atlas Network Access is restricted during viva, the app automatically switches to an in-memory high-fidelity local fallback so your project **never crashes** during a demonstration.

### Step 4: Run the Application
```bash
python app.py
```
Open your browser and navigate to: **`http://127.0.0.1:5000`**

---

## 7. Demo Login Credentials

| Role | Username | Password | Privileges |
|---|---|---|---|
| **Admin (Store Owner)** | `admin` | `admin123` | Full access: All 30 modules, user management, profile settings, reports. |
| **Staff (Cashier)** | `suresh` | `staff123` | Operational access: POS Billing, products, customers, stock overview. |

---

## 8. Automated Testing

To run the automated verification suite:
```bash
python test_app.py
```
This tests:
1. Admin & staff authentication.
2. Category, Product, Supplier, Customer CRUD.
3. Real-time product search & barcode lookup.
4. **Stock Cycle Test**: (10 initial $\rightarrow$ Purchase 5 $\rightarrow$ 15 $\rightarrow$ Sell 3 $\rightarrow$ 12 $\rightarrow$ Cancel sale $\rightarrow$ 15).
5. **Billing Calculation Test**: Subtotal, discount, tax, grand total, paid, due balance, and `Partial` payment status.
6. Daily, monthly, top products, and profit reports.

---

## 9. Deployment to Render

1. Push code to your GitHub repository.
2. Log in to [Render](https://render.com) and create a **New Web Service**.
3. Connect your GitHub repository.
4. Set Build Command: `pip install -r requirements.txt`
5. Set Start Command: `python app.py` (or `gunicorn app:app`)
6. Add Environment Variables:
   - `MONGO_URI`: `mongodb+srv://...`
   - `SECRET_KEY`: `<your_secret_key>`
7. In MongoDB Atlas, go to **Network Access** $\rightarrow$ Click **Add IP Address** $\rightarrow$ Select **Allow Access From Anywhere (`0.0.0.0/0`)**.

---

## 10. College Viva & Project Defense Guide

### Q1: Why did you choose Python Flask and MongoDB for this project?
> **Answer**: Flask is a lightweight WSGI microframework that allows us to cleanly map HTTP routes to simple Python functions without unnecessary boilerplate. MongoDB is a document-oriented NoSQL database that naturally represents retail records like sales invoices, where an invoice has an embedded array of line items with varied quantities and rates.

### Q2: How does the system ensure stock integrity when a bill is cancelled?
> **Answer**: When an invoice is cancelled in Module 25, the application loops through each item in the sale document and executes an `$inc` operation on the product collection with the positive quantity previously sold. It also logs an audit entry in the `stock_movements` collection and updates the sale status to `Cancelled` rather than deleting the record, preserving complete audit trails.

### Q3: How is password security handled?
> **Answer**: Plaintext passwords are never stored in the database. When a user is registered or updated, Werkzeug's `generate_password_hash()` hashes the password with salt. On login, `check_password_hash()` securely validates the credentials against the stored hash.

### Q4: How does the printable invoice work without heavy PDF dependencies?
> **Answer**: In Module 23, we use a clean HTML invoice template paired with `@media print` CSS styles. The print stylesheet automatically hides the sidebar, navigation bar, and buttons, allowing the shopkeeper to print directly to a POS thermal printer or save as PDF using the browser's native print engine (`Ctrl+P` or `window.print()`).
