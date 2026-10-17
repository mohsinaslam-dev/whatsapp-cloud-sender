# WhatsApp Cloud Sender

**Platform:** WhatsApp Business Cloud API (Meta)

Sends approved template messages from a CSV. Only rows with opted_in=yes are messaged, numbers are validated, and every send is rate-limited. Opt-in contacts only, never spam.

## Setup
```bash
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env    # then fill in your values
```
Environment variables: WHATSAPP_PHONE_ID, WHATSAPP_TOKEN

Load them before running (for example `export $(grep -v '^#' .env | xargs)` on Linux/macOS, or set them in your shell on Windows).

## Usage
```bash
python app.py contacts.sample.csv --template welcome --dry-run
python app.py contacts.csv --template welcome --lang en
```
Use `--dry-run` where available to see what would happen without calling the real API.

## Tests
The core logic is covered by tests that need no internet or credentials:
```bash
pip install pytest && pytest
```

## License
MIT
