"""Lab 4b - ask the reference assistant (RAG + simulated tools). Guide: Section 4 (Figure 8).

Without arguments it runs the three example questions of the lab:
  VPN question as group 'all'        -> retrieves vpn.md AND the poisoned wiki_vpn_tips.md (look at the sources)
  salary question as group 'hr'      -> allowed
  salary question as group 'all'     -> the same HR document leaks: there is no access control yet
With a question it asks that one, with the user groups and the controls you choose (see CONTROLS in common/corp_assistant.py).

Run: python lessons/lab4/lab4b_ask.py
     python lessons/lab4/lab4b_ask.py "How do I set up the VPN?" --groups all
     python lessons/lab4/lab4b_ask.py "What are the salary bands for L4?" --groups all --controls acl mask
"""
import argparse

from common import require_ollama
from common.corp_assistant import CONTROLS, ask

ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
ap.add_argument("question", nargs="?")
ap.add_argument("--groups", nargs="+", default=["all"], help="user groups, e.g. all or hr (default: all)")
ap.add_argument("--controls", nargs="*", default=[], choices=CONTROLS, help="controls to switch on")
ap.add_argument("--task", default=None, help="task profile for the 'policy' control: faq | support | mail")
ap.add_argument("--model", default=None)
a = ap.parse_args()

require_ollama("llama3.2", "nomic-embed-text")
cases = [(a.question, a.groups)] if a.question else [("How do I set up the VPN?", ["all"]), ("What are the salary bands for L4?", ["hr"]),
                                                      ("What are the salary bands for L4?", ["all"])]
for question, groups in cases:
    r = ask(question, set(groups), set(a.controls), model=a.model, task=a.task)
    print(f"\nQ: {question}   [groups={groups} controls={sorted(a.controls) or 'none'}]")
    print("sources    :", list(zip(r["sources"], r["similarity"])))
    print("tool call  :", r["tool_call"], "->", r["tool"])
    print("answer     :", r["answer"])
    if r["raw_answer"] != r["answer"]:
        print("raw answer :", r["raw_answer"])
