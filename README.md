# LogLens

A Python CLI that reads application and Windows Event Viewer logs, detects error
patterns with regex classification, and prints a pre-triaged report (error type,
frequency, likely root cause) to speed up R&D escalations.

## Features
- Regex-based error classification (authentication, timeout, license, PDF, general)
- Frequency count for each error category
- Likely root cause for each category
- JSON / CSV reporting

## Usage
```bash
python src/loglens.py samples/sample.log
```

## Project structure
```
loglens/
├── src/loglens.py        # main script
├── samples/sample.log    # example input
├── docs/runbook.md       # troubleshooting runbook
└── README.md
```

## Author
Sai Vidhya Darshini
