# 📁 Sample Files for CRM Import Tool

This directory contains various sample CSV files to demonstrate the enhanced client/supplier import functionality.

## 🏢 Company Sample Files

### 1. `sample_companies_basic.csv` - **Simple Start**
**Best for:** First-time users, basic relationship setup
```csv
Company Name,Is Client,Is Supplier,Notes
Acme Corporation,true,false,Premium software development client
Tech Solutions Ltd,false,true,Reliable IT consulting supplier
```
**Features:**
- ✅ Basic company information
- ✅ Simple client/supplier flags
- ✅ Perfect for learning the interface

---

### 2. `sample_companies_detailed.csv` - **Full Feature Demo**
**Best for:** Advanced users, complete relationship management
```csv
Company Name,Customer Number,Payment Terms,Invoice Email,Discount Days,DATEV Account,Leitweg ID
Acme Corporation,CLI-001,30,billing@acme.de,,1200,99ZZ-ACME12345
Tech Solutions Ltd,,,,,SUP001,14,2.5
```
**Features:**
- ✅ All client/supplier fields
- ✅ Payment terms and discount settings
- ✅ German/EU compliance (DATEV, Leitweg-ID)
- ✅ Comprehensive business data

---

### 3. `sample_companies_german_focus.csv` - **Deutsche Unternehmen**
**Best for:** German companies, DATEV integration, German compliance
```csv
Firmenname,Ist Kunde,Kundennummer,Zahlungsziel,DATEV Konto,Leitweg-ID
Müller & Partner GmbH,true,KD-001,30,1200,99ZZ-MUELLER12345
```
**Features:**
- ✅ German column headers
- ✅ German legal forms (GmbH, AG, UG, KG)
- ✅ DATEV accounting codes
- ✅ Leitweg-ID for e-invoicing
- ✅ German business terminology

---

### 4. `sample_companies_mixed_formats.csv` - **Format Flexibility**
**Best for:** Testing different data formats and boolean variations
```csv
Name,Client,Supplier,Net Days,Early Payment %
Alpha Solutions,yes,no,30,
Beta Manufacturing,1,1,45,2.5
Gamma Consulting,TRUE,FALSE,30,
```
**Features:**
- ✅ Various boolean formats (yes/no, 1/0, TRUE/FALSE)
- ✅ International addresses
- ✅ Mixed data types
- ✅ Edge case testing

---

## 🏷️ Tag Sample Files (NEW!)

### 5. `sample_companies_with_tags.csv` - **Comma-Separated Tags**
**Best for:** Users who prefer intuitive tag lists
```csv
Company Name,Tags,Is Client
Acme Corporation,"VIP, Enterprise, Marketing",true
Tech Solutions Ltd,"Supplier, IT Services, Verified",false
```
**Features:**
- ✅ Intuitive comma-separated tag format
- ✅ Unlimited tags per company
- ✅ Auto-detection and parsing
- ✅ Flexible spacing and quotes

### 6. `sample_companies_one_hot_tags.csv` - **Boolean Tag Columns**
**Best for:** Structured data with known tag sets
```csv
Company Name,Tag_VIP,Tag_Enterprise,Tag_Marketing,Is Client
Acme Corporation,1,1,1,true
Tech Solutions Ltd,0,0,0,false
```
**Features:**
- ✅ One-hot encoding (1/0 for each tag)
- ✅ Perfect for data exports from other systems
- ✅ Clear boolean logic
- ✅ Easy filtering and analysis

### 7. `sample_companies_mixed_tag_formats.csv` - **All Tag Formats**
**Best for:** Testing different tag approaches in one file
```csv
Company Name,Tags,Primary Tag,Tag_VIP,Category
Acme Corporation,"VIP, Enterprise",Marketing,1,Technology
```
**Features:**
- ✅ Combines comma-separated, single tag, and one-hot formats
- ✅ Demonstrates flexible tag detection
- ✅ Tests multiple tag sources per entity
- ✅ Real-world complexity simulation

### 8. `sample_persons_with_tags.csv` - **People with Tags**
**Best for:** Contact management with tag categorization
```csv
First Name,Last Name,Tags,Tag_VIP,Tag_Decision_Maker
John,Smith,"VIP, Decision Maker",1,1
Sarah,Johnson,"Technical, Developer",0,0
```
**Features:**
- ✅ Person-specific tag assignments
- ✅ Mixed tag formats for contacts
- ✅ Role-based tag categories
- ✅ Decision maker identification

---

## 👤 Person Sample Files

### 9. `sample_persons_enhanced.csv` - **Person with Company Links**
**Best for:** Importing contacts with company relationships
```csv
First Name,Last Name,Email,Company,Company Type
John,Smith,john.smith@acme.de,Acme Corporation,Client
Sarah,Johnson,sarah.j@techsolutions.co.uk,Tech Solutions Ltd,Supplier
```
**Features:**
- ✅ Person details with company links
- ✅ Company type indication
- ✅ Automatic company lookup during import

---

## 🎯 How to Use These Files

### **Step 1: Choose Your Scenario**
- **New to the tool?** → Start with `sample_companies_basic.csv`
- **Want full features?** → Use `sample_companies_detailed.csv`
- **German company?** → Try `sample_companies_german_focus.csv`
- **Testing formats?** → Use `sample_companies_mixed_formats.csv`

### **Step 2: Upload & Auto-Map**
1. Go to the **CRM Import Tool**
2. Select **"Companies"** as import type
3. Upload your chosen sample file
4. Click **"🎯 Auto-Map Fields"** - should map 70-90% automatically!

### **Step 3: Explore the Tabs**
- **📋 Basic Info** - Company name, address, contact info, general fields
- **💼 Client Settings** - Client relationship, payment terms, invoicing, DATEV/compliance
- **🏭 Supplier Settings** - Supplier relationship, discount terms, supplier-specific notes

### **Step 4: Check the Preview**
- Look at the **Client Preview** in the 💼 Client Settings tab
- Look at the **Supplier Preview** in the 🏭 Supplier Settings tab
- Verify relationship detection is working correctly
- See real-time counts and status (✅/❌)

---

## 💡 Field Mapping Examples

The auto-mapping will detect these patterns:

| CSV Column | Maps To | Example Values |
|------------|---------|----------------|
| `Is Client` | `is_client` | `true`, `1`, `yes` |
| `Customer Number` | `customer_number` | `CLI-001`, `C12345` |
| `Payment Terms` | `payment_time_day_num` | `30`, `14`, `45` |
| `Invoice Email` | `send_bill_to_email_to` | `billing@company.com` |
| `Discount Days` | `discount_day_num` | `14`, `21` |
| `Discount Percent` | `discount_percentage` | `2.5`, `1.0` |
| `DATEV Account` | `datev_account` | `1200`, `SUP001` |
| `Leitweg ID` | `leitweg_id` | `99ZZ-COMPANY123` |

### 🏷️ **Tag Mapping Examples (NEW!)**

The system automatically detects and handles three tag formats:

| CSV Column | Format | Example Values | Result |
|------------|--------|----------------|--------|
| `Tags` | Comma-separated | `"VIP, Enterprise, Marketing"` | Creates/assigns 3 tags |
| `Tag1`, `Primary Tag` | Single tag | `"VIP"`, `"Marketing"` | Creates/assigns 1 tag per column |
| `Tag_VIP`, `Tag_Enterprise` | One-hot | `1`, `0`, `true`, `false` | Extracts tag name from column |

**Tag Processing Features:**
- ✅ **Auto-detection** of tag columns and formats
- ✅ **Auto-creation** of missing tags with default colors
- ✅ **Case-insensitive** tag name matching
- ✅ **Flexible formats** - handles quotes, spaces, various boolean values
- ✅ **Multiple sources** - can combine different tag formats in one file
- ✅ **Preview & validation** - shows which tags will be created vs. assigned

---

## 🎨 New Tab Organization

The interface is now organized into three logical tabs:

### **📋 Basic Info Tab**
- ✅ **Company essentials**: Name, address, contact information
- ✅ **Business details**: Tax numbers, VAT ID, website
- ✅ **General fields**: Notes, additional information
- 💡 **Start here first** - these are the core company fields

### **💼 Client Settings Tab**
- ✅ **Client relationship**: `is_client` flag and identification
- ✅ **Payment & Invoicing**: Customer numbers, payment terms, invoice emails
- ✅ **Business rules**: Reference requirements, dunning settings
- ✅ **German compliance**: DATEV accounts, Leitweg-ID for e-invoicing
- 💡 **Use when companies are your clients** (they pay you)

### **🏭 Supplier Settings Tab**
- ✅ **Supplier relationship**: `is_supplier` flag and identification
- ✅ **Payment terms**: Discount periods, early payment rates
- ✅ **Supplier notes**: Vendor-specific comments and details
- 💡 **Use when companies are your suppliers** (you pay them)

This organization makes it much clearer which fields apply to which business relationships!

---

## 🚀 Advanced Tips

### **Multi-Language Support**
- German headers work: `Firmenname` → `name`
- English variations: `Company Name`, `Firm Name` → `name`
- Mixed formats supported in same file

### **Boolean Flexibility**
Client/Supplier fields accept:
- ✅ `true`, `false`
- ✅ `1`, `0`
- ✅ `yes`, `no`
- ✅ `TRUE`, `FALSE`
- ✅ Any value = true, empty = false

### **Relationship Combinations**
- **Client only**: `is_client=true`, `is_supplier=false`
- **Supplier only**: `is_client=false`, `is_supplier=true`
- **Both**: `is_client=true`, `is_supplier=true`
- **Neither**: Leave both empty (contact only)

### **German E-Invoicing**
For German companies, include:
- `leitweg_id`: Format like `99ZZ-COMPANYID123`
- `datev_account`: Your DATEV account code
- Payment terms in days for compliance

---

## 🔧 Troubleshooting

**Auto-mapping didn't work?**
- Check column names match patterns above
- Try manual mapping in the UI tabs
- Use "🗑️ Clear All" and "🎯 Auto-Map" again

**Relationship preview shows wrong data?**
- Verify boolean values in your CSV
- Check the 🤝 Relationships tab mapping
- Remember: any value = true, empty = false

**German fields not detected?**
- Use the 🇩🇪 German/EU tab for manual mapping
- Check Leitweg-ID format (should start with country code)

---

**Ready to import your own data?** Use these samples as templates and modify with your company information!