"""Lab 10d - three types of statements: knowledge, source, computation. Guide: Section 10 (Figure 28).

Average of a 400-row column asked three ways. (3) shows the model WRITING code; you must READ it and
run it yourself (running model-written code unattended is what the sandbox of lab 21 is for).
The code is saved to results/lab10d_generated.py. Read it first; only then use --run, which executes THAT saved file (not a new one) in
results/ next to data.csv and compares its output with the true average (needs pandas).

Run: python lessons/lab10/lab10d_statement_types.py
     python lessons/lab10/lab10d_statement_types.py --run        # after you have READ results/lab10d_generated.py
"""
import argparse
import random
import subprocess
import sys

from common import RESULTS, chat, report, require_ollama

ap = argparse.ArgumentParser()
ap.add_argument("--run", action="store_true", help="execute the generated code (read it first!)")
args = ap.parse_args()
if args.run:    # execute the code saved by the previous run - after you have read it
    csv_path, code_path = RESULTS / "data.csv", RESULTS / "lab10d_generated.py"
    if not (csv_path.exists() and code_path.exists()):
        sys.exit("Run the script without --run first.")
    values = [int(l.split(",")[1]) for l in csv_path.read_text().splitlines()[1:]]
    r = subprocess.run([sys.executable, code_path.name], cwd=RESULTS, capture_output=True, text=True, timeout=120)
    report("10d-code-result", exit_code=r.returncode, output=(r.stdout or r.stderr).strip()[:80], truth=round(sum(values) / len(values), 2))
    sys.exit(0)
require_ollama("llama3.2")
rows = [random.randint(100, 999) for _ in range(400)]
csv = "id,value\n" + "\n".join(f"{i},{v}" for i, v in enumerate(rows))
here = RESULTS
here.mkdir(parents=True, exist_ok=True)
(here / "data.csv").write_text(csv)
truth = sum(rows) / len(rows)
alone = chat([{"role": "user", "content": "What is the average of the 'value' column of a table of 400 random 3-digit numbers? Number only."}])
ctx = chat([{"role": "user", "content": f"Average of the value column? Reply with just the number.\n{csv}"}], num_ctx=16384)
code = chat([{"role": "user", "content": "Write Python (pandas) that prints the mean of column 'value' in data.csv. Code only."}])
code = code.strip().removeprefix("```python").removeprefix("```").removesuffix("```").strip()
(here / "lab10d_generated.py").write_text(code + "\n")
report("10d", truth=round(truth, 2), model_alone=alone[:40], model_with_data_in_context=ctx[:40], generated_code=str(here / "lab10d_generated.py"))
print("\n--- generated code (read it before running) ---\n" + code)
