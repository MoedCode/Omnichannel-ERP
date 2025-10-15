# API Usage Examples

This document provides practical examples of using the OmniMerch ERP API.

## Authentication

### 1. Obtain JWT Token
```bash
curl -X POST http://localhost:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "your_username",
    "password": "your_password"
  }'
```

Response:
```json
{
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

### 2. Refresh Access Token
```bash
curl -X POST http://localhost:8000/api/token/refresh/ \
  -H "Content-Type: application/json" \
  -d '{
    "refresh": "your_refresh_token"
  }'
```

## Inventory Management

### Create a Category
```bash
curl -X POST http://localhost:8000/api/inventory/categories/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Electronics",
    "description": "Electronic devices and accessories"
  }'
```

### Create a Supplier
```bash
curl -X POST http://localhost:8000/api/inventory/suppliers/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Tech Supplies Inc",
    "contact_person": "John Doe",
    "email": "john@techsupplies.com",
    "phone": "+1234567890",
    "address": "123 Tech Street, Silicon Valley"
  }'
```

### Create a Product
```bash
curl -X POST http://localhost:8000/api/inventory/products/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Laptop",
    "sku": "LAP-001",
    "description": "High-performance laptop",
    "category": 1,
    "supplier": 1,
    "cost_price": "800.00",
    "selling_price": "1200.00",
    "quantity_in_stock": 50,
    "reorder_level": 10,
    "status": "ACTIVE"
  }'
```

### Get Low Stock Products
```bash
curl -X GET http://localhost:8000/api/inventory/products/low_stock/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### Record Stock Movement
```bash
curl -X POST http://localhost:8000/api/inventory/stock-movements/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "product": 1,
    "movement_type": "IN",
    "quantity": 100,
    "reference": "PO-2024-001",
    "notes": "Received from supplier"
  }'
```

## CRM (Customer Relationship Management)

### Create a Customer
```bash
curl -X POST http://localhost:8000/api/crm/customers/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "ABC Corporation",
    "customer_type": "BUSINESS",
    "email": "contact@abc.com",
    "phone": "+1234567890",
    "address": "456 Business Ave",
    "city": "New York",
    "country": "USA"
  }'
```

### Create a Lead
```bash
curl -X POST http://localhost:8000/api/crm/leads/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Jane Smith",
    "email": "jane@example.com",
    "phone": "+1234567890",
    "company": "Smith Industries",
    "status": "NEW",
    "source": "Website",
    "notes": "Interested in bulk purchase"
  }'
```

### Record a Contact
```bash
curl -X POST http://localhost:8000/api/crm/contacts/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "customer": 1,
    "contact_type": "EMAIL",
    "subject": "Follow-up on quotation",
    "description": "Sent quotation for 50 units",
    "contact_date": "2024-10-15T10:00:00Z"
  }'
```

## Maintenance Management

### Create an Asset
```bash
curl -X POST http://localhost:8000/api/maintenance/assets/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Industrial Printer",
    "asset_tag": "ASSET-001",
    "description": "Heavy-duty industrial printer",
    "customer": 1,
    "purchase_date": "2024-01-01",
    "warranty_expiry": "2025-01-01",
    "status": "OPERATIONAL"
  }'
```

### Create a Work Order
```bash
curl -X POST http://localhost:8000/api/maintenance/work-orders/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "order_number": "WO-2024-001",
    "asset": 1,
    "customer": 1,
    "title": "Routine Maintenance",
    "description": "Quarterly maintenance check",
    "status": "PENDING",
    "priority": "MEDIUM",
    "scheduled_date": "2024-10-20T09:00:00Z",
    "estimated_cost": "150.00"
  }'
```

## Sales

### Create a POS Order
```bash
curl -X POST http://localhost:8000/api/sales/orders/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "order_number": "ORD-2024-001",
    "order_type": "POS",
    "customer": 1,
    "status": "PENDING",
    "payment_status": "UNPAID",
    "subtotal": "1000.00",
    "tax": "100.00",
    "discount": "0.00",
    "total": "1100.00"
  }'
```

### Add Order Items
```bash
curl -X POST http://localhost:8000/api/sales/order-items/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "order": 1,
    "product": 1,
    "quantity": 2,
    "unit_price": "500.00"
  }'
```

### Record Payment
```bash
curl -X POST http://localhost:8000/api/sales/payments/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "order": 1,
    "payment_method": "CARD",
    "amount": "1100.00",
    "reference": "TXN-123456",
    "notes": "Payment completed successfully"
  }'
```

## Accounting

### Create an Invoice
```bash
curl -X POST http://localhost:8000/api/accounting/invoices/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "invoice_number": "INV-2024-001",
    "customer": 1,
    "order": 1,
    "issue_date": "2024-10-15",
    "due_date": "2024-11-15",
    "status": "SENT",
    "subtotal": "1000.00",
    "tax": "100.00",
    "discount": "0.00",
    "total": "1100.00"
  }'
```

### Create an Account
```bash
curl -X POST http://localhost:8000/api/accounting/accounts/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "account_number": "1000",
    "account_name": "Cash",
    "account_type": "ASSET",
    "description": "Cash on hand",
    "is_active": true
  }'
```

### Record a Ledger Entry
```bash
curl -X POST http://localhost:8000/api/accounting/ledger-entries/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "account": 1,
    "entry_type": "DEBIT",
    "amount": "1100.00",
    "description": "Payment received for invoice INV-2024-001",
    "reference": "INV-2024-001",
    "transaction_date": "2024-10-15"
  }'
```

### Record an Expense
```bash
curl -X POST http://localhost:8000/api/accounting/expenses/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "expense_number": "EXP-2024-001",
    "category": "UTILITIES",
    "amount": "200.00",
    "description": "Monthly electricity bill",
    "expense_date": "2024-10-15"
  }'
```

## Dashboard & Reports

### Get Dashboard Overview
```bash
curl -X GET http://localhost:8000/api/dashboard/overview/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### Get Sales Report
```bash
curl -X GET http://localhost:8000/api/dashboard/reports/sales/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### Get Inventory Report
```bash
curl -X GET http://localhost:8000/api/dashboard/reports/inventory/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

## Filtering and Search

### Search Products
```bash
curl -X GET "http://localhost:8000/api/inventory/products/?search=laptop" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### Filter by Category
```bash
curl -X GET "http://localhost:8000/api/inventory/products/?category=1" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### Filter and Order
```bash
curl -X GET "http://localhost:8000/api/inventory/products/?status=ACTIVE&ordering=-created_at" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### Pagination
```bash
curl -X GET "http://localhost:8000/api/inventory/products/?page=2" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

## Tips

1. Always include the Authorization header with your access token
2. Use the refresh token to get a new access token when it expires
3. Check the Swagger documentation at `/swagger/` for detailed API schema
4. Use query parameters for filtering, searching, and pagination
5. All timestamps should be in ISO 8601 format
