# I2PE PII Protection Engine

Detects and protects Personally Identifiable Information (PII) such as names, phone numbers, emails and Aadhaar numbers in text/data.

## Features
- PII detection
- Masking / redaction of sensitive data
- Simple web interface

## Setup
1. Clone the repo:
   git clone https://github.com/Priyadharshini032007/I2PE-PII-Protection-Engine.git
   cd I2PE-PII-Protection-Engine
2. Create a virtual environment (optional):
   python -m venv venv
3. Install dependencies:
   pip install -r requirements.txt
4. Run:
   python app.py

## Environment Variables
Create a `.env` file (not committed):
- `API_KEY=your_key_here` (only if app.py uses one)

## Project Structure
- app.py: main application
- requirements.txt: dependencies
- docs/ARCHITECTURE.md: technical design
- sample_data/: sample inputs
- tests/: test cases
- LICENSE: MIT

## License
MIT
