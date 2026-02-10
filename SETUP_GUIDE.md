# 🚀 Student Review System - Setup Guide

## Prerequisites

- Python 3.8 or higher
- Internet connection (for initial setup)
- 100MB free disk space

## Installation Steps

### Step 1: Verify Python Installation

```bash
python --version
# or
python3 --version
```

Should show Python 3.8 or higher.

### Step 2: Navigate to Project Directory

```bash
cd student-review-system
```

### Step 3: Install Dependencies

**Option A: Using pip (Recommended)**
```bash
pip install -r requirements.txt
```

**Option B: Manual installation**
```bash
pip install streamlit>=1.28.0
pip install pandas>=2.0.0
pip install plotly>=5.17.0
pip install vaderSentiment>=3.3.2
```

**Option C: Using virtual environment (Best Practice)**
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Step 4: Verify Installation

Run the test script:
```bash
python test_system.py
```

You should see:
```
🎉 ALL TESTS PASSED!
System is ready to use!
```

## Running the Application

### Start the Server

```bash
streamlit run app.py
```

The application will automatically open in your browser at:
```
http://localhost:8501
```

### Alternative: Specify Port

```bash
streamlit run app.py --server.port 8080
```

## First Time Setup

### 1. Login with Demo Credentials

**Parent Account:**
- Username: `parent1`
- Password: `pass1234`

**Teacher Account:**
- Username: `teacher`
- Password: `admin1234`

### 2. Explore Features

**As Parent:**
- View your child's dashboard
- Check sentiment analysis
- Download reports

**As Teacher:**
- Add new reviews
- Edit existing reviews
- View analytics

## Troubleshooting

### Issue: "Module not found" errors

**Solution:**
```bash
pip install --upgrade pip
pip install -r requirements.txt --force-reinstall
```

### Issue: Port already in use

**Solution:**
```bash
streamlit run app.py --server.port 8502
```

### Issue: CSV file not found

**Solution:**
Make sure `student_reviews.csv` is in the `data/` folder:
```bash
ls data/student_reviews.csv
```

### Issue: Slow performance

**Solution:**
Clear Streamlit cache:
```bash
# In the app, use the hamburger menu → Settings → Clear cache
```

Or add to your code:
```python
st.cache_data.clear()
```

## Configuration

### Adding New Users

Edit `modules/config.py`:

```python
USERS = {
    "parent1": {
        "password": "pass1234",
        "role": "parent",
        "student_id": "01"
    },
    "parent2": {  # Add new parent
        "password": "newpass123",
        "role": "parent",
        "student_id": "02"
    },
    "teacher": {
        "password": "admin1234",
        "role": "teacher",
        "student_id": None
    }
}
```

### Customizing Appearance

Edit `app.py` to modify the CSS:

```python
st.markdown("""
    <style>
    .main-header {
        color: #YOUR_COLOR;  # Change colors here
    }
    </style>
""", unsafe_allow_html=True)
```

## Data Management

### Backup Your Data

```bash
# Create backup
cp data/student_reviews.csv data/student_reviews_backup.csv
```

### Import New Student Data

1. Prepare CSV with required columns:
   - Student Number
   - Student Name
   - Grade
   - Subject
   - Archetype
   - Teacher Review
   - NLP Analysis (optional)

2. Replace or merge with existing `data/student_reviews.csv`

3. Restart the application

## Security Recommendations

### For Production Use:

1. **Change Default Passwords**
   ```python
   # In config.py, update:
   USERS = {
       "parent1": {"password": "STRONG_PASSWORD_HERE", ...}
   }
   ```

2. **Use Environment Variables**
   ```python
   import os
   
   USERS = {
       "parent1": {
           "password": os.getenv("PARENT1_PASSWORD"),
           ...
       }
   }
   ```

3. **Enable HTTPS**
   ```bash
   streamlit run app.py --server.sslCertFile cert.pem --server.sslKeyFile key.pem
   ```

4. **Implement Database Authentication**
   Replace the `USERS` dictionary with database queries

## Performance Optimization

### For Large Datasets (1000+ students):

1. **Enable caching in config**
   ```python
   # In data_handler.py
   @st.cache_data(ttl=600)  # Cache for 10 minutes
   ```

2. **Use pagination**
   Display students in batches of 50-100

3. **Optimize CSV reading**
   ```python
   df = pd.read_csv(csv_path, usecols=['needed', 'columns'])
   ```

4. **Consider database migration**
   Migrate from CSV to SQLite or PostgreSQL for better performance

## Advanced Features

### Enable Email Notifications

Add to `requirements.txt`:
```
smtplib  # For email
```

Implement in code:
```python
import smtplib
from email.mime.text import MIMEText

def send_notification(parent_email, summary):
    # Email logic here
    pass
```

### Schedule Automated Reports

Use `cron` (Linux/Mac) or Task Scheduler (Windows):
```bash
# Run daily at 6 PM
0 18 * * * python /path/to/generate_reports.py
```

## Development

### Running in Development Mode

```bash
streamlit run app.py --server.runOnSave true
```

Auto-reloads when you save code changes.

### Debugging

Add debug mode:
```python
# At top of app.py
DEBUG = True

if DEBUG:
    st.write("Debug info:", data)
```

## Deployment

### Deploy to Streamlit Cloud (Free)

1. Push code to GitHub
2. Visit [share.streamlit.io](https://share.streamlit.io)
3. Connect your repository
4. Deploy!

### Deploy to Custom Server

```bash
# Install PM2 for process management
npm install -g pm2

# Start application
pm2 start "streamlit run app.py" --name student-review-system

# Auto-start on boot
pm2 startup
pm2 save
```

## Support & Resources

- **Streamlit Docs**: https://docs.streamlit.io
- **VADER Documentation**: https://github.com/cjhutto/vaderSentiment
- **Plotly Charts**: https://plotly.com/python/

## Maintenance

### Regular Tasks

- **Weekly**: Backup CSV data
- **Monthly**: Review sentiment thresholds
- **Quarterly**: Update dependencies
  ```bash
  pip install --upgrade -r requirements.txt
  ```

## Next Steps

1. ✅ Complete installation
2. ✅ Test with demo accounts
3. ✅ Add your student data
4. ✅ Create user accounts
5. ✅ Customize branding
6. 🚀 Launch to users!

---

**Need Help?**

Check the main README.md for detailed documentation.
