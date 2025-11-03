# Running the Application - Quick Guide

## Server Status

The application server has been started in the background.

**Default URL:** http://localhost:8000

---

## Quick Start Checklist

### 1. ✅ Server Started
The server should be running on port 8000 (default).

### 2. ⚠️ Connection Configuration
You may need to create `connection.json` if it doesn't exist:
```bash
cp connection.json.example connection.json
```

Then edit `connection.json` with your IB connection details:
- **host**: `127.0.0.1` (localhost)
- **port**: `7497` for IB Gateway paper trading, `7496` for TWS
- **client_id**: Any unique number (e.g., `1`)
- **readonly**: `true` for safe testing
- **account_id**: Your IB account ID

### 3. ⚠️ Interactive Brokers Setup
Make sure **TWS** or **IB Gateway** is:
- ✅ Running on your computer
- ✅ Logged in to your account
- ✅ API enabled and configured:
  - TWS: File → Global Configuration → API → Settings
  - Gateway: Configure → Settings → API → Settings
  - Check "Enable ActiveX and Socket Clients"
  - Socket port matches your `connection.json` port

---

## Accessing the Application

### Web Interface
Open your browser and navigate to:
- **Dashboard**: http://localhost:8000/
- **Portfolio**: http://localhost:8000/portfolio
- **Rollover**: http://localhost:8000/rollover

### API Endpoints
- **Health Check**: http://localhost:8000/health
- **API Base**: http://localhost:8000/api/

### Example API Calls
```bash
# Check if server is running
curl http://localhost:8000/health

# Get OTM options for AAPL
curl "http://localhost:8000/api/options/otm?tickers=AAPL&otm=10"

# Get stock price
curl "http://localhost:8000/api/options/stock-price?tickers=AAPL"
```

---

## Server Management

### Stop the Server
Press `Ctrl+C` in the terminal where the server is running, or:
```bash
# Find and kill the process (Windows PowerShell)
Get-Process python | Where-Object {$_.Path -like "*python*"} | Stop-Process
```

### Change Port
```bash
PORT=8080 python run_api.py
```

### View Logs
Logs are in the `logs/` directory:
- `logs/api/` - API request logs
- `logs/server/` - Server logs
- `logs/tws/` - Interactive Brokers connection logs
- `logs/general/` - General application logs

---

## Troubleshooting

### Port Already in Use
If port 8000 is busy:
```bash
PORT=8001 python run_api.py
```

### Connection Errors
- Check that TWS/Gateway is running
- Verify API is enabled in TWS/Gateway settings
- Check that the port in `connection.json` matches TWS/Gateway API port
- Ensure `readonly: true` if you want to test safely

### Import Errors
Install dependencies:
```bash
pip install -r requirements.txt
```

### Database Errors
The app creates `options.db` automatically. If issues:
- Check file permissions
- Ensure directory is writable

---

## Testing Features

### Without IB Connection (Read-Only Mode)
Even without IB connected, you can:
- ✅ View the web interface
- ✅ Test API endpoints (some may return errors without connection)
- ✅ Navigate dashboard
- ✅ See UI components

### With IB Connection
With TWS/Gateway connected:
- ✅ View portfolio positions
- ✅ Get options data
- ✅ View recommendations
- ✅ Manage orders (if `readonly: false`)

---

## Next Steps

1. **Open Browser**: Navigate to http://localhost:8000
2. **Check Health**: Visit http://localhost:8000/health
3. **Explore Dashboard**: Navigate through the interface
4. **Test API**: Try API endpoints with curl or Postman
5. **Check Logs**: Monitor `logs/` directory for activity

---

**Server should be running at:** http://localhost:8000 🚀

