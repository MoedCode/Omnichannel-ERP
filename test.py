
#!/usr/bin/env python3
'''
Advanced Python Desktop POS / Sales & Inventory System (single-file)

Features:
- Tkinter GUI (single-file, zero external deps)
- SQLite backend (stored in "pos.db" next to the script)
- Product management (add/edit products)
- Purchases: add stock, apply unit cost (with currency rate if needed)
- Weighted average inventory costing (updated on purchases)
- Sales: reduce stock, compute COGS using current weighted average
- Other revenues & expenses (maintenance, services, dues...)
- Reports: Inventory, Sales, P&L over a date range
- CSV export for reports
- Designed for fast-changing EGP: each transaction may include a conversion rate
  so you can record amounts in foreign currency and convert to EGP for cost/profit.
- Single-file: run `python advanced_pos.py` to start

Note: This is a functional MVP meant to be extended. It's deliberately dependency-free
to ease running on most Python installs (3.8+ recommended).

Author: ChatGPT (GPT-5 Thinking mini)
Date: 2025
"""
'''
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import sqlite3
from datetime import datetime
import csv
import os

DB_FILE = os.path.join(os.path.dirname(__file__), "pos.db")

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY,
        sku TEXT UNIQUE,
        name TEXT,
        qty REAL DEFAULT 0,
        avg_cost REAL DEFAULT 0 -- stored in EGP
    )""")
    cur.execute("""
    CREATE TABLE IF NOT EXISTS purchases (
        id INTEGER PRIMARY KEY,
        product_id INTEGER,
        date TEXT,
        qty REAL,
        unit_cost REAL, -- as entered (in its currency)
        currency TEXT,
        rate_to_egp REAL, -- multiply unit_cost * rate_to_egp => cost in EGP
        cost_egp REAL, -- unit cost in EGP (unit_cost * rate_to_egp)
        total_egp REAL,
        notes TEXT,
        FOREIGN KEY(product_id) REFERENCES products(id)
    )""")
    cur.execute("""
    CREATE TABLE IF NOT EXISTS sales (
        id INTEGER PRIMARY KEY,
        product_id INTEGER,
        date TEXT,
        qty REAL,
        unit_price REAL, -- selling price per unit (in EGP)
        total_egp REAL,
        cogs_egp REAL, -- cost of goods sold in EGP (qty * avg_cost_at_sale)
        notes TEXT,
        FOREIGN KEY(product_id) REFERENCES products(id)
    )""")
    cur.execute("""
    CREATE TABLE IF NOT EXISTS other_entries (
        id INTEGER PRIMARY KEY,
        date TEXT,
        type TEXT, -- 'revenue' or 'expense'
        category TEXT, -- maintenance, service, dues, etc.
        amount REAL, -- in EGP
        notes TEXT
    )""")
    conn.commit()
    conn.close()

def add_product(sku, name):
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    try:
        cur.execute("INSERT INTO products (sku, name) VALUES (?, ?)", (sku, name))
        conn.commit()
    except sqlite3.IntegrityError:
        raise
    finally:
        conn.close()

def get_products():
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("SELECT id, sku, name, qty, avg_cost FROM products ORDER BY name")
    rows = cur.fetchall()
    conn.close()
    return rows

def get_product_by_id(pid):
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("SELECT id, sku, name, qty, avg_cost FROM products WHERE id=?", (pid,))
    r = cur.fetchone()
    conn.close()
    return r

def record_purchase(product_id, date, qty, unit_cost, currency, rate_to_egp, notes=""):
    # Convert to EGP if rate provided; if no rate use 1.0
    rate = float(rate_to_egp) if rate_to_egp else 1.0
    cost_egp = float(unit_cost) * rate
    total = cost_egp * float(qty)
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()

    # get current qty and avg_cost
    cur.execute("SELECT qty, avg_cost FROM products WHERE id=?", (product_id,))
    row = cur.fetchone()
    if row is None:
        conn.close()
        raise Exception("Product not found")
    old_qty, old_avg = float(row[0]), float(row[1] or 0.0)

    new_qty = old_qty + float(qty)
    if new_qty <= 0:
        new_avg = 0.0
    else:
        # Weighted average update
        new_avg = ((old_qty * old_avg) + (float(qty) * cost_egp)) / new_qty

    # insert purchase record
    cur.execute('''INSERT INTO purchases
        (product_id, date, qty, unit_cost, currency, rate_to_egp, cost_egp, total_egp, notes)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''',
        (product_id, date, qty, unit_cost, currency, rate, cost_egp, total, notes))

    # update product inventory and avg_cost
    cur.execute("UPDATE products SET qty=?, avg_cost=? WHERE id=?",
                (new_qty, new_avg, product_id))

    conn.commit()
    conn.close()

def record_sale(product_id, date, qty, unit_price, notes=""):
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("SELECT qty, avg_cost FROM products WHERE id=?", (product_id,))
    row = cur.fetchone()
    if row is None:
        conn.close()
        raise Exception("Product not found")
    old_qty, avg_cost = float(row[0]), float(row[1] or 0.0)
    if float(qty) > old_qty + 1e-9:
        conn.close()
        raise Exception("Not enough stock to sell (current stock: {})".format(old_qty))
    new_qty = old_qty - float(qty)
    cogs = avg_cost * float(qty)
    total = float(unit_price) * float(qty)

    # insert sale record
    cur.execute('''INSERT INTO sales
        (product_id, date, qty, unit_price, total_egp, cogs_egp, notes)
        VALUES (?, ?, ?, ?, ?, ?, ?)''',
        (product_id, date, qty, unit_price, total, cogs, notes))

    # update product qty only (avg_cost stays same for weighted average until next purchase)
    cur.execute("UPDATE products SET qty=? WHERE id=?", (new_qty, product_id))

    conn.commit()
    conn.close()

def record_other(date, type_, category, amount, notes=""):
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute('''INSERT INTO other_entries (date, type, category, amount, notes)
                   VALUES (?, ?, ?, ?, ?)''', (date, type_, category, amount, notes))
    conn.commit()
    conn.close()

def query_inventory():
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("SELECT id, sku, name, qty, avg_cost, qty*avg_cost as val FROM products")
    rows = cur.fetchall()
    conn.close()
    return rows

def query_sales(from_date=None, to_date=None):
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    q = "SELECT s.id, p.sku, p.name, s.date, s.qty, s.unit_price, s.total_egp, s.cogs_egp, s.notes FROM sales s JOIN products p ON s.product_id=p.id"
    params = []
    if from_date and to_date:
        q += " WHERE date BETWEEN ? AND ?"
        params = [from_date, to_date]
    q += " ORDER BY date DESC"
    cur.execute(q, params)
    rows = cur.fetchall()
    conn.close()
    return rows

def query_others(from_date=None, to_date=None):
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    q = "SELECT id, date, type, category, amount, notes FROM other_entries"
    params = []
    if from_date and to_date:
        q += " WHERE date BETWEEN ? AND ?"
        params = [from_date, to_date]
    q += " ORDER BY date DESC"
    cur.execute(q, params)
    rows = cur.fetchall()
    conn.close()
    return rows

def compute_pnl(from_date=None, to_date=None):
    # compute revenue (sales total), cogs, other revenues, other expenses
    sales = query_sales(from_date, to_date)
    others = query_others(from_date, to_date)
    revenue = sum(r[6] for r in sales)
    cogs = sum(r[7] for r in sales)
    other_revenue = sum(r[4] for r in others if r[2]=='revenue')
    other_expense = sum(r[4] for r in others if r[2]=='expense')
    gross_profit = revenue - cogs
    net_profit = gross_profit + other_revenue - other_expense
    return {
        "revenue": revenue,
        "cogs": cogs,
        "other_revenue": other_revenue,
        "other_expense": other_expense,
        "gross_profit": gross_profit,
        "net_profit": net_profit
    }

# ----------------- UI -----------------

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Advanced Sales & Inventory - Weighted Average (EGP-aware)")
        self.geometry("1000x650")
        self.create_widgets()

    def create_widgets(self):
        nb = ttk.Notebook(self)
        nb.pack(fill=tk.BOTH, expand=True)

        self.tab_products = ttk.Frame(nb)
        self.tab_purchase = ttk.Frame(nb)
        self.tab_sales = ttk.Frame(nb)
        self.tab_other = ttk.Frame(nb)
        self.tab_reports = ttk.Frame(nb)

        nb.add(self.tab_products, text="Products")
        nb.add(self.tab_purchase, text="Purchases")
        nb.add(self.tab_sales, text="Sales")
        nb.add(self.tab_other, text="Other Revenue/Expense")
        nb.add(self.tab_reports, text="Reports & Export")

        self.build_products_tab()
        self.build_purchase_tab()
        self.build_sales_tab()
        self.build_other_tab()
        self.build_reports_tab()

    def build_products_tab(self):
        frm = self.tab_products
        left = ttk.Frame(frm, padding=10)
        left.pack(side=tk.LEFT, fill=tk.Y)
        ttk.Label(left, text="Add Product (SKU & Name)").pack(anchor=tk.W)
        self.e_sku = ttk.Entry(left)
        self.e_sku.pack(fill=tk.X)
        self.e_name = ttk.Entry(left)
        self.e_name.pack(fill=tk.X, pady=(5,5))
        ttk.Button(left, text="Add Product", command=self.on_add_product).pack(pady=(5,10))
        ttk.Button(left, text="Refresh List", command=self.refresh_products).pack()

        right = ttk.Frame(frm, padding=10)
        right.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        cols = ("id","sku","name","qty","avg_cost","value")
        self.tv_products = ttk.Treeview(right, columns=cols, show="headings")
        for c in cols:
            self.tv_products.heading(c, text=c.title())
        self.tv_products.pack(fill=tk.BOTH, expand=True)
        self.refresh_products()

    def on_add_product(self):
        sku = self.e_sku.get().strip()
        name = self.e_name.get().strip()
        if not sku or not name:
            messagebox.showwarning("Missing", "Provide SKU and name")
            return
        try:
            add_product(sku, name)
            messagebox.showinfo("Added", f"Product {name} added.")
            self.e_sku.delete(0, tk.END); self.e_name.delete(0, tk.END)
            self.refresh_products()
            self.refresh_product_options()
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "SKU already exists. Use another SKU.")

    def refresh_products(self):
        for i in self.tv_products.get_children():
            self.tv_products.delete(i)
        for r in query_inventory():
            self.tv_products.insert("", tk.END, values=(r[0], r[1], r[2], round(r[3],3), round(r[4],3), round(r[5] or 0.0,2)))

    def build_purchase_tab(self):
        frm = self.tab_purchase
        top = ttk.Frame(frm, padding=10)
        top.pack(fill=tk.X)
        ttk.Label(top, text="Purchase - add stock and update weighted average cost").grid(row=0,column=0,columnspan=4,sticky=tk.W)
        ttk.Label(top, text="Product:").grid(row=1,column=0,sticky=tk.W)
        self.cmb_purchase_product = ttk.Combobox(top, values=[], state="readonly")
        self.cmb_purchase_product.grid(row=1,column=1,sticky=tk.W)
        ttk.Label(top, text="Qty:").grid(row=1,column=2,sticky=tk.W)
        self.e_purchase_qty = ttk.Entry(top, width=10); self.e_purchase_qty.grid(row=1,column=3,sticky=tk.W)
        ttk.Label(top, text="Unit Cost:").grid(row=2,column=0,sticky=tk.W)
        self.e_purchase_unit = ttk.Entry(top, width=12); self.e_purchase_unit.grid(row=2,column=1,sticky=tk.W)
        ttk.Label(top, text="Currency:").grid(row=2,column=2,sticky=tk.W)
        self.e_purchase_currency = ttk.Entry(top, width=10); self.e_purchase_currency.insert(0, "EGP"); self.e_purchase_currency.grid(row=2,column=3,sticky=tk.W)
        ttk.Label(top, text="Rate to EGP:").grid(row=3,column=0,sticky=tk.W)
        self.e_purchase_rate = ttk.Entry(top, width=12); self.e_purchase_rate.insert(0,"1.0"); self.e_purchase_rate.grid(row=3,column=1,sticky=tk.W)
        ttk.Label(top, text="Date (YYYY-MM-DD):").grid(row=3,column=2,sticky=tk.W)
        self.e_purchase_date = ttk.Entry(top, width=12); self.e_purchase_date.insert(0, datetime.today().strftime("%Y-%m-%d")); self.e_purchase_date.grid(row=3,column=3,sticky=tk.W)
        ttk.Label(top, text="Notes:").grid(row=4,column=0,sticky=tk.W)
        self.e_purchase_notes = ttk.Entry(top, width=60); self.e_purchase_notes.grid(row=4,column=1,columnspan=3,sticky=tk.W)
        ttk.Button(top, text="Record Purchase", command=self.on_record_purchase).grid(row=5,column=0,columnspan=2,pady=6)
        ttk.Button(top, text="Refresh Products", command=self.refresh_product_options).grid(row=5,column=2,columnspan=2)

        self.refresh_product_options()
        # recent purchases
        bottom = ttk.Frame(frm, padding=10)
        bottom.pack(fill=tk.BOTH, expand=True)
        cols = ("id","sku","name","date","qty","unit_cost","currency","rate","cost_egp","total","notes")
        self.tv_purchases = ttk.Treeview(bottom, columns=cols, show="headings")
        for c in cols:
            self.tv_purchases.heading(c, text=c.title())
        self.tv_purchases.pack(fill=tk.BOTH, expand=True)
        self.refresh_purchases()

    def refresh_product_options(self):
        prods = get_products()
        choices = [f"{p[0]} - {p[2]} ({p[1]})" for p in prods]
        self.cmb_purchase_product['values'] = choices
        self.cmb_sale_product = getattr(self, "cmb_sale_product", None)
        if self.cmb_sale_product:
            self.cmb_sale_product['values'] = choices

    def on_record_purchase(self):
        sel = self.cmb_purchase_product.get().strip()
        if not sel:
            messagebox.showwarning("Select", "Select a product first")
            return
        pid = int(sel.split(" - ")[0])
        try:
            qty = float(self.e_purchase_qty.get())
            unit = float(self.e_purchase_unit.get())
            rate = float(self.e_purchase_rate.get() or 1.0)
        except Exception:
            messagebox.showerror("Bad input", "Qty, Unit Cost, and Rate must be numeric")
            return
        date = self.e_purchase_date.get().strip() or datetime.today().strftime("%Y-%m-%d")
        try:
            record_purchase(pid, date, qty, unit, self.e_purchase_currency.get().strip() or "EGP", rate, self.e_purchase_notes.get().strip())
            messagebox.showinfo("OK", "Purchase recorded and inventory updated (weighted avg adjusted)." )
            self.refresh_products(); self.refresh_purchases(); self.refresh_product_options()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def refresh_purchases(self):
        for i in self.tv_purchases.get_children():
            self.tv_purchases.delete(i)
        conn = sqlite3.connect(DB_FILE)
        cur = conn.cursor()
        cur.execute("SELECT p.id, pr.sku, pr.name, p.date, p.qty, p.unit_cost, p.currency, p.rate_to_egp, p.cost_egp, p.total_egp, p.notes FROM purchases p JOIN products pr ON p.product_id=pr.id ORDER BY date DESC")
        for r in cur.fetchall():
            self.tv_purchases.insert("", tk.END, values=(r[0], r[1], r[2], r[3], round(r[4],3), round(r[5],4), r[6], round(r[7],4), round(r[8],4), round(r[9],4), r[10]))
        conn.close()

    def build_sales_tab(self):
        frm = self.tab_sales
        top = ttk.Frame(frm, padding=10)
        top.pack(fill=tk.X)
        ttk.Label(top, text="Record Sale").grid(row=0,column=0,columnspan=4,sticky=tk.W)
        ttk.Label(top, text="Product:").grid(row=1,column=0,sticky=tk.W)
        self.cmb_sale_product = ttk.Combobox(top, values=[], state="readonly")
        self.cmb_sale_product.grid(row=1,column=1,sticky=tk.W)
        ttk.Label(top, text="Qty:").grid(row=1,column=2,sticky=tk.W); self.e_sale_qty = ttk.Entry(top, width=10); self.e_sale_qty.grid(row=1,column=3,sticky=tk.W)
        ttk.Label(top, text="Unit Price (EGP):").grid(row=2,column=0,sticky=tk.W); self.e_sale_unit = ttk.Entry(top, width=12); self.e_sale_unit.grid(row=2,column=1,sticky=tk.W)
        ttk.Label(top, text="Date (YYYY-MM-DD):").grid(row=2,column=2,sticky=tk.W); self.e_sale_date = ttk.Entry(top, width=12); self.e_sale_date.insert(0, datetime.today().strftime("%Y-%m-%d")); self.e_sale_date.grid(row=2,column=3,sticky=tk.W)
        ttk.Label(top, text="Notes:").grid(row=3,column=0,sticky=tk.W)
        self.e_sale_notes = ttk.Entry(top, width=60); self.e_sale_notes.grid(row=3,column=1,columnspan=3,sticky=tk.W)
        ttk.Button(top, text="Record Sale", command=self.on_record_sale).grid(row=4,column=0,columnspan=2,pady=6)
        ttk.Button(top, text="Refresh Products", command=self.refresh_product_options).grid(row=4,column=2,columnspan=2)

        bottom = ttk.Frame(frm, padding=10)
        bottom.pack(fill=tk.BOTH, expand=True)
        cols = ("id","sku","name","date","qty","unit_price","total","cogs","notes")
        self.tv_sales = ttk.Treeview(bottom, columns=cols, show="headings")
        for c in cols:
            self.tv_sales.heading(c, text=c.title())
        self.tv_sales.pack(fill=tk.BOTH, expand=True)
        self.refresh_sales()

    def on_record_sale(self):
        sel = self.cmb_sale_product.get().strip()
        if not sel:
            messagebox.showwarning("Select", "Select a product first")
            return
        pid = int(sel.split(" - ")[0])
        try:
            qty = float(self.e_sale_qty.get())
            unit = float(self.e_sale_unit.get())
        except Exception:
            messagebox.showerror("Bad input", "Qty and Unit Price must be numeric")
            return
        date = self.e_sale_date.get().strip() or datetime.today().strftime("%Y-%m-%d")
        try:
            record_sale(pid, date, qty, unit, self.e_sale_notes.get().strip())
            messagebox.showinfo("OK", "Sale recorded. COGS computed using current weighted average cost.")
            self.refresh_products(); self.refresh_sales()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def refresh_sales(self):
        for i in self.tv_sales.get_children():
            self.tv_sales.delete(i)
        for r in query_sales():
            self.tv_sales.insert("", tk.END, values=(r[0], r[1], r[2], r[3], round(r[4],3), round(r[5],3), round(r[6],3), round(r[7],3), r[8]))

    def build_other_tab(self):
        frm = self.tab_other
        top = ttk.Frame(frm, padding=10)
        top.pack(fill=tk.X)
        ttk.Label(top, text="Add Other Revenue / Expense").grid(row=0,column=0,columnspan=4,sticky=tk.W)
        ttk.Label(top, text="Type:").grid(row=1,column=0,sticky=tk.W)
        self.cmb_other_type = ttk.Combobox(top, values=["revenue","expense"], state="readonly"); self.cmb_other_type.current(0); self.cmb_other_type.grid(row=1,column=1,sticky=tk.W)
        ttk.Label(top, text="Category:").grid(row=1,column=2,sticky=tk.W); self.e_other_cat = ttk.Entry(top); self.e_other_cat.grid(row=1,column=3,sticky=tk.W)
        ttk.Label(top, text="Amount (EGP):").grid(row=2,column=0,sticky=tk.W); self.e_other_amount = ttk.Entry(top); self.e_other_amount.grid(row=2,column=1,sticky=tk.W)
        ttk.Label(top, text="Date (YYYY-MM-DD):").grid(row=2,column=2,sticky=tk.W); self.e_other_date = ttk.Entry(top); self.e_other_date.insert(0, datetime.today().strftime("%Y-%m-%d")); self.e_other_date.grid(row=2,column=3,sticky=tk.W)
        ttk.Label(top, text="Notes:").grid(row=3,column=0,sticky=tk.W); self.e_other_notes = ttk.Entry(top, width=60); self.e_other_notes.grid(row=3,column=1,columnspan=3,sticky=tk.W)
        ttk.Button(top, text="Record", command=self.on_record_other).grid(row=4,column=0,columnspan=2,pady=6)

        bottom = ttk.Frame(frm, padding=10)
        bottom.pack(fill=tk.BOTH, expand=True)
        cols = ("id","date","type","category","amount","notes")
        self.tv_others = ttk.Treeview(bottom, columns=cols, show="headings")
        for c in cols:
            self.tv_others.heading(c, text=c.title())
        self.tv_others.pack(fill=tk.BOTH, expand=True)
        self.refresh_others()

    def on_record_other(self):
        try:
            amt = float(self.e_other_amount.get())
        except Exception:
            messagebox.showerror("Bad input", "Amount must be numeric in EGP")

        d = self.e_other_date.get().strip() or datetime.today().strftime("%Y-%m-%d")
        record_other(d, self.cmb_other_type.get(), self.e_other_cat.get().strip(), amt, self.e_other_notes.get().strip())
        messagebox.showinfo("OK", "Recorded.")
        self.refresh_others()

    def refresh_others(self):
        for i in self.tv_others.get_children():
            self.tv_others.delete(i)
        for r in query_others():
            self.tv_others.insert("", tk.END, values=(r[0], r[1], r[2], r[3], round(r[4],2), r[5]))

    def build_reports_tab(self):
        frm = self.tab_reports
        top = ttk.Frame(frm, padding=10)
        top.pack(fill=tk.X)
        ttk.Label(top, text="Reports & Export").grid(row=0,column=0,sticky=tk.W)
        ttk.Label(top, text="From (YYYY-MM-DD):").grid(row=1,column=0,sticky=tk.W); self.e_r_from = ttk.Entry(top); self.e_r_from.grid(row=1,column=1,sticky=tk.W)
        ttk.Label(top, text="To (YYYY-MM-DD):").grid(row=1,column=2,sticky=tk.W); self.e_r_to = ttk.Entry(top); self.e_r_to.grid(row=1,column=3,sticky=tk.W)
        ttk.Button(top, text="Show Inventory", command=self.on_show_inventory).grid(row=2,column=0)
        ttk.Button(top, text="Show Sales", command=self.on_show_sales).grid(row=2,column=1)
        ttk.Button(top, text="Show Other Entries", command=self.on_show_others).grid(row=2,column=2)
        ttk.Button(top, text="Compute P&L", command=self.on_compute_pnl).grid(row=2,column=3)
        ttk.Button(top, text="Export CSV", command=self.on_export_csv).grid(row=3,column=0,columnspan=2,pady=6)
        self.txt_report = tk.Text(frm, height=20)
        self.txt_report.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    def on_show_inventory(self):
        rows = query_inventory()
        out = "ID,SKU,Name,Qty,AvgCost(EGP),Value(EGP)\\n"
        for r in rows:
            out += f"{r[0]},{r[1]},{r[2]},{r[3]:.3f},{r[4]:.4f},{(r[3]* (r[4] or 0)):.2f}\\n"
        self.txt_report.delete("1.0", tk.END); self.txt_report.insert(tk.END, out)

    def on_show_sales(self):
        f = self.e_r_from.get().strip() or None; t = self.e_r_to.get().strip() or None
        rows = query_sales(f, t)
        out = "ID,SKU,Name,Date,Qty,UnitPrice,TotalEGP,COGS_EGP,Notes\\n"
        for r in rows:
            out += f"{r[0]},{r[1]},{r[2]},{r[3]},{r[4]:.3f},{r[5]:.2f},{r[6]:.2f},{r[7]:.2f},{r[8]}\\n"
        self.txt_report.delete("1.0", tk.END); self.txt_report.insert(tk.END, out)

    def on_show_others(self):
        f = self.e_r_from.get().strip() or None; t = self.e_r_to.get().strip() or None
        rows = query_others(f, t)
        out = "ID,Date,Type,Category,Amount(EGP),Notes\\n"
        for r in rows:
            out += f"{r[0]},{r[1]},{r[2]},{r[3]},{r[4]:.2f},{r[5]}\\n"
        self.txt_report.delete("1.0", tk.END); self.txt_report.insert(tk.END, out)

    def on_compute_pnl(self):
        f = self.e_r_from.get().strip() or None; t = self.e_r_to.get().strip() or None
        pnl = compute_pnl(f, t)
        out = f"Revenue: {pnl['revenue']:.2f} EGP\\nCOGS: {pnl['cogs']:.2f} EGP\\nGross Profit: {pnl['gross_profit']:.2f} EGP\\nOther Revenue: {pnl['other_revenue']:.2f} EGP\\nOther Expense: {pnl['other_expense']:.2f} EGP\\nNet Profit: {pnl['net_profit']:.2f} EGP\\n"
        self.txt_report.delete("1.0", tk.END); self.txt_report.insert(tk.END, out)

    def on_export_csv(self):
        # export current report text to CSV file selected by user
        content = self.txt_report.get("1.0", tk.END).strip().splitlines()
        if not content:
            messagebox.showwarning("Empty", "No report content to export. Generate a report first.")
            return
        path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files","*.csv")])
        if not path:
            return
        # try to parse as CSV-like lines separated by commas already
        with open(path, "w", newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            for line in content:
                # split by comma; if no commas, put full line into single column
                if ',' in line:
                    writer.writerow([c.strip() for c in line.split(",")])
                else:
                    writer.writerow([line])
        messagebox.showinfo("Saved", f"Report exported to {path}")

if __name__ == "__main__":
    init_db()
    app = App()
    app.mainloop()
