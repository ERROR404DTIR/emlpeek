import unittest, app
class EMLTests(unittest.TestCase):
 def test_headers_and_attachment(self):
  raw=b"From: Alice <a@example.com>\r\nSubject: Hello\r\nMIME-Version: 1.0\r\nContent-Type: multipart/mixed; boundary=x\r\n\r\n--x\r\nContent-Type: text/plain; charset=utf-8\r\n\r\nHi\r\n--x\r\nContent-Type: application/octet-stream\r\nContent-Disposition: attachment; filename=sample.bin\r\nContent-Transfer-Encoding: base64\r\n\r\nAQID\r\n--x--\r\n"
  r=app.inspect_message(raw)
  self.assertEqual(r["headers"]["Subject"],"Hello")
  self.assertEqual(r["attachments"][0]["filename"],"sample.bin")
  self.assertEqual(r["attachments"][0]["size"],3)
if __name__=="__main__":unittest.main()
