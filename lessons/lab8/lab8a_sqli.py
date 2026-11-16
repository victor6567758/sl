"""Lab 8a - SQL injection IS solved: parameterized queries are a deterministic fix. Guide: Section 8 (Figure 19).

Run: python lessons/lab8/lab8a_sqli.py
"""
import sqlite3

from common import report

db = sqlite3.connect(":memory:")
db.execute("create table u(name, pw)")
db.execute("insert into u values('alice','s3cret')")


def concatenated_query(name):
    """Code and data mixed: the user's text becomes part of the SQL."""
    sql = f"select * from u where name='{name}'"
    print("  SQL sent:", sql)
    return db.execute(sql).fetchall()


def parameterized_query(name):
    """Data kept separate: the user's text can never become SQL."""
    sql = "select * from u where name=?"
    print("  SQL sent:", sql, "with value", repr(name))
    return db.execute(sql, (name,)).fetchall()


payload = "x' OR '1'='1"
print("concatenated:")
concatenated = concatenated_query(payload)
print("parameterized:")
parameterized = parameterized_query(payload)
report("8a", concatenated_returns=concatenated, parameterized_returns=parameterized)
