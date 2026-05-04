# Malicious Email Scorer – Gmail Add-on

## Overview

This project implements a phishing detection system composed of a Gmail Add-on and a Python backend service.

The system analyzes an opened email in Gmail and produces:

- A maliciousness score (0–100)
- A verdict (Safe / Suspicious / Phishing)
- Explainable reasons for the decision

The focus of this project is on **product thinking, system design, and explainability**, ensuring that each classification is **transparent and interpretable**.

This project was developed under time constraints, with a focus on building a functional end-to-end system rather than optimizing every component.

---

## Architecture

The system consists of three main parts:

### 1. Gmail Add-on

The Gmail Add-on is the user-facing product.

It is built with Google Apps Script and is responsible for:

- Displaying the UI inside Gmail
- Reading data from the opened email
- Sending the email data to the backend
- Displaying the score, verdict, and reasons

### 2. Backend Service

The backend is built with Python and FastAPI.

It is responsible for:

- Receiving structured email data
- Running the phishing scoring logic
- Returning a JSON response with score, verdict, and reasons

### 3. Communication Layer

During development, ngrok is used to expose the local backend over HTTPS so the Gmail Add-on can communicate with it.

---

## Flow

1. The user opens an email in Gmail.
2. The user clicks "Analyze Email".
3. The Gmail Add-on extracts the email subject, sender, and body.
4. The Add-on sends the data to the FastAPI backend.
5. The backend analyzes the email using a rule-based scoring model.
6. The backend returns a score, verdict, and reasons.
7. The Add-on displays the result to the user.

---

## Detection Logic

The system uses a rule-based scoring model. Each phishing signal adds points to the total score.

The final score is capped at 100.

### Scoring Signals

| Signal | Description | Score |
|---|---|---:|
| Known malicious domains | Detects known suspicious or phishing domains | +50 |
| Reply-To mismatch | Sender domain differs from Reply-To domain | +25 |
| Sensitive information request | Detects requests for password, credit card, bank account, or verification code | +25 |
| Multiple links | Email contains more than 2 links | +15 |
| Urgency or pressure language | Detects phrases such as urgent, immediately, last warning, or verify now | +15 |
| Brand impersonation | Known brand is mentioned but sender domain does not match the brand | +25 |
| Link domain mismatch | A link domain differs from the sender domain | +20 |

---

## Verdict Mapping

| Score Range | Verdict |
|---|---|
| 0–30 | Safe |
| 31–70 | Suspicious |
| 71–100 | Phishing |


---

## Example API Request

```json
{
  "subject": "URGENT! Verify your account",
  "sender": "support@fake-bank.com",
  "reply_to": "help@malicious-site.com",
  "body": "Your account will be blocked. Please verify your password immediately at http://fake-site.com"
}
```

## Example API Response

```json
{
  "score": 100,
  "verdict": "Phishing",
  "reasons": [
    "Known malicious indicator found",
    "Reply-To domain is different from sender domain",
    "Email requests sensitive information",
    "Urgent or pressure language detected",
    "Possible Paypal impersonation",
    "Link domain differs from sender domain"
  ],
  "links_count": 1
}
```

---

## Running the Backend

Navigate to the backend directory and install dependencies:

```bash
pip install -r requirements.txt
```

Run the backend:

```bash
uvicorn app:app --reload
```

Open the FastAPI Swagger UI:

```text
http://127.0.0.1:8000/docs
```

The Swagger UI was used during development to test different email examples and validate the scoring logic.

---

## Exposing the Backend with ngrok

Google Apps Script runs in Google's cloud environment, so it cannot access a local backend using `localhost` or `127.0.0.1`.

To allow the Gmail Add-on to communicate with the local backend, ngrok was used:

```bash
ngrok http 8000
```

The generated HTTPS URL was then used inside the Gmail Add-on code:

```javascript
const url = "https://your-ngrok-url/analyze";
```

---

## Gmail Add-on Setup

The Add-on was implemented using Google Apps Script and deployed as a Google Workspace Add-on, including OAuth configuration and test user setup.


---

## Challenges Encountered

### Gmail Add-on Visibility

One of the main challenges was getting the Add-on to appear inside Gmail.

The Add-on was successfully deployed and installed, but Gmail did not immediately show it in the interface. The issue was related to Gmail UI behavior and the Side Panel.

Steps taken included:

- Enabling Google Chat
- Verifying Gmail Add-on settings
- Testing in Incognito mode
- Reinstalling the Add-on
- Configuring the OAuth consent screen
- Adding the correct test user

Eventually, the Add-on was installed and connected successfully, although its visibility depended on Gmail UI behavior.

---

### Localhost Communication Issue

Initially, the Add-on attempted to call:

```text
http://127.0.0.1:8000
```

This failed because Apps Script runs in the cloud and cannot access local services.

The solution was to use ngrok to expose the backend via HTTPS, enabling communication between the Add-on and the local server.

---

### Static vs Dynamic Email Data

At first, the Add-on used a static payload, which caused all emails to return the same result.

The Add-on was then updated to extract real email data from Gmail, enabling dynamic analysis.

---

## Design Decisions

### Rule-Based Approach

A rule-based model was chosen because:

- It is simple and transparent
- It provides explainable results
- It fits well within the scope of a home assignment

### Separation of Components

The system was designed with a clear separation:

- Gmail Add-on: UI and user interaction
- Backend: scoring logic and analysis

This improves maintainability and makes the detection logic easier to test independently.

### Use of ngrok

ngrok was used to quickly expose the local backend during development without deploying it to a cloud provider.

---

## Security Considerations


- All inputs are treated as untrusted
- No external content is executed
- No sensitive data is stored

---

## Limitations

- The malicious domain list is static and used as a mock threat intelligence source.
- The scoring model is heuristic-based and may produce false positives or false negatives.
- A production deployment would require a stable hosted backend and stronger monitoring.

---

## Future Improvements


- Integrate machine learning models for improved phishing detection  
- Connect to real threat intelligence sources (e.g. domain blacklists, phishing databases such as Google Safe Browsing or VirusTotal)  
- Improve the Gmail Add-on UI for better user experience  

---

## Summary

This project demonstrates a complete phishing detection workflow:

- Extracting email data from Gmail
- Sending it to a backend service
- Scoring and classifying the email
- Returning clear and explainable results to the user

The project demonstrates the ability to design and implement an end-to-end solution, including frontend integration, backend logic, and real-world constraints such as cloud-to-local communication and Gmail platform limitations.

It reflects strong product thinking, system design, and the ability to make practical engineering trade-offs.

---

## Author

Alon Ashkenazi