# I2PE PII Protection Engine

A privacy protection tool that detects and redacts sensitive personal information (PII) from text documents. All processing happens locally.

## Features
- Detects emails, phone numbers, Aadhaar-like numbers and names
- Replaces detected values with `[REDACTED]`
- Upload a TXT file or paste text
- Download the protected text as a TXT file

## Setup
1. Clone the repo:
   ```
   git clone https://github.com/Priyadharshini032007/I2PE-PII-Protection-Engine.git
   cd I2PE-PII-Protection-Engine
   ```
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Run the app:
   ```
   streamlit run app.py
   ```

## Environment Variables
None required (all processing is local).

## Project Structure
- `app.py`: Streamlit user interface
- `pii_engine.py`: PII detection and redaction logic
- `requirements.txt`: dependencies
- `docs/ARCHITECTURE.md`: technical design
- `sample_data/`: sample input
- `tests/`: test cases
- `LICENSE`: MIT License

## Run Tests
```
pytest
```

## License
MIT
