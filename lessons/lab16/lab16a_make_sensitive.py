"""Lab 16a (setup) - create a FAKE project folder full of fake sensitive data. Guide: Section 16 (Figure 44).

Everything here is invented test data (4111... is a public test card number, the AWS key is Amazon's documentation example).
Creates lessons/lab16/proj/{notes.txt,.env,README.md}.

Run: python lessons/lab16/lab16a_make_sensitive.py
"""
import pathlib

proj = pathlib.Path(__file__).parent / "proj"
proj.mkdir(exist_ok=True)
(proj / "notes.txt").write_text("Client: John Smith, john.smith@example.com, phone +1 202-555-0143. Card 4111 1111 1111 1111. Passport X1234567.")
(proj / ".env").write_text("AWS_ACCESS_KEY_ID=AKIAIOSFODNN7EXAMPLE\nDB_PASSWORD=hunter2hunter2\n")
(proj / "README.md").write_text("# Public readme\nThis project parses logs.")
print("created", proj)
