import re
from urllib.parse import urlparse

KNOWN_MALICIOUS_INDICATORS = [
    "malicious-site.com",
    "fake-bank-login.com"
]

URGENT_WORDS = [
    "urgent",
    "immediately",
    "last warning",
    "account blocked",
    "verify now",
    "action required"
]

SENSITIVE_WORDS = [
    "password",
    "credit card",
    "bank account",
    "verification code",
    "login details"
]

KNOWN_BRANDS = {
    "paypal": "paypal.com",
    "google": "google.com",
    "microsoft": "microsoft.com",
    "apple": "apple.com",
    "amazon": "amazon.com"
}


def extract_links(text):
    if not text:
        return []
    return re.findall(r"https?://[^\s]+", text)


def extract_domain(email_or_url):
    if not email_or_url:
        return ""

    if "@" in email_or_url:
        return email_or_url.split("@")[-1].lower()

    parsed = urlparse(email_or_url)
    return parsed.netloc.lower().replace("www.", "")


def analyze_email(subject, sender, reply_to, body):
    score = 0
    reasons = []

    subject = subject or ""
    sender = sender or ""
    reply_to = reply_to or ""
    body = body or ""

    full_text = f"{subject} {body}".lower()
    links = extract_links(body)
    sender_domain = extract_domain(sender)

    # 1. Known malicious indicators
    for indicator in KNOWN_MALICIOUS_INDICATORS:
        if indicator in full_text or indicator in sender_domain:
            score += 50
            reasons.append("Known malicious indicator found")
            break

    # 2. Reply-To mismatch
    if reply_to:
        reply_to_domain = extract_domain(reply_to)
        if reply_to_domain and sender_domain and reply_to_domain != sender_domain:
            score += 25
            reasons.append("Reply-To domain is different from sender domain")

    # 3. Sensitive information request
    for word in SENSITIVE_WORDS:
        if word in full_text:
            score += 25
            reasons.append("Email requests sensitive information")
            break

    # 4. Multiple links
    if len(links) > 2:
        score += 15
        reasons.append("Email contains multiple links")

    # 5. Urgent / pressure language
    for word in URGENT_WORDS:
        if word in full_text:
            score += 15
            reasons.append("Urgent or pressure language detected")
            break

    # 6. Brand impersonation
    for brand, official_domain in KNOWN_BRANDS.items():
        if brand in full_text and official_domain not in sender_domain:
            score += 25
            reasons.append(f"Possible {brand.title()} impersonation")
            break

    # 7. Link domain differs from sender domain
    suspicious_link_domains = []
    for link in links:
        link_domain = extract_domain(link)
        if link_domain and sender_domain and sender_domain not in link_domain:
            suspicious_link_domains.append(link_domain)

    if suspicious_link_domains:
        score += 20
        reasons.append("Link domain differs from sender domain")

    score = min(score, 100)

    if score <= 30:
        verdict = "Safe"
    elif score <= 70:
        verdict = "Suspicious"
    else:
        verdict = "Phishing"

    return {
        "score": score,
        "verdict": verdict,
        "reasons": reasons or ["No strong phishing indicators found"],
        "links_count": len(links)
    }