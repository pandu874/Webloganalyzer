# Web Server Log Analyzer

A Flask-based web application for analyzing web server log files. Upload log files to get insights on request counts, HTTP status code distributions, and identify malformed log entries.

## Features

- **File Upload**: Securely upload log files through a web interface
- **Stream-based Analysis**: Memory-efficient processing of large log files
- **Status Code Analysis**: Count and categorize HTTP status codes
- **Error Detection**: Identify and report malformed log lines
- **Web Dashboard**: Clean, responsive interface for viewing analysis results

## Installation

1. Clone or download this repository
2. Navigate to the project directory:
   ```bash
   cd log_analyzer_web
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Run the application:
   ```bash
   python app.py
   ```

2. Open your web browser and go to `http://localhost:5000`

3. Upload a log file using the web interface

4. View the analysis results on the dashboard

## Requirements

- Python 3.7+
- Flask 3.0+

## Project Structure

```
log_analyzer_web/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── analyzer/
│   ├── __init__.py
│   └── log_analyzer.py    # Core log analysis logic
├── templates/
│   ├── index.html         # Upload page
│   └── dashboard.html     # Results dashboard
├── static/
│   └── style.css          # CSS styling
├── logs/                  # Application logs
└── uploads/               # Uploaded log files
```

## Log Format Support

The analyzer expects log files in Common Log Format or similar formats where the HTTP status code appears as the penultimate token in each line. Examples:

```
127.0.0.1 - - [10/Oct/2023:13:55:36 -0700] "GET /index.html HTTP/1.1" 200 2326
192.168.1.1 - - [10/Oct/2023:13:55:37 -0700] "POST /api/data HTTP/1.1" 404 512
```

## Security Notes

- Uploaded files are stored temporarily in the `uploads/` directory
- The application uses secure filename handling
- Consider implementing file type validation for production use
- Replace the default secret key with a secure random key in production

## Contributing

Feel free to submit issues and enhancement requests!</content>
<parameter name="filePath">c:\Users\DELL\OneDrive\Desktop\webloganalyzer\log_analyzer_web\README.md
