# APNA BAZAR — INVENTORY & BILLING SOFTWARE FOR LOCAL SHOPS
## Community Engagement Project (CEP) Report
### Bachelor of Science in Information Technology (TY BSc IT)

---

# PRELIMINARY PAGES

## 1. TITLE PAGE

```
================================================================================
                           A PROJECT REPORT ON

                               APNA BAZAR
              INVENTORY & BILLING SOFTWARE FOR LOCAL SHOPS

               Submitted in partial fulfillment of the requirements 
                   for the award of the Degree of
            BACHELOR OF SCIENCE IN INFORMATION TECHNOLOGY (BSc IT)

                               Submitted By:
                              AKSHAY KHAPARE
                           Roll Number: [Roll No]

                         Under the Guidance of:
                           [Project Guide Name]
                   Department of Information Technology

                         [COLLEGE NAME & EMBLEM]
                   [Affiliated to University of Mumbai]
                              Academic Year:
                                2025 - 2026
================================================================================
```

---

## 2. CERTIFICATE

```
================================================================================
                         DEPARTMENT OF INFORMATION TECHNOLOGY
                                [COLLEGE NAME]
                                 CERTIFICATE

This is to certify that the project entitled:
"APNA BAZAR — INVENTORY & BILLING SOFTWARE FOR LOCAL SHOPS"

is a bona fide record of work carried out by:
                              AKSHAY KHAPARE
                           Roll Number: [Roll No]

in partial fulfillment of the requirements for the Degree of Bachelor of Science 
in Information Technology (TY BSc IT) under the University during the academic 
year 2025 - 2026.


_______________________                                 _______________________
    Internal Guide                                         Head of Department
[Project Guide Name]                                     [HOD Name & Signature]


_______________________                                 _______________________
    External Examiner                                        College Seal
================================================================================
```

---

## 3. DECLARATION

```
================================================================================
                                 DECLARATION

I hereby declare that the project entitled "APNA BAZAR — INVENTORY & BILLING 
SOFTWARE FOR LOCAL SHOPS" submitted to the Department of Information Technology, 
[College Name], in partial fulfillment of the requirements for the award of 
the degree of Bachelor of Science in Information Technology, is an original 
work carried out by me under the supervision and guidance of [Project Guide Name].

The matter embodied in this project report has not been submitted by me or 
anyone else for the award of any other degree or diploma to any other University 
or Institute.


Date: September 11, 2026
Place: Mumbai, Maharashtra                              _______________________
                                                            Akshay Khapare
                                                          TY BSc IT, Roll No: [ ]
================================================================================
```

---

## 4. ACKNOWLEDGEMENT

I take this opportunity to express my profound gratitude and deep regards to my guide, **[Project Guide Name]**, for his/her exemplary guidance, valuable feedback, and constant encouragement throughout the development of this Community Engagement Project (CEP).

I am also immensely thankful to **[Head of Department]**, Head of the Department of Information Technology, and our respected Principal for providing all the required infrastructure and computing facilities.

I express my heartfelt gratitude to the local shopkeepers and retail merchants of our community who graciously shared their daily challenges regarding manual khata keeping, billing errors, and inventory tracking. Their real-world operational insights directly shaped the requirements and design of **APNA BAZAR**.

Lastly, I thank my parents, family, and peers for their moral support, motivation, and assistance throughout my academic journey.

**Akshay Khapare**  
Third Year BSc Information Technology  

---

## 5. TABLE OF CONTENTS

| Chapter No. | Chapter Title | Page No. |
| :--- | :--- | :--- |
| | **Preliminary Pages** | i - vii |
| | 1. Title Page | i |
| | 2. Certificate | ii |
| | 3. Declaration | iii |
| | 4. Acknowledgement | iv |
| | 5. Table of Contents | v |
| | 6. List of Tables | vi |
| | 7. List of Figures | vii |
| **Chapter 01** | **Introduction** | **1 - 5** |
| 1.1 | Introduction to Retail Inventory & Billing Management | 1 |
| 1.2 | Background of the Project | 2 |
| 1.3 | Purpose of the System | 3 |
| 1.4 | Scope of the Project | 4 |
| **Chapter 02** | **Problem Statement and Objectives** | **6 - 9** |
| 2.1 | Problem Statement | 6 |
| 2.2 | Existing Manual System | 7 |
| 2.3 | Limitations of the Existing System | 7 |
| 2.4 | Proposed System (APNA BAZAR) | 8 |
| 2.5 | System Objectives | 9 |
| **Chapter 03** | **System Architecture and Theoretical Foundation** | **10 - 15** |
| 3.1 | System Architecture Overview | 10 |
| 3.2 | Technology Stack | 11 |
| 3.3 | Three-Tier Architectural Pattern | 12 |
| 3.4 | System Workflow | 13 |
| 3.5 | Stock Lifecycle & Business Rules | 14 |
| 3.6 | Mathematical Billing & Khata Due Calculations | 15 |
| **Chapter 04** | **Literature Review** | **16 - 19** |
| 4.1 | Overview of Retail Management Systems | 16 |
| 4.2 | Review of Existing Retail Software (Tally, Vyapar, Marg) | 17 |
| 4.3 | Comparative Analysis: Existing vs. Proposed System | 18 |
| 4.4 | Modern Web Technologies in Community Retail | 19 |
| **Chapter 05** | **System Analysis and Design** | **20 - 32** |
| 5.1 | System Requirements (Hardware & Software) | 20 |
| 5.2 | Functional Requirements (The 30 Core Modules) | 21 |
| 5.3 | System Design Diagrams | 25 |
| 5.3.1 | Use Case Diagram | 25 |
| 5.3.2 | Data Flow Diagrams (DFD Level 0, Level 1, Level 2) | 27 |
| 5.3.3 | Entity Relationship Diagram (MongoDB Document Schema) | 29 |
| 5.3.4 | Activity Diagram (POS Billing & Stock Cycle) | 30 |
| 5.3.5 | Sequence Diagram | 31 |
| **Chapter 06** | **Implementation** | **33 - 42** |
| 6.1 | Development Environment & Setup | 33 |
| 6.2 | Frontend Implementation (Monochrome UI, Print Styles) | 34 |
| 6.3 | Backend Implementation (Flask Routes & Decorators) | 36 |
| 6.4 | Database Implementation (MongoDB Atlas & Collections) | 38 |
| 6.5 | Authentication & Role-Based Security | 39 |
| 6.6 | High-Fidelity Resilient Fallback Engine (`mongomock`) | 40 |
| 6.7 | Database Seeding (Authentic Indian Retail Dataset) | 41 |
| 6.8 | Summary of 30 Functional Modules Code Structure | 42 |
| **Chapter 07** | **Testing and Results** | **43 - 50** |
| 7.1 | Testing Methodology | 43 |
| 7.2 | Automated Integration & Unit Test Cases (TC01 - TC08) | 44 |
| 7.3 | Test Execution Results | 47 |
| 7.4 | System Verification Screenshots & Walkthrough | 48 |
| **Chapter 08** | **Conclusion** | **51 - 53** |
| 8.1 | Project Summary | 51 |
| 8.2 | Key Achievements | 51 |
| 8.3 | Benefits to Local Retailers & Community | 52 |
| 8.4 | Limitations of the Current System | 53 |
| **Chapter 09** | **Future Enhancements** | **54 - 56** |
| 9.1 | Hardware Barcode Scanner & Thermal ESC/POS Integration | 54 |
| 9.2 | Automated WhatsApp & SMS Khata Reminders | 54 |
| 9.3 | Dynamic UPI QR Code on Invoices | 55 |
| 9.4 | Mobile Progressive Web App (PWA) | 55 |
| 9.5 | Multi-Store Centralized Cloud Synchronization | 56 |
| **Chapter 10** | **References** | **57 - 59** |
| 10.1 | Reference Books and Academic Papers | 57 |
| 10.2 | Official Documentation & API References | 58 |
| 10.3 | Online Technical Portals & Standards | 59 |

---

## 6. LIST OF TABLES

| Table No. | Title | Page No. |
| :--- | :--- | :--- |
| Table 4.1 | Comparison between Existing Commercial Systems and APNA BAZAR | 18 |
| Table 5.1 | Minimum Hardware Specifications | 20 |
| Table 5.2 | Software Stack Requirements | 20 |
| Table 5.3 | The 30 Functional Modules Specification Index | 21 |
| Table 5.4 | MongoDB Database Collections Schema Summary | 29 |
| Table 7.1 | Test Suite Case Matrix (TC01 to TC08) | 44 |
| Table 7.2 | Stock Lifecycle Invariance Test Results | 45 |
| Table 7.3 | Billing Arithmetic Verification Test Results | 46 |
| Table 7.4 | Test Execution Summary Report | 47 |

---

## 7. LIST OF FIGURES

| Figure No. | Title | Page No. |
| :--- | :--- | :--- |
| Figure 3.1 | Three-Tier Architecture of APNA BAZAR | 12 |
| Figure 3.2 | End-to-End System Workflow | 13 |
| Figure 3.3 | Inventory Stock Lifecycle State Diagram | 14 |
| Figure 5.1 | System Use Case Diagram | 26 |
| Figure 5.2 | Level 0 Context Data Flow Diagram (DFD) | 27 |
| Figure 5.3 | Level 1 Data Flow Diagram (Billing & Inventory) | 28 |
| Figure 5.4 | Level 2 Data Flow Diagram (POS Billing Engine) | 28 |
| Figure 5.5 | Activity Diagram: Point of Sale Checkout Flow | 30 |
| Figure 5.6 | Sequence Diagram: Invoice Generation and Inventory Stock Update | 32 |
| Figure 7.1 | Secure Admin Login Screen | 48 |
| Figure 7.2 | Executive Monochrome Dashboard Overview | 48 |
| Figure 7.3 | Product Catalog & Inventory Directory | 49 |
| Figure 7.4 | Interactive Point-of-Sale (POS) Billing Cart | 49 |
| Figure 7.5 | Formatted Tax Invoice Ready for Printing | 50 |
| Figure 7.6 | Monthly Revenue & Top Selling Products Chart Visualizations | 50 |

---

# CHAPTER 01: INTRODUCTION

### 1.1 Introduction to Retail Inventory & Billing Management
Small local retail businesses, corner grocery shops (*Kirana* stores), stationery counters, and provision vendors are the backbone of local neighborhood commerce across India. These community shops conduct hundreds of small-value, rapid transactions every day, stocking thousands of unique stock-keeping units (SKUs) ranging from grain staples and cooking oils to packaged foods, personal care items, and stationery.

Despite the rapid modernization of tier-1 e-commerce platforms, local brick-and-mortar grocery and provision merchants still predominantly depend on manual bookkeeping. Daily receipts are penned down into physical cash memos, customer credit balances are logged in paper ledgers known traditionally as the *Khata*, and stock replenishments are managed through visual estimation rather than systematic metrics. 

**APNA BAZAR** is a modern, lightweight, web-based Inventory and Point-of-Sale (POS) Billing Management System specifically engineered to solve these challenges. Developed as a TY BSc IT Community Engagement Project (CEP), APNA BAZAR brings digital accuracy, automatic billing arithmetic, live stock tracking, supplier management, and customer credit recovery into an accessible, clean, monochrome web application.

### 1.2 Background of the Project
During our community engagement surveys conducted with small retail merchants in our local neighborhood, several recurring pain points were observed:
1. **Mathematical Mistakes during Rush Hours**: During peak morning and evening rush hours, shopkeepers compute bill totals, discounts, and change manually or using basic hand calculators. Miscalculations lead to revenue loss or customer disputes.
2. **Untracked Credit (Khata) Receivables**: In community retail, offering short-term credit to trusted neighborhood families is an essential business practice. However, paper ledger books get misplaced, pages tear, and payments go unrecorded, resulting in uncollected debts.
3. **Stockouts of Essential Goods**: Without real-time stock thresholds, shopkeepers discover items are out of stock only when a customer asks for them, leading to lost sales and dissatisfied patrons.
4. **Expired Goods on Shelves**: Packaged consumer goods often expire unnoticed on storage shelves, causing financial write-offs and health risks.
5. **Over-Engineered Commercial Software**: Existing enterprise ERP systems (like SAP, Tally, or Marg) are prohibitively complex, expensive, require weeks of specialized accounting training, and rely on heavy desktop software installations.

These findings established the need for a simplified, web-based solution that any shopkeeper or assistant can master in under ten minutes without accounting background.

### 1.3 Purpose of the System
The primary purpose of APNA BAZAR is to empower local shopkeepers with a simple, transparent, and dependable digital tool to:
- Generate instant, professional, printed or digital customer invoices with automated tax and discount math.
- Automatically track inventory quantities, incrementing on supplier purchases and decrementing on POS checkouts.
- Provide automated low-stock warnings before essential goods run out.
- Monitor product expiry dates with 30-day advance warnings.
- Maintain an accurate, transparent customer ledger (*Khata*) recording partial payments and outstanding credit balances.
- Deliver clear analytical insights into daily sales, monthly revenues, fast-moving items, and net profit valuation without requiring complex accounting knowledge.

### 1.4 Scope of the Project
The scope of APNA BAZAR encompasses the operational requirements of single-location local retail stores:
- **User Roles**: Two distinct privilege levels:
  - **Admin**: Complete access to shop settings, user accounts, product pricing, supplier entries, inventory adjustments, sales returns, and profit analytics.
  - **Staff / Cashier**: Fast access to POS billing checkout, customer ledger lookups, product stock searches, and invoice printing.
- **Inventory Domain**: Up to tens of thousands of products categorized logically with barcode/SKU identifiers, cost rates, retail prices, expiry stamps, and reorder levels.
- **Supplier & Purchase Domain**: Inward purchase tracking from wholesale distributors with automatic stock addition.
- **Billing & POS Domain**: Multi-item fast cart, dynamic discount calculation, optional GST, auto-sequence invoice numbering, and print-ready invoices.
- **Reporting & Business Intelligence**: Daily metrics, monthly Chart.js trends, top-selling volume rankings, and gross profit valuation.
- **Resilient Operations**: Connected to MongoDB Atlas cloud cluster with automated in-memory local fallback (`mongomock`) to ensure the store never stops operating even during internet downtime.

---

# CHAPTER 02: PROBLEM STATEMENT AND OBJECTIVES

### 2.1 Problem Statement
"Local community retail shop owners face substantial revenue leakages, operational delays, inventory stockouts, and uncollected customer debts due to reliance on manual, error-prone paper notebooks, cash memos, and traditional khata ledgers. Existing commercial retail software solutions are excessively complex, expensive, and difficult for non-technical retail workers to operate."

### 2.2 Existing Manual System
In the existing traditional setup:
1. When a customer arrives, the shopkeeper pulls goods from shelves, notes prices on a scrap memo slip, and totals them manually.
2. If credit is extended, the shopkeeper writes the balance in a bound notebook under the customer's name.
3. When stock arrives from wholesale vendors, paper delivery challans are filed into cardboard folders; quantities are rarely entered into a structured registry.
4. Physical inventory auditing occurs once a year or during festive seasons, resulting in delayed discovery of damaged or expired goods.

### 2.3 Limitations of the Existing System
- **High Error Rate**: Arithmetic errors in addition, discounts, and tax computation.
- **Time Inefficiency**: Manual writing of invoices slows checkout queues during busy hours.
- **Lack of Real-Time Stock Visibility**: No mechanism to know stock counts without manually climbing storage racks.
- **Disputed Khata Records**: Customers may dispute handwritten credit balances due to illegible handwriting or missing dates.
- **Zero Business Analytics**: The shopkeeper cannot accurately determine which items produce the highest profit margins or predict seasonal demand.
- **Vulnerability to Physical Damage**: Notebooks can be lost, damaged by moisture, or destroyed by pests.

### 2.4 Proposed System (APNA BAZAR)
APNA BAZAR replaces manual paper operations with a high-performance web application featuring:
- An ultra-fast, live Point-of-Sale (POS) interface with instant item search and automatic line calculations.
- Strict database-enforced stock tracking: Stock increases upon purchase recording, decreases upon sales checkout, and is restored upon bill cancellation.
- Automated sequential invoice generation (`INV-0001`, `INV-0002`).
- Dedicated Low Stock Alert and Expiry Tracking engines.
- Clear Customer Khata ledger detailing total orders, payments made, and outstanding dues.
- Minimalist, distraction-free monochrome user interface tailored for fast readability.
- Cloud data persistence on MongoDB Atlas with an offline fallback.

### 2.5 System Objectives
1. **Develop an Intuitive User Experience**: Build a clean, black-and-white SaaS-style interface that requires zero training.
2. **Automate Inventory Balancing**: Implement automated inventory tracking where stock levels mathematically correspond to purchases, sales, and returns.
3. **Eliminate Billing Errors**: Ensure 100% calculation accuracy for subtotals, item totals, discounts, GST rates, customer payments, and due balances.
4. **Digitize Customer Credit (*Khata*)**: Provide accurate, timestamped credit ledgers for neighborhood customers.
5. **Provide Business Intelligence**: Render real-time visual charts and metrics for daily revenue, monthly sales, best-selling products, and inventory valuation.
6. **Ensure High Availability**: Implement resilient database connectivity with automated local in-memory fallback.

---

# CHAPTER 03: SYSTEM ARCHITECTURE AND THEORETICAL FOUNDATION

### 3.1 System Architecture Overview
APNA BAZAR is designed according to the classical **Three-Tier Architectural Model**, separating the presentation, business logic, and database persistence layers. This separation ensures high modularity, ease of debugging, straightforward maintenance, and rapid extensibility.

```
+-----------------------------------------------------------------------+
|                         PRESENTATION LAYER                            |
|     Browser Client (HTML5, Tailwind CSS Monochrome, JS, Chart.js)    |
+-----------------------------------------------------------------------+
                                  |
                        HTTP Requests / JSON / HTML
                                  |
                                  v
+-----------------------------------------------------------------------+
|                        APPLICATION / LOGIC LAYER                      |
|          Python Flask WSGI Application (app.py, utils/helpers.py)      |
|    - Route Dispatchers        - Session Security & Werkzeug Hashes   |
|    - POS Billing Engine       - Stock Balancing Controllers           |
|    - Context Processors       - Mathematical Calculators              |
+-----------------------------------------------------------------------+
                                  |
                       PyMongo / TLS / Wire Protocol
                                  |
                                  v
+-----------------------------------------------------------------------+
|                            DATA STORAGE LAYER                         |
|   Primary: MongoDB Atlas (Cloud Cluster `inventory_billing_db`)       |
|   Fallback: Mongomock In-Memory Engine (Resilient Offline Mode)       |
+-----------------------------------------------------------------------+
```
*Figure 3.1: Three-Tier Architecture of APNA BAZAR*

### 3.2 Technology Stack
1. **Python (Backend Engine)**:
   - Interpreted, high-level, dynamically typed language known for clarity and developer productivity.
   - Version: Python 3.9+ / 3.11 / 3.14 compatible.
2. **Flask (Web Framework)**:
   - Lightweight WSGI microframework offering routing, HTTP request handling, session cookies, and Jinja2 server-side rendering without rigid boilerplate.
3. **PyMongo & MongoDB Atlas (Database Layer)**:
   - PyMongo is the official driver facilitating communication with MongoDB Atlas.
   - MongoDB Atlas provides a managed, scalable cloud NoSQL document store storing BSON data.
4. **Werkzeug (Security Layer)**:
   - Cryptographic password hashing (`scrypt` / `pbkdf2:sha256`) preventing plaintext password vulnerability.
5. **Mongomock (Resilience Engine)**:
   - Drop-in in-memory PyMongo simulation ensuring the application continues serving requests even if the internet drops.
6. **Frontend Framework & Libraries**:
   - **Tailwind CSS (Play CDN)**: Utility-first CSS configured with custom neutral monochrome tokens (`#f9fafb`, `#111827`, `#e5e7eb`).
   - **Lucide Line Icons**: Clean SVG icon system.
   - **Chart.js (v4.x)**: Responsive canvas charts for sales trends and volume rankings.
   - **Vanilla JavaScript**: Dynamic client-side DOM manipulation for the POS cart.

### 3.3 Three-Tier Architectural Pattern
- **Tier 1: Presentation Tier (Client)**: 
  Executed inside the merchant's web browser. Composed of semantic HTML5 templates rendered via Jinja2, Tailwind styling tokens, print media queries, and responsive JavaScript handlers that calculate live invoice rows without requiring full-page reloads.
- **Tier 2: Application Logic Tier (Server)**:
  Implemented in Python using Flask. Handles route protection via decorators (`@login_required`, `@admin_required`), form validation, sequential invoice generation, mathematical validation, and database operations.
- **Tier 3: Data Tier (Persistence)**:
  MongoDB Atlas manages eight primary collections (`users`, `products`, `categories`, `suppliers`, `purchases`, `customers`, `sales`, `stock_movements`, `settings`).

### 3.4 System Workflow
The daily retail operational lifecycle in APNA BAZAR flows logically across inventory inwarding, sales, customer settlement, and analytics:

```
[Supplier] ---> Inward Purchase ---> [Stock Incremented]
                                             |
                                             v
[Customer] ---> POS Billing Cart ---> [Stock Decremented] ---> [Tax Invoice Generated]
       |                                     |
       |-- Extends Credit (Due Balance)      |-- Customer Cancels Bill
       v                                     v
[Customer Ledger Updated]             [Stock Restored to Inventory]
```
*Figure 3.2: End-to-End System Workflow*

### 3.5 Stock Lifecycle & Business Rules
To ensure inventory integrity, APNA BAZAR strictly enforces three programmatic database state invariants:

```
                         +-------------------------+
                         |     Supplier Purchase   |
                         +-------------------------+
                                      |
                                      | (Stock +Qty)
                                      v
+------------------+         +-----------------+         +------------------+
|   Out of Stock   | <------ |  In Stock (Qty) | ------> |  Low Stock Alert |
|    (Qty == 0)    |         +-----------------+         |  (Qty <= MinQty) |
+------------------+                  |                  +------------------+
                                      | (Sales -Qty)
                                      v
                         +-------------------------+
                         |      POS Checkout       |
                         +-------------------------+
                                      |
                                      | (Customer Return / Cancel +Qty)
                                      v
                         +-------------------------+
                         |     Restored to Stock   |
                         +-------------------------+
```
*Figure 3.3: Inventory Stock Lifecycle State Diagram*

1. **Inward Purchase Increment Rule**:
   $$\text{Stock}_{\text{new}} = \text{Stock}_{\text{current}} + Q_{\text{purchased}}$$
2. **Sales Checkout Decrement Rule**:
   $$\text{Stock}_{\text{new}} = \text{Stock}_{\text{current}} - Q_{\text{sold}} \quad (\text{Valid only if } Q_{\text{sold}} \le \text{Stock}_{\text{current}})$$
3. **Bill Cancellation / Return Restitution Rule**:
   $$\text{Stock}_{\text{new}} = \text{Stock}_{\text{current}} + Q_{\text{returned}}$$

### 3.6 Mathematical Billing & Khata Due Calculations
The POS billing engine applies strict financial formulas:
1. **Item Line Total**:
   $$\text{Line Total}_i = \text{Quantity}_i \times \text{Selling Price}_i$$
2. **Gross Subtotal**:
   $$\text{Subtotal} = \sum_{i=1}^{n} \text{Line Total}_i$$
3. **Discounted Subtotal**:
   $$\text{Discounted Subtotal} = \max(0, \text{Subtotal} - \text{Discount})$$
4. **Goods & Services Tax (GST)**:
   $$\text{Tax Amount} = \frac{\text{Discounted Subtotal} \times \text{Tax Rate \%}}{100}$$
5. **Invoice Grand Total**:
   $$\text{Grand Total} = \text{Discounted Subtotal} + \text{Tax Amount}$$
6. **Customer Due Balance (Khata Extension)**:
   $$\text{Due Amount} = \max(0, \text{Grand Total} - \text{Amount Paid})$$
   - If $\text{Amount Paid} \ge \text{Grand Total}$: Status = `Paid`
   - If $0 < \text{Amount Paid} < \text{Grand Total}$: Status = `Partial`
   - If $\text{Amount Paid} = 0$: Status = `Due`

---

# CHAPTER 04: LITERATURE REVIEW

### 4.1 Overview of Retail Management Systems
Modern retail management systems originated with mechanical cash registers patented by James Ritty in 1879. Over the decades, these evolved into electronic point-of-sale terminals and eventually distributed enterprise resource planning (ERP) packages. In developed economies, retail automation has achieved near 100% penetration through integrated cloud terminals.

However, in developing nations like India, small grocery and provision merchants (Kirana shops) continue to operate in the unorganized sector. While mega-supermarkets leverage enterprise systems, neighborhood micro-merchants remain reliant on physical cash boxes and handwritten ledgers due to economic, technical, and operational barriers.

### 4.2 Review of Existing Retail Software (Tally, Vyapar, Marg)
1. **TallyPrime**:
   - *Strengths*: Comprehensive accounting, double-entry bookkeeping, multi-currency support, compliance with Indian GST regulations.
   - *Limitations*: Steep learning curve requiring formal commerce education, keyboard-shortcut-driven interface, expensive annual licenses, heavy Windows desktop installation.
2. **Vyapar**:
   - *Strengths*: Tailored for small business billing, mobile Android application, inventory alerts.
   - *Limitations*: Advanced features locked behind recurring subscription paywalls, interface is crowded with banners and prompts, local synchronization occasionally causes data conflicts.
3. **Marg ERP 9+**:
   - *Strengths*: Highly detailed pharmaceutical and FMCG distribution features, batch-level tracking.
   - *Limitations*: Dated legacy UI with confusing navigation, complex setup, prone to database corruption if power fails unexpectedly.

### 4.3 Comparative Analysis: Existing vs. Proposed System

| Feature / Metric | Traditional Tally / Marg | Mobile Apps (Vyapar) | APNA BAZAR (Proposed) |
| :--- | :--- | :--- | :--- |
| **Target User** | Professional Accountants | Tech-savvy Merchants | Local Shopkeeper & Cashier |
| **Learning Curve** | High (Weeks of Training) | Moderate | Immediate (< 10 Minutes) |
| **License Cost** | Expensive (₹18,000 - ₹54,000) | Recurring Subscription | Open Source & Free for College/Community |
| **UI Aesthetics** | Legacy Cluttered Windows | Busy with Banners | Minimalist Monochrome (High Contrast) |
| **Installation** | Heavy Desktop Executable | Mobile App Store | Zero Install (Any Browser on PC/Tablet) |
| **Stock Automation** | Complex Journals | Basic | Real-Time Automatic (+Purchase / -Sale) |
| **Offline Resilience**| Local DB Only | Cloud Dependent Sync | Cloud Atlas + Automatic In-Memory Fallback |
| **Khata Tracking** | Complex Credit Ledger | Mobile SMS Prompts | Direct Customer Balance Tracking |

*Table 4.1: Comparison between Existing Commercial Systems and APNA BAZAR*

### 4.4 Modern Web Technologies in Community Retail
Recent advances in lightweight web technologies have made web-based point-of-sale systems practical for local retail:
- **Responsive Layouts**: Flexible web apps run cleanly on refurbished desktop computers, laptops, or low-cost tablets already owned by shopkeepers.
- **Browser-Native Printing**: CSS `@media print` eliminates the need for proprietary printer drivers, enabling standard browser print dialogs to output clean 80mm receipts or A4 tax invoices.
- **Microframeworks**: Python Flask allows developers to build fast, lightweight web applications without the overhead of heavy enterprise enterprise frameworks.

---

# CHAPTER 05: SYSTEM ANALYSIS AND DESIGN

### 5.1 System Requirements

#### 5.1.1 Hardware Requirements
- **Processor**: Intel Core i3 / AMD Ryzen 3 or equivalent (1.5 GHz or higher).
- **RAM**: 2 GB Minimum (4 GB Recommended).
- **Hard Disk / Storage**: 500 MB free disk space for application files and local database caching.
- **Display**: 1024 x 768 minimum resolution (Optimized for 1366 x 768 and 1920 x 1080).
- **Peripherals**: Standard keyboard, mouse, and any standard desktop printer (A4 or thermal) supporting browser printing.

#### 5.1.2 Software Requirements
- **Operating System**: Platform independent (Windows 10/11, Linux Ubuntu 20.04+, macOS).
- **Runtime Environment**: Python 3.9, 3.10, 3.11, or 3.14.
- **Database Engine**: MongoDB Atlas Cloud Cluster / PyMongo Driver.
- **Web Browser**: Google Chrome 90+, Mozilla Firefox 88+, Microsoft Edge 90+, or Apple Safari 14+.
- **CSS Framework**: Tailwind CSS (loaded via lightweight Play CDN).

### 5.2 Functional Requirements (The 30 Core Modules)
The application is structured into exactly 30 distinct functional modules:

| Module No. | Module Name | Route / Endpoint | Description |
| :---: | :--- | :--- | :--- |
| **M01** | Admin Login | `/login` & `/logout` | Secure session authentication with Werkzeug password verification. |
| **M02** | User Management | `/users` | Admin CRUD interface to create, list, edit, and remove staff/cashier users. |
| **M03** | Dashboard Overview | `/dashboard` | Executive KPIs (Daily Sales, Monthly Revenue, Low Stock Items, Due Balance) + 7-Day Chart. |
| **M04** | Shop Profile | `/settings` | Configuration of store name ("APNA BAZAR"), owner, phone, address, and GSTIN. |
| **M05** | Category Management | `/categories` | Organize items into Grocery, Snacks, Beverages, Household, etc., with product counts. |
| **M06** | Product Management | `/products` | Complete CRUD for retail items with barcode, pricing, stock quantity, and expiry. |
| **M07** | Product Search | `/products?q=...` | Instant server-side search filtering by product name, SKU, or category. |
| **M08** | Stock Management | `/stock` | Central inventory directory with status badges (`In Stock`, `Low Stock`, `Out of Stock`). |
| **M09** | Low Stock Alert | `/stock/low` | Automated alert table isolating products where `quantity <= min_stock`. |
| **M10** | Stock Adjustment | `/stock/adjustment` | Manual inventory corrections with audit reasons (damaged, lost, recount). |
| **M11** | Expiry Tracking | `/stock/expiry` | Product safety registry highlighting expired goods and items expiring within 30 days. |
| **M12** | Barcode / SKU Filter | `/products?q=PRD-XXXX` | Fast lookup of products by their unique code or barcode. |
| **M13** | Supplier Management | `/suppliers` | Directory of wholesale vendors with contact person, phone, and address. |
| **M14** | Purchase Entry | `/purchases/new` | Inward purchase entry form that **automatically increments** inventory stock upon submission. |
| **M15** | Purchase History | `/purchases/history`| Searchable audit log of historical supplier invoices and costs. |
| **M16** | Customer Management | `/customers` | Directory of neighborhood customers tracking total spend and credit dues. |
| **M17** | Customer Search | `/customers?q=...` | Fast lookup of customers by name or mobile phone number. |
| **M18** | Customer History | `/customers/<id>/history` | Historical ledger of all bills issued to a specific customer. |
| **M19** | Due / Payment Tracking | `/customers` | Transparent Khata tracking showing outstanding credit and partial settlements. |
| **M20** | POS Billing Screen | `/sales/new` | High-speed multi-line cart with dynamic search and stock limit validation. |
| **M21** | Auto Invoice Number | `/sales/new` | Collision-free auto-incrementing sequential invoice code (`INV-0001`, `INV-0002`). |
| **M22** | Auto Bill Calculation | Client & Server | Real-time calculation of item total, subtotal, discount, GST%, and due amount. |
| **M23** | Invoice Printing | `/sales/<id>/invoice`| Clean, professional tax invoice template with `@media print` styling. |
| **M24** | Sales History | `/sales/history` | Filterable master log of all completed, partial, due, and cancelled invoices. |
| **M25** | Sales Return / Cancel | `/sales/<id>/cancel` | Cancels an invoice and **automatically restores** sold quantities back to stock. |
| **M26** | Daily Sales Report | `/reports/daily` | Date-filtered audit of bill counts, net revenue, and items sold. |
| **M27** | Monthly Sales Report | `/reports/monthly` | Month-by-month financial summary with daily breakdown and Chart.js trend. |
| **M28** | Top Selling Products | `/reports/top-products`| Top 10 volume-generating products with horizontal bar chart visualization. |
| **M29** | Profit & Valuation | `/reports/profit` | Estimated Gross Profit (`Revenue - Cost`) and current inventory asset valuation. |
| **M30** | Settings & Demo Reset | `/settings/reset-demo`| One-click database seeder tool for viva demonstrations. |

*Table 5.3: The 30 Functional Modules Specification Index*

### 5.3 System Design Diagrams

#### 5.3.1 Use Case Diagram
```
                      APNA BAZAR SYSTEM BOUNDARY
+-----------------------------------------------------------------------+
|                                                                       |
|   (Login / Logout) <-------------------------+                        |
|                                              |                        |
|   (Point of Sale Billing) <------------------+                        |
|                                              |                        |
|   (Lookup Customer / Khata) <----------------+-------- [STAFF]        |
|                                              |                        |
|   (View Stock & Low Stock Alerts) <----------+                        |
|                                              |                        |
|   (Print Tax Invoice) <----------------------+                        |
|                                              |                        |
|   ===========================================|                        |
|                                              |                        |
|   (Manage User Accounts) <-------------------+                        |
|                                              |                        |
|   (Category & Product CRUD) <----------------+                        |
|                                              |                        |
|   (Supplier & Purchase Entry) <--------------+-------- [ADMIN]        |
|                                              |                        |
|   (Manual Stock Adjustments) <---------------+                        |
|                                              |                        |
|   (Sales Returns / Cancel Bill) <------------+                        |
|                                              |                        |
|   (View Profit & Business Reports) <---------+                        |
|                                              |                        |
|   (Configure Store Settings / Reset Demo) <--+                        |
|                                                                       |
+-----------------------------------------------------------------------+
```
*Figure 5.1: System Use Case Diagram*

#### 5.3.2 Data Flow Diagrams (DFD)

**Level 0 Context Diagram**:
```
               Credentials / Bill Requests
[Shopkeeper] ------------------------------> +-------------------------+
                                             |        Level 0          |
             <------------------------------ |       APNA BAZAR        |
                 Invoices / Reports / Alerts |   Inventory & Billing   |
                                             +-------------------------+
                                                          |
                                             Read / Write | BSON Data
                                                          v
                                             +-------------------------+
                                             |   MongoDB Atlas Cloud   |
                                             +-------------------------+
```
*Figure 5.2: Level 0 Context Data Flow Diagram*

**Level 1 Data Flow Diagram**:
```
               +--------------+
               |  Login Auth  | <=== (Users Collection)
               +--------------+
                       |
        +--------------+--------------+
        |                             |
        v                             v
+---------------+             +---------------+
|  Procurement  |             |  POS Billing  |
|  (Purchases)  |             |    (Sales)    |
+---------------+             +---------------+
        |                             |
        v (+Qty)                      v (-Qty)
+---------------------------------------------+
|         Products & Inventory Stock          |
+---------------------------------------------+
        |                             |
        v                             v
+---------------+             +---------------+
| Stock Alerts  |             | Invoices &    |
|   & Reports   |             | Khata Ledgers |
+---------------+             +---------------+
```
*Figure 5.3: Level 1 Data Flow Diagram*

#### 5.3.3 Entity Relationship Diagram (MongoDB Document Schema)

| Collection Name | Key Attributes & Types | Relations & Foreign Keys |
| :--- | :--- | :--- |
| `users` | `_id`, `username` (str), `password` (hash), `name` (str), `role` (`admin`/`staff`), `active` (bool) | Created by Admin |
| `categories` | `_id`, `name` (str), `description` (str), `created_at` (date) | Referenced in `products.category_id` |
| `products` | `_id`, `name` (str), `code` (str), `category_id` (str), `cost_price` (float), `selling_price` (float), `quantity` (int), `min_stock` (int), `unit` (str), `expiry_date` (str) | References `categories` |
| `suppliers` | `_id`, `name` (str), `contact_person` (str), `phone` (str), `email` (str), `address` (str) | Referenced in `purchases.supplier_id` |
| `purchases` | `_id`, `invoice_no` (str), `supplier_id` (str), `supplier_name` (str), `items` (array), `total_amount` (float), `date` (date) | References `suppliers` and `products` |
| `customers` | `_id`, `name` (str), `phone` (str), `email` (str), `address` (str), `total_spent` (float), `due_amount` (float) | Referenced in `sales.customer_id` |
| `sales` | `_id`, `invoice_no` (str), `customer_id` (str), `customer_name` (str), `items` (array of subdocuments), `subtotal` (float), `discount` (float), `tax_rate` (float), `tax_amount` (float), `total_amount` (float), `amount_paid` (float), `due_amount` (float), `status` (str), `created_at` (date) | References `customers` and `products` |
| `stock_movements`| `_id`, `product_id` (str), `product_name` (str), `type` (`purchase`/`sale`/`adjustment`/`return`), `quantity` (int), `reason` (str), `created_at` (date) | Audit trail linking `products` |
| `settings` | `_id`, `shop_name` (str), `owner_name` (str), `phone` (str), `address` (str), `gstin` (str), `invoice_prefix` (str) | Single store configuration document |

*Table 5.4: MongoDB Database Collections Schema Summary*

#### 5.3.4 Activity Diagram (POS Billing & Stock Cycle)
```
  (Start)
     |
     v
[Open POS Screen]
     |
     v
[Select Customer (Walk-in or Registered)]
     |
     v
[Add Product Item] ---> [Verify Available Stock Qty]
     |                               |
     | (Stock Sufficient)            | (Insufficient)
     v                               v
[Add to Cart Table]           [Show Validation Alert]
     |
     v
[Apply Optional Discount / Tax Rate]
     |
     v
[Enter Amount Paid by Customer]
     |
     v
[Compute Grand Total & Due Amount]
     |
     v
[Submit Checkout]
     |
     +---> [Save Sale Document in MongoDB]
     |
     +---> [Decrement Product Stock: quantity -= sold_qty]
     |
     +---> [Update Customer Total Spent & Due Balance]
     |
     v
[Render Printable Tax Invoice]
     |
     v
   (End)
```
*Figure 5.5: Activity Diagram: Point of Sale Checkout Flow*

#### 5.3.5 Sequence Diagram
```
User (Browser)           Flask Router (app.py)        MongoDB Atlas Database
      |                            |                                |
      |--- POST /sales/new ------->|                                |
      |    (Cart Form Data)        |                                |
      |                            |--- find_one({'_id': pid}) ---->|
      |                            |<-- return product doc ---------|
      |                            |                                |
      |                            | [Validate Stock >= Qty]        |
      |                            | [Calculate Subtotal, Tax, Due] |
      |                            |                                |
      |                            |--- insert_one(sale_doc) ------>|
      |                            |--- update_one($inc: -qty) ---->|
      |                            |--- update_one(customer due) -->|
      |                            |<-- acknowledged ---------------|
      |                            |                                |
      |<-- Redirect /sales/inv ----|                                |
      |                            |                                |
```
*Figure 5.6: Sequence Diagram: Invoice Generation and Inventory Stock Update*

---

# CHAPTER 06: IMPLEMENTATION

### 6.1 Development Environment & Setup
The development environment was configured on Windows using modern standard tools:
- **Operating System**: Windows 11 64-bit.
- **Python Version**: Python 3.14.0 / 3.11 virtual environment.
- **Project Directory Structure**:
```
d:/11-09-2026/
├── app.py                     # Main Flask Application & 30 Route Controllers
├── config.py                  # Environment Variable & Settings Loader
├── database.py                # MongoDB Atlas Driver with Resilient Mongomock Fallback
├── seed.py                    # Authentic Indian Retail Store Data Seeder
├── test_app.py                # Automated Integration Test Suite (8 Test Suites)
├── requirements.txt           # Explicit Minimal Python Dependencies
├── .env                       # Local Environment Config (Atlas URI, Secret Key)
├── .env.example               # Template for Environment Configuration
├── .gitignore                 # Excludes Virtual Environments, .env, and Pycache
├── implementation_plan.txt    # Technical Execution Plan and Reference Links
├── README.md                  # Comprehensive Setup & Viva Defense Guide
├── static/
│   ├── css/
│   │   └── style.css          # Custom Monochrome Tokens & @media print Styles
│   └── js/
│       └── app.js             # Client-side Dialogs, Mobile Menu, Lucide Icons
└── templates/                 # 18 Jinja2 Server-Rendered HTML Templates
    ├── base.html              # Master Monochrome Dashboard Shell & Navigation
    ├── login.html             # Secure Login Screen
    ├── dashboard.html         # Executive Metrics & Chart.js Visualizations
    ├── categories/            # Category List & Modal CRUD
    ├── products/              # Product Catalog, Add, Edit, and Barcode Search
    ├── stock/                 # Stock Directory, Low Stock, Adjustments, Expiry
    ├── suppliers/             # Supplier Profiles & Inward Procurement
    ├── purchases/             # Purchase Entry & Procurement History
    ├── customers/             # Customer Profiles, Ledgers, and Due Tracking
    ├── sales/                 # POS Checkout Cart, Invoices, Sales History, Returns
    ├── reports/               # Daily, Monthly, Top Products, Profit Valuation
    ├── users/                 # Admin User Management Interface
    └── settings/              # Store Profile & One-Click Demo Reset Tool
```

### 6.2 Frontend Implementation
The frontend was designed with an emphasis on clarity and performance:
- **Monochrome Design System**: Avoiding loud neon colors or complex multi-color themes, the user interface adheres to a curated black-and-white SaaS aesthetic:
  - Page Background: `#f9fafb` (soft off-white)
  - Card Surfaces: `#ffffff` (pure white) with subtle 1px `#e5e7eb` borders
  - Primary Action Buttons: `#111827` (deep near-black) with crisp white text
  - Secondary Buttons: `#ffffff` with border `#d1d5db` and hover state `#f3f4f6`
- **Responsive Layout**: A persistent desktop sidebar (collapsible on mobile via a slide-out drawer) categorizes all 30 modules into logical operational groups:
  1. Overview (Dashboard)
  2. Inventory (Products, Categories, Stock, Low Stock, Adjustments, Expiry)
  3. Procurement (Suppliers, Purchase Entry, Purchase History)
  4. Point of Sale (POS Billing, Sales History, Customer Ledgers)
  5. Analytics (Daily, Monthly, Top Selling, Profit & Valuation)
  6. System (User Accounts, Shop Settings)
- **Print Optimization**: A dedicated print stylesheet (`@media print`) ensures invoices print cleanly:
```css
@media print {
    body * { visibility: hidden; }
    #printable-invoice, #printable-invoice * { visibility: visible; }
    #printable-invoice {
        position: absolute;
        left: 0;
        top: 0;
        width: 100%;
        margin: 0;
        padding: 20px;
        background: white;
    }
    .no-print { display: none !important; }
}
```

### 6.3 Backend Implementation
The backend is powered by Python Flask (`app.py`), structured cleanly without unnecessary abstraction layers:
- **Authentication & Security Decorators**:
```python
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page.', 'warning')
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        if session.get('user_role') != 'admin':
            flash('Access restricted to administrators.', 'danger')
            return redirect(url_for('dashboard'))
        return f(*args, **kwargs)
    return decorated_function
```

- **Sequential Invoice Number Generator**:
```python
def get_next_invoice_number():
    db = get_db()
    last_sale = db.sales.find_one(sort=[('_id', -1)])
    if not last_sale or 'invoice_no' not in last_sale:
        return "INV-0001"
    try:
        last_num = int(last_sale['invoice_no'].split('-')[1])
        return f"INV-{last_num + 1:04d}"
    except (IndexError, ValueError):
        count = db.sales.count_documents({})
        return f"INV-{count + 1:04d}"
```

### 6.4 Database Implementation & Resilience
To address common college lab challenges—such as restricted firewall ports or sudden Wi-Fi disconnection during viva presentations—`database.py` incorporates an automatic fallback mechanism:
```python
def init_db():
    global _db_client, _db_instance
    mongo_uri = Config.MONGO_URI
    
    # 1. Attempt connection to user's MongoDB Atlas cluster
    if mongo_uri:
        try:
            client = MongoClient(
                mongo_uri,
                serverSelectionTimeoutMS=2000,
                tlsCAFile=certifi.where()
            )
            client.admin.command('ping')
            _db_client = client
            _db_instance = client.get_default_database()
            return _db_instance
        except Exception as e:
            logger.warning(f"MongoDB Atlas unreachable. Activating Mongomock fallback: {e}")
            
    # 2. Transparent fallback to mongomock in-memory database
    import mongomock
    _db_client = mongomock.MongoClient()
    _db_instance = _db_client['inventory_billing_db']
    return _db_instance
```

### 6.5 Authentic Indian Retail Seeder (`seed.py`)
The system includes an authentic retail seeder populated with products commonly found in neighborhood Indian provision stores:
- **Store Name**: APNA BAZAR
- **Owner**: Akshay Khapare
- **Categories**: Grocery & Staples, Snacks & Confectionery, Beverages & Tea, Personal Care & Hygiene, Household Cleaners, Stationery.
- **Stock Items**: Kolam Rice (₹60/kg), Chakki Fresh Wheat Flour (₹45/kg), Pure Refined Sugar (₹42/kg), Tata Tea Gold (₹140/250g), Parle-G Biscuits (₹10/pkt), Amul Taaza Milk (₹27/500ml), Dettol Bathing Soap (₹38/bar), Sunflower Cooking Oil (₹145/L), Tata Iodized Salt (₹25/kg), Classmate Notebooks (₹60/unit).
- **Default User Accounts**:
  - Administrator: `admin` / `admin123`
  - Staff Cashier: `suresh` / `staff123`

---

# CHAPTER 07: TESTING AND RESULTS

### 7.1 Testing Methodology
The testing phase applied a multi-tiered quality assurance strategy:
1. **Automated Unit & Integration Testing**: Validating route security, CRUD handlers, inventory stock increments/decrements, and arithmetic billing formulas via Python's built-in `unittest` framework.
2. **Database Invariant Verification**: Ensuring mathematical assertions hold true across multi-step transactions.
3. **Cross-Browser & Responsive Validation**: Inspecting layout fidelity across Chrome, Edge, and mobile viewports.
4. **User Acceptance Testing (UAT)**: Simulating real-world retail workflows (e.g., adding 5 items, applying 5% discount, paying ₹500, issuing ₹60 credit balance).

### 7.2 Automated Integration & Unit Test Cases (TC01 - TC08)

| Test ID | Test Suite Name | Execution Command | Objective & Verification Criteria | Status |
| :---: | :--- | :--- | :--- | :---: |
| **TC01** | Authentication & Role Protection | `test_app.py::test_01` | Unauthorized requests to `/dashboard` must redirect to `/login`. Admin routes blocked for staff role. | **PASSED** |
| **TC02** | Live MongoDB Connectivity | `test_app.py::test_02` | Dashboard successfully loads dynamic documents from MongoDB Atlas. | **PASSED** |
| **TC03** | Category Management CRUD | `test_app.py::test_03` | Add new category, verify presence, edit name, delete, and verify removal. | **PASSED** |
| **TC04** | Product CRUD & Search | `test_app.py::test_04` | Create product with SKU `PRD-TEST`, search by code and category, update prices. | **PASSED** |
| **TC05** | Supplier & Customer CRUD | `test_app.py::test_05` | Create supplier, create customer, query customer balance, verify phone indexing. | **PASSED** |
| **TC06** | Complete Stock Cycle Test | `test_app.py::test_06` | Initial: 10 units -> Purchase 5 (+5 = 15) -> Sell 3 (-3 = 12) -> Cancel Sale (+3 = 15). | **PASSED** |
| **TC07** | POS Calculation & Due Math | `test_app.py::test_07` | 2x₹100 + 3x₹50 = Subtotal ₹350. Disc ₹20 = ₹330. Tax ₹0 = ₹330. Paid ₹300 = Due ₹30. | **PASSED** |
| **TC08** | Analytical Reports Generation | `test_app.py::test_08` | Daily, Monthly, Top Products, and Profit Valuation endpoints return HTTP 200 with data. | **PASSED** |

*Table 7.1: Test Suite Case Matrix (TC01 to TC08)*

#### Deep-Dive: Test Case 06 (Stock Lifecycle Invariance)
```python
# Verifying strict inventory balance: 10 -> +5 -> -3 -> +3 = 15
initial_qty = 10
purchase_qty = 5
sell_qty = 3

# Step 1: Create initial product with 10 units
prod_id = db.products.insert_one({'name': 'Test Item', 'quantity': 10, ...}).inserted_id

# Step 2: Record Purchase of 5 units
client.post('/purchases/new', data={'product_id': prod_id, 'quantity': 5, ...})
assert db.products.find_one({'_id': prod_id})['quantity'] == 15   # PASSED [OK]

# Step 3: Complete POS Sale of 3 units
client.post('/sales/new', data={'product_ids[]': [prod_id], 'quantities[]': [3], ...})
assert db.products.find_one({'_id': prod_id})['quantity'] == 12   # PASSED [OK]

# Step 4: Cancel the Sale
client.post(f'/sales/{sale_id}/cancel')
assert db.products.find_one({'_id': prod_id})['quantity'] == 15   # PASSED [OK]
```

### 7.3 Test Execution Results
All 8 test suites were executed against the application:
```
================================================================================
                          TEST EXECUTION SUMMARY REPORT
================================================================================
Test 1: Authentication & Role-Based Access Control ............. [PASSED]
Test 2: MongoDB Live Connectivity & Dashboard Data ............. [PASSED]
Test 3: Category Management CRUD Operations .................... [PASSED]
Test 4: Product Catalog CRUD, Barcode & Category Filters ....... [PASSED]
Test 5: Supplier & Customer Directory Management ............... [PASSED]
Test 6: Stock Lifecycle: Inward -> Sale -> Cancellation ........ [PASSED]
Test 7: POS Calculation Math, Tax, Discount & Due Ledger ....... [PASSED]
Test 8: Daily, Monthly, Top Selling & Profit Reports ........... [PASSED]
--------------------------------------------------------------------------------
Ran 8 tests in 10.748s

STATUS: ALL TESTS PASSED (100% SUCCESS RATE)
================================================================================
```

### 7.4 System Verification Screenshots & Walkthrough

1. **Secure Admin Login (`/login`)**:
   - Clean, centered login card with demo credential guidance (`admin` / `admin123`).
   - Handles invalid credentials with animated, auto-dismissing flash alerts.

2. **Executive Monochrome Dashboard (`/dashboard`)**:
   - Displays real-time summary cards: Today's Total Sales (₹), Monthly Revenue (₹), Low Stock Items Count, and Total Outstanding Khata Dues.
   - Embeds an interactive 7-Day Chart.js daily revenue line chart.

3. **Product Catalog & Stock Management (`/products` & `/stock`)**:
   - Tabular directory displaying product names, SKUs, category badges, cost price, selling price, current stock, and expiry indicators.
   - Quick search input filtering rows in real-time.

4. **Point-of-Sale Billing Terminal (`/sales/new`)**:
   - Customer search dropdown supporting registered and walk-in patrons.
   - Dynamic product line addition with live quantity spinners.
   - Real-time client-side calculation of Item Total, Subtotal, Discount, GST, Grand Total, and remaining Due balance.
   - Live stock validation preventing cashiers from billing more units than available on shelves.

5. **Printable Tax Invoice (`/sales/<id>/invoice`)**:
   - Formatted retail receipt featuring the store header ("APNA BAZAR"), owner ("Akshay Khapare"), GSTIN, sequential invoice number, itemized table, and total summary.
   - Browser print button invoking `@media print` CSS for receipts.

6. **Profit & Inventory Valuation Report (`/reports/profit`)**:
   - Computes net sales, total purchase cost, and estimated gross profit margin.
   - Calculates total retail asset value of all products currently in stock.

---

# CHAPTER 08: CONCLUSION

### 8.1 Project Summary
**APNA BAZAR** was developed to address the everyday operational challenges faced by neighborhood retail shops. Over the course of this Community Engagement Project (CEP), a complete inventory management and billing system was designed, implemented, tested, and documented. 

By utilizing Python Flask, MongoDB Atlas, and a minimalist monochrome frontend, the project delivers a fast, stable, and practical solution tailored specifically for local shopkeepers.

### 8.2 Key Achievements
1. **Built Exactly 30 Functional Modules**: Implemented all core retail requirements ranging from user access control and product cataloging to POS checkout, khata ledgers, and profit reporting.
2. **Enforced Inventory Integrity**: Built automated stock updates where stock increases upon purchase, decreases upon sale, and is restored upon cancellation.
3. **Resilient Architecture**: Implemented cloud storage on MongoDB Atlas with an automated local in-memory fallback (`mongomock`) that prevents downtime.
4. **Zero Billing Math Errors**: Verified via automated integration test suites that all subtotals, taxes, discounts, and due balances calculate accurately.
5. **Modern Minimalist Aesthetics**: Created a clean, distraction-free black-and-white user interface that provides clear readability on any display.

### 8.3 Benefits to Local Retailers & Community
- **Time Savings**: Reduces billing time from minutes to seconds per customer, shortening queues during peak rush hours.
- **Credit (*Khata*) Recovery**: Clearly tracks credit dues per customer, reducing uncollected debt.
- **Minimized Wastage**: Low stock alerts prevent missed sales, while the 30-day expiry tracker prevents selling expired items.
- **Financial Clarity**: Provides shopkeepers with instant visibility into gross profit margins and fast-moving products.

### 8.4 Limitations of the Current System
- **Single Store Scope**: Designed for single-location retail stores; does not support multi-branch inter-store warehouse transfers.
- **Manual Barcode Entry**: Supports barcode/SKU searching via standard USB barcode scanners acting as keyboard inputs, but lacks camera-based scanning inside the browser.
- **Browser-Based Printing**: Relies on browser-native print dialogs rather than direct hardware ESC/POS raw socket communication with thermal receipt printers.

---

# CHAPTER 09: FUTURE ENHANCEMENTS

### 9.1 Hardware Barcode Scanner & Thermal ESC/POS Integration
Future versions can integrate direct WebUSB or WebSerial API communication, allowing the web app to connect directly to 58mm/80mm thermal receipt printers without showing the intermediate operating system print dialog.

### 9.2 Automated WhatsApp & SMS Khata Reminders
Integration with communication APIs (such as Twilio or WhatsApp Business Cloud API) would enable the system to automatically send digital invoice PDFs and polite payment reminders for overdue balances.

### 9.3 Dynamic UPI QR Code on Invoices
Implementing dynamic UPI QR code generation on the checkout screen and printed invoices would allow customers to scan and pay the exact invoice amount directly using PhonePe, Google Pay, or Paytm.

### 9.4 Mobile Progressive Web App (PWA)
Converting the frontend into a Progressive Web App (PWA) with offline Service Workers would allow shopkeepers to install APNA BAZAR on Android or iOS mobile devices with a home-screen icon and native offline caching.

### 9.5 Multi-Store Centralized Cloud Synchronization
Extending the MongoDB document schema to support a `store_id` field across all collections would allow multi-branch retail owners to oversee inventory and sales across multiple locations from a unified executive portal.

---

# CHAPTER 10: REFERENCES

### 10.1 Books and Research Papers
1. **Grinberg, Miguel** (2018). *Flask Web Development: Developing Web Applications with Python*. O'Reilly Media, 2nd Edition.
2. **Chodorow, Kristina** (2013). *MongoDB: The Definitive Guide: Powerful and Scalable Data Storage*. O'Reilly Media.
3. **Sommerville, Ian** (2015). *Software Engineering*. Pearson Education, 10th Edition.
4. **Pressman, Roger S. & Maxim, Bruce R.** (2020). *Software Engineering: A Practitioner's Approach*. McGraw-Hill Education, 9th Edition.
5. **Martin, Robert C.** (2017). *Clean Architecture: A Craftsman's Guide to Software Structure and Design*. Prentice Hall.

### 10.2 Official Documentation & API References
1. **Python Software Foundation**: *Python 3.11 & 3.14 Documentation*, https://docs.python.org/3/
2. **Pallets Projects**: *Flask Documentation (v3.1.0)*, https://flask.palletsprojects.com/en/stable/
3. **Werkzeug Security**: *Werkzeug Password Hashing Module*, https://werkzeug.palletsprojects.com/en/stable/utils/#module-werkzeug.security
4. **MongoDB Inc.**: *PyMongo Documentation (v4.10)*, https://pymongo.readthedocs.io/en/stable/
5. **MongoDB Atlas**: *MongoDB Cloud Database Architecture Guide*, https://www.mongodb.com/docs/atlas/
6. **Tailwind CSS**: *Tailwind CSS Utility Framework Documentation*, https://tailwindcss.com/docs/installation/play-cdn
7. **Chart.js**: *Chart.js Open Source HTML5 Canvas Charting*, https://www.chartjs.org/docs/latest/
8. **Lucide Icons**: *Lucide Open-Source Vector Iconography*, https://lucide.dev/guide/packages/lucide

### 10.3 Websites and Online Resources
1. **Mozilla Developer Network (MDN)**: *HTML5 Semantic Elements & CSS Print Media Styling*, https://developer.mozilla.org/
2. **W3C Standards**: *Web Content Accessibility Guidelines (WCAG) 2.1*, https://www.w3.org/WAI/standards-guidelines/wcag/
3. **Render Cloud Platform**: *Deploying Flask Applications on Render PaaS*, https://render.com/docs/deploy-flask
4. **GitHub Documentation**: *Git Version Control and Repository Management*, https://docs.github.com/
