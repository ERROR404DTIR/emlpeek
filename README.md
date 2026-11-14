<div align="center"><img src="assets/banner.svg" width="100%"><h1>EMLPeek</h1><p>Inspect email source and MIME structure without opening attachments.</p></div>

## Features
- Decode common encoded headers (Subject, From, To, Date).
- Display MIME part tree, content types, filenames and byte sizes.
- Show Authentication-Results and other raw headers as received.
- Optional JSON report for automation.
- Attachments are listed, never extracted or executed.

## Run
```bash
python app.py message.eml
python app.py message.eml --json
```
Python 3.9+, standard library only. The tool reads the supplied file locally; it does not contact mail servers. Treat email content as untrusted.

## Tests
```bash
python -m unittest discover -s tests -v
```
MIT License.