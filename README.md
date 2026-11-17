# Security Incident & Compliance Tracking Dashboard

A Streamlit dashboard for centralized tracking of security incidents, vulnerabilities, remediation status and compliance-control mapping.

## Features
- KPI cards for total, open, critical/high, overdue and closed/resolved records.
- Filters by record type, severity and status.
- Severity distribution and remediation-status visualizations.
- Compliance-control tracking table.
- Prioritized incident/vulnerability register.
- Downloadable filtered CSV risk report.
- Supports CSV upload from an authorized source.

## Setup
```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
```

## Run
```bash
streamlit run app.py
```
The app loads `data/security_tracking_sample.csv` by default. You can upload another CSV from the sidebar.

## Required CSV columns
`Ticket ID`, `Type`, `Severity`, `Status`, `Owner`, `Reported Date`, `Due Date`, `Compliance Control`

Example values:
- Type: Incident, Vulnerability
- Severity: Critical, High, Medium, Low
- Status: Open, In Progress, Pending Validation, Closed, Resolved

## Notes
Sample data is synthetic. The dashboard does not connect to a live ticketing platform or independently certify compliance. Confirm source data and control mappings with the security/compliance team before operational use.
