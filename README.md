# linkedin-post-timestamp-extractor
Python script to extract LinkedIn activity IDs from post URLs and convert them into human-readable timestamps using Snowflake decoding methodology for OSINT investigations.
# LinkedIn Post Timestamp Extractor

This Python project extracts timestamps from LinkedIn post URLs by decoding LinkedIn Snowflake Activity IDs.

## 🔎 Purpose
Useful for OSINT investigations, digital intelligence analysis, and social media timeline verification.

## ⚙️ Features
- Extract activity ID from LinkedIn URL
- Convert ID to binary
- Decode timestamp bits
- Convert into UTC human-readable time

## 🧠 How It Works
LinkedIn uses Snowflake IDs where:
- First 42 bits = timestamp (milliseconds)
- Epoch starts at Jan 1, 2010 (UTC)

## 🚀 Usage

```bash
python timestamp_extractor.py
