"""Lab 4a - create the fake knowledge base of the reference app. Guide: Section 4 (Figure 8), Section 6 (Figure 14).

Writes data/kb/*.md (4 fake documents). Line 1 of each file is an access list ("ACL: all" / "ACL: hr").
  vpn.md, onboarding.md   readable by everybody
  salary_bands.md         HR only; contains the canary CANARY-SALARY-7731
  wiki_vpn_tips.md        unverified wiki page with a hidden instruction (the indirect prompt injection of labs 6, 7, 15, 19)
The files come from common/kbdata.py. Run this script again after you edit that file (the app only builds the folder when it is empty).

Run: python lessons/lab4/lab4a_make_kb.py
"""
from common.kbdata import FILES, make_kb

path = make_kb()
print("knowledge base written to", path)
for name, text in FILES.items():
    print(f"  {name:18} {text.splitlines()[0]}")
