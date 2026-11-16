# data/

Runtime data for the labs. `data/kb/` is created by `python lessons/lab4/lab4a_make_kb.py` (or on first use by `common/corp_assistant.py`): four **fake** markdown documents with an access-list header (`ACL: all` / `ACL: hr`). `wiki_vpn_tips.md` carries the hidden prompt injection used in labs 6, 7, 15 and 19; `salary_bands.md` carries the canary `CANARY-SALARY-7731`. The content comes from `common/kbdata.py`: edit it there and rerun `lab4a_make_kb.py` to rewrite the folder.
