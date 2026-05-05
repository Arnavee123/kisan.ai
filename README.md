# 🌾 Kisan.AI – Smart Farm Management System

A full-stack Django web application with AI-powered recommendations, YOLO object detection,
PDF chat queries, and a **blockchain-backed immutable audit trail**.

Built by: Saima Syeda, Arnavee Gite, Sameera Lakhote, Animesh Yadav
Guide: Prof. V. A. Injamuri | GCOE Chhatrapati Sambhajinagar

---

## 📁 Project Structure

```
kisan_ai/
├── manage.py
├── requirements.txt
├── .env.example                  ← Copy to .env and fill values
├── deploy_contract.py            ← Blockchain deployment script
│
├── kisan_ai/                     ← Django project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── inventory/                    ← Core inventory app
│   ├── models.py                 ← InventoryItem, Category, Alert, StockTransaction
│   ├── views.py                  ← Dashboard, CRUD, YOLO, Gemini, Market
│   ├── forms.py
│   ├── urls.py
│   └── admin.py
│
├── chat/                         ← PDF Chat module
│   ├── views.py                  ← PDF upload + Gemini Q&A
│   └── urls.py
│
├── blockchain/                   ← Ethereum blockchain integration
│   ├── KisanInventory.sol        ← Solidity smart contract
│   ├── service.py                ← Web3 Python interface
│   ├── views.py                  ← Audit trail UI
│   └── urls.py
│
├── templates/                    ← HTML templates
│   ├── base.html
│   ├── inventory/
│   │   ├── dashboard.html
│   │   ├── item_list.html
│   │   ├── item_form.html
│   │   ├── item_detail.html
│   │   ├── alerts.html
│   │   ├── yolo_detect.html
│   │   ├── recommendations.html
│   │   └── market_prices.html
│   ├── chat/
│   │   └── chat.html
│   └── blockchain/
│       ├── dashboard.html
│       └── item_history.html
│
└── media/                        ← Uploaded images and PDFs
```

---

## ⛓️ How Blockchain is Used in Kisan.AI

### The Problem Blockchain Solves

Traditional farm management apps store data in a central database that can be:
- Edited silently (no audit trail)
- Tampered with to falsify subsidy claims
- Lost if the server crashes

### The Kisan.AI Blockchain Solution

Every inventory action is permanently written to an **Ethereum smart contract**:

```
Farmer adds item  →  Django saves to DB  →  Blockchain logs immutable record
                                              (itemId, action, quantity,
                                               actor address, timestamp,
                                               SHA-256 data hash)
```

### What Gets Stored On-Chain

| Field        | Description                                      |
|-------------|--------------------------------------------------|
| `itemId`    | Database ID of the inventory item                |
| `action`    | "ADD", "UPDATE", "REMOVE", or "EXPIRY_ALERT"    |
| `quantity`  | Current quantity at time of action               |
| `timestamp` | Block timestamp (tamper-proof)                   |
| `actor`     | Ethereum wallet address of the operator          |
| `dataHash`  | SHA-256 of item JSON — detects off-chain tampering |
| `isValid`   | Record validity flag                             |

### Three Key Smart Contract Functions

```solidity
// 1. Log every inventory change (called by Django backend)
logInventoryAction(itemId, action, quantity, dataHash)

// 2. Retrieve full audit trail for any item
getItemHistory(itemId)  →  returns array of InventoryRecord

// 3. Verify data integrity (compare hash to detect tampering)
verifyRecord(itemId, recordIndex, expectedHash)  →  bool
```

### Real-World Benefits

1. **Subsidy Auditing** — Government officers can verify fertilizer usage on-chain
2. **Bank Loans** — Verified inventory history supports farm loan applications
3. **Tamper Detection** — Any change to off-chain DB can be detected via hash mismatch
4. **Multi-Party Trust** — Farmer, auditor, NGO all see the same immutable record
5. **Supply Chain** — Every purchase traced from vendor to storage to field use

### Blockchain Modes

| Mode      | When Active                              | Notes                         |
|-----------|------------------------------------------|-------------------------------|
| **Live**  | Ganache/Testnet running + contract deployed | Real transactions              |
| **Mock**  | No blockchain node (default)            | Simulated SHA-256 hash stored |

The system works perfectly without blockchain — it degrades gracefully.

---

## 🚀 How to Run on VS Code – Step by Step

### Prerequisites

Make sure these are installed on your computer:
- **Python 3.10+** — https://www.python.org/downloads/
- **VS Code** — https://code.visualstudio.com/
- **Git** — https://git-scm.com/ (optional)

---

### Step 1 — Open the Project in VS Code

1. Open VS Code
2. Go to **File → Open Folder**
3. Select the `kisan_ai` folder (the one containing `manage.py`)
4. VS Code will open the project

---

### Step 2 — Open the Integrated Terminal

In VS Code:
- Press **Ctrl + `** (backtick) to open the terminal
- Or go to **Terminal → New Terminal**

---

### Step 3 — Create a Virtual Environment

In the VS Code terminal, run:

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac / Linux
python3 -m venv venv
source venv/bin/activate
```

You should see `(venv)` at the start of your terminal prompt.

---

### Step 4 — Install Python Dependencies

```bash
pip install -r requirements.txt
```

This installs Django, OpenCV, PyMuPDF, Web3, and all other libraries.
It may take 2–5 minutes.

> ⚠️ If `opencv-python-headless` fails on Windows, try:
> `pip install opencv-python` instead.

---

### Step 5 — Configure Environment Variables

```bash
# Copy the example env file
cp .env.example .env
```

Now open `.env` in VS Code and fill in:

```
DJANGO_SECRET_KEY=any-random-long-string-here
DEBUG=True
GEMINI_API_KEY=your_key_here   ← Get free at https://makersuite.google.com/app/apikey
```

All other keys (Twilio, blockchain, weather) are **optional** — the app works without them.

---

### Step 6 — Run Database Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

This creates the SQLite database with all tables.

---

### Step 7 — Create Admin User (Optional)

```bash
python manage.py createsuperuser
```

Enter a username, email, and password. This lets you access `/admin/`.

---

### Step 8 — Load Sample Data (Optional)

```bash
python manage.py shell
```

Then paste this to add some demo inventory items:

```python
from inventory.models import Category, InventoryItem
from datetime import date, timedelta

s = Category.objects.get_or_create(name='Seeds')[0]
f = Category.objects.get_or_create(name='Fertilizer')[0]
p = Category.objects.get_or_create(name='Pesticide')[0]

InventoryItem.objects.create(name='Urea Fertilizer',    category=f, quantity=120, unit='kg',    min_quantity=20, batch_number='B2024-01', vendor='Iffco', expiry_date=date.today()+timedelta(days=90))
InventoryItem.objects.create(name='DAP Fertilizer',     category=f, quantity=8,   unit='bags',  min_quantity=10, batch_number='B2024-02', vendor='Coromandel', expiry_date=date.today()+timedelta(days=180))
InventoryItem.objects.create(name='Wheat Seeds',        category=s, quantity=50,  unit='kg',    min_quantity=5,  batch_number='S2024-01', expiry_date=date.today()+timedelta(days=365))
InventoryItem.objects.create(name='Chlorpyrifos Spray', category=p, quantity=2,   unit='liters',min_quantity=1,  expiry_date=date.today()-timedelta(days=10))
InventoryItem.objects.create(name='Cotton Seeds',       category=s, quantity=30,  unit='kg',    min_quantity=5,  expiry_date=date.today()+timedelta(days=20))

print("Sample data loaded!")
exit()
```

---

### Step 9 — Run the Development Server

```bash
python manage.py runserver
```

You should see:
```
Django version 4.2.7, using settings 'kisan_ai.settings'
Starting development server at http://127.0.0.1:8000/
```

---

### Step 10 — Open in Browser

Go to: **http://127.0.0.1:8000/**

The app will redirect to the Dashboard.

---

## 🔗 All Pages & URLs

| Page                  | URL                          |
|-----------------------|------------------------------|
| Dashboard             | http://127.0.0.1:8000/       |
| Inventory List        | http://127.0.0.1:8000/inventory/items/ |
| Add Item              | http://127.0.0.1:8000/inventory/items/add/ |
| YOLO Detection        | http://127.0.0.1:8000/inventory/yolo/ |
| AI Recommendations    | http://127.0.0.1:8000/inventory/recommendations/ |
| PDF Chat              | http://127.0.0.1:8000/chat/ |
| Alerts                | http://127.0.0.1:8000/inventory/alerts/ |
| Market Prices         | http://127.0.0.1:8000/inventory/market/ |
| Blockchain Audit      | http://127.0.0.1:8000/blockchain/ |
| Django Admin          | http://127.0.0.1:8000/admin/ |

---

## 🔗 Optional: Enable Blockchain (Ganache)

### Step A — Install Node.js
Download from https://nodejs.org/ (LTS version)

### Step B — Install Ganache CLI
```bash
npm install -g ganache
```

### Step C — Start Ganache
Open a **second terminal** in VS Code and run:
```bash
ganache --port 7545
```
Keep this terminal open.

### Step D — Deploy the Smart Contract
In your first terminal (with venv active):
```bash
pip install py-solc-x
python deploy_contract.py
```

Copy the printed `CONTRACT_ADDRESS` into your `.env` file.

### Step E — Restart Django
```bash
python manage.py runserver
```

Now the Blockchain Audit page will show live on-chain records!

---

## 🤖 Getting Your Free Gemini API Key

1. Go to https://makersuite.google.com/app/apikey
2. Sign in with your Google account
3. Click **"Create API Key"**
4. Copy the key and paste it in your `.env` as `GEMINI_API_KEY`

This enables:
- AI Resource Recommendations (fertilizer, irrigation, yield)
- PDF Chat Query answers

---

## 🧪 Testing All Features

| Feature              | How to Test                                                     |
|----------------------|-----------------------------------------------------------------|
| Add Inventory        | Go to Items → Add Item → fill form → Save                      |
| YOLO Detection       | Go to Detect via Camera → upload any image                      |
| Expiry Alerts        | Add item with past expiry date → Go to Alerts → Run Check       |
| AI Recommendations   | Go to AI Recommendations → enter crop details → Submit          |
| PDF Chat             | Go to PDF Chat → upload a PDF → type a question                 |
| Blockchain Log       | Add any item → Go to Blockchain Audit → see TX hash             |
| Market Prices        | Go to Market Prices → view simulated APMC data                  |
| Admin Panel          | Go to /admin/ → log in with superuser                           |

---

## 🐛 Common Errors & Fixes

| Error                              | Fix                                                          |
|------------------------------------|--------------------------------------------------------------|
| `ModuleNotFoundError: cv2`         | Run `pip install opencv-python`                             |
| `ModuleNotFoundError: fitz`        | Run `pip install PyMuPDF`                                    |
| `ModuleNotFoundError: web3`        | Run `pip install web3` (optional, for blockchain)           |
| `No module named 'dotenv'`         | Run `pip install python-dotenv`                             |
| `TemplateDoesNotExist`             | Make sure `templates/` folder is at project root            |
| Port 8000 already in use           | Run `python manage.py runserver 8001` instead               |
| Gemini returns error               | Check your `GEMINI_API_KEY` in `.env`                       |
| Blockchain not connecting          | Start Ganache first, then restart Django                     |

---

## 📌 Tech Stack Summary

| Layer          | Technology                         |
|----------------|------------------------------------|
| Backend        | Django 4.2 (Python)                |
| Database       | SQLite (dev) / PostgreSQL (prod)   |
| AI / LLM       | Google Gemini API                  |
| Computer Vision| OpenCV + YOLO (simulated)          |
| PDF Processing | PyMuPDF (fitz)                     |
| Blockchain     | Ethereum + Solidity + Web3.py      |
| Blockchain Node| Ganache (local dev)                |
| Frontend       | Django Templates + vanilla CSS/JS  |
| Alerts         | Twilio SMS/WhatsApp (optional)     |
| Weather        | OpenWeatherMap API (optional)      |
