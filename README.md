# 🧩 MerchPro ERP
### (Omnichannel ERP for Merchandise, Maintenance & Service Companies)

A modern **Django-based ERP system** designed for small to medium **merchandise and maintenance** businesses.
It unifies **inventory, operations, CRM, accounting, and online store management** under one scalable backend — with JWT authentication and modular design.

---

## 🚀 Core Features

### **Phase 1 (MVP)**
- 🏪 **Inventory Management**
  Manage stock, categories, product conditions (new/used), and multi-location tracking.

- 🔧 **Operations Module (Sales, Purchases, Services, Maintenance)**
  - Record **purchases** from vendors, suppliers, or corporate clearance.
  - Register **sales** to customers (in-store or corporate).
  - Manage **services** like software installation or system setup (even if not purchased internally).
  - Track **maintenance** tasks — diagnostics, repairs, or support after sale.

- 👥 **CRM (Customer Relationship Management)**
  Manage customers, vendors, service history, and feedback.

- 🧾 **Accounting**
  Basic transaction tracking for sales, purchases, and service invoices.

- 🛒 **E-Commerce (Online Store)**
  Optional module for managing online product listings and web orders, connected to the same inventory.

- 📊 **Dashboard**
  Unified admin dashboard summarizing key metrics across operations, inventory, and accounting.

---

### **Phase 2 (Expansion)**
- 📦 **Procurement** – Supplier management, purchase orders, and delivery tracking.
- 👔 **HR & Roles** – Employee records, roles, payroll, and permissions.
- 🔔 **Notifications** – Email/SMS/app alerts for workflow updates.
- 📈 **Analytics** – Reports, KPIs, and performance tracking.
- 📁 **Documents** – Upload invoices, receipts, and PDFs.
- 🔗 **Integration Layer** – API gateways and payment integrations.

---

## 🧱 Project Structure

```bash
Omnichannel-ERP/
│
├── manage.py
├── README.md
├── LICENSE
│
├── core/               # Base model, utilities, and shared mixins
├── users/              # Custom JWT user model (extends AbstractUser + Base)
├── inventory/          # Inventory, products, warehouses, stock management
├── operations/         # Sales, purchases, maintenance, and service orders
├── ecommerce/          # Online store module (optional)
├── accounting/         # Basic accounting and transactions
├── crm/                # Customers, vendors, relations
├── dashboard/          # Overview and analytics dashboard
├── documents/          # Document uploads (contracts, invoices, etc.)
│
├── business_core/      # Shared business logic and data operations
├── apps.sh             # App management script
├── psqlcmd.md          # PostgreSQL command references
├── test.py / test.sql  # Development test files
└── requirements.txt
