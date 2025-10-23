#!/bin/bash
# ==============================================
# Django ERP App Generator Script
# Project: MerchPro ERP (by Pro-Eng)
# Location: Root of repository (same level as business_core/)
# ==============================================

# Ensure script is run from repo root
if [ ! -d "business_core" ]; then
  echo "❌ Please run this script from the repository root (where 'business_core' folder exists)."
  exit 1
fi

cd business_core

# List of Django apps to create directly under business_core/
apps=(
  "inventory"
  "crm"
  "maintenance"
  "sales"
  "accounting"
  "dashboard"
  "procurement"
  "hr"
  "notifications"
  "analytics"
  "documents"
  "integration"
)

echo "🚀 Starting Django app creation inside business_core/ ..."

# Loop through and create each app if it doesn’t exist
for app in "${apps[@]}"; do
  if [ ! -d "$app" ]; then
    echo "📦 Creating app: $app"
    python ../manage.py startapp "$app"
  else
    echo "⚠️  Skipping $app (already exists)"
  fi
done

echo "✅ All apps created successfully under business_core/"
