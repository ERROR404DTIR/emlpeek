#!/usr/bin/env python3
"""EMLPeek: inspect RFC 5322 email files without extracting attachments."""
import argparse,json
from email import policy
from email.parser import BytesParser
from email.header import decode_header,make_header
from pathlib import Path
def decoded(value):
 if value is None:return ""
 try:return str(make_header(decode_header(str(value))))
 except (LookupError,UnicodeError):return str(value)
def inspect_message(data):
 msg=BytesParser(policy=policy.default).parsebytes(data);headers={k:decoded(v) for k,v in msg.items()};parts=[]
 for i,part in enumerate(msg.walk()):
  if part.is_multipart():continue
  payload=part.get_payload(decode=True) or b"";filename=decoded(part.get_filename())
  parts.append({"index":i,"content_type":part.get_content_type(),"filename":filename or None,"disposition":part.get_content_disposition(),"size":len(payload),"charset":part.get_content_charset()})
 body=[]
 for part in msg.walk():
  if part.is_multipart() or part.get_content_disposition()=="attachment":continue
  if part.get_content_type() in ("text/plain","text/html"):
   try:body.append(part.get_content())
   except (LookupError,UnicodeError,AttributeError):pass
 return {"headers":headers,"parts":parts,"body_preview":"\n".join(str(x) for x in body)[:4000],"attachments":[x for x in parts if x["filename"] or x["disposition"]=="attachment"]}
def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument("file",type=Path);p.add_argument("--json",action="store_true");a=p.parse_args()
 if not a.file.is_file():p.error("file not found")
 try:result=inspect_message(a.file.read_bytes())
 except OSError as e:p.error(str(e))
 if a.json:print(json.dumps(result,ensure_ascii=False,indent=2));return
 print("EMAIL HEADERS")
 for k,v in result["headers"].items():print(f"{k}: {v}")
 print("\nMIME PARTS")
 for x in result["parts"]:print(f"#{x['index']} {x['content_type']} · {x['size']} bytes · {x['filename'] or 'inline'}")
 print(f"\nAttachments: {len(result['attachments'])}")
 if result["body_preview"]:print("\nBODY PREVIEW\n"+result["body_preview"])
if __name__=="__main__":main()
