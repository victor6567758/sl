# Lab 23 - Conclusion: red team / blue team capstone

## 1. Read

So today we dived into AI security in practice. We understood why this is an important topic and why it is gaining momentum right now. We looked at several cases and understood how to work with threat maps, how to build attack chains and how to interrupt them. We worked out that in AI systems the language model itself must be considered an untrusted component, and all security must be built around it. And we reviewed the tools that make this possible. What remains now is to use this knowledge in practice.

**Key takeaways**

- AI security can be handled with threat maps, attack chains and layered controls.
- The language model itself is an untrusted component, so build security around it.

## 2. Goal

Run a measured before-and-after exercise on your own assistant: attack an unprotected twin and the protected gateway with the same attacks.

## 3. Do it

### Step 1 - Start both gateways

```bash
bash lessons/lab20/lab20a_run_gateway.sh --port 9001 --baseline
```

Unprotected twin (no guards). Keep it running; then, in a second terminal:
`bash lessons/lab20/lab20a_run_gateway.sh --port 9000` for the protected one.

### Step 2 - Attack the baseline

```bash
python lessons/lab23/lab23a_battery.py http://localhost:9001/chat baseline
```

Replays every attack in `attacks.jsonl` (leak, injection, off-topic, long output...).

**You should see:** Several attacks succeed.

### Step 3 - Attack the hardened gateway

```bash
python lessons/lab23/lab23a_battery.py http://localhost:9000/chat hardened
```

Same attacks.

**You should see:** Most are blocked. The Base64 and spelled-out leaks are your interesting leftovers.

### Step 4 - Extend and repeat

```bash
python lessons/lab21/lab21d_add_attack.py "name" "prompt" "regex"
```

Add the attacks from earlier labs (RAG injection, suffix, image, multi-turn, distillation), then rerun steps 2-3 after every change.

**You should see:** A before/after table and a one-page summary: who owns each risk, which controls come first, which residual risks you accept and why (Section 7).

## 4. Write up

Write your answers in the **Lab 23** section of [`deliverables.md`](../../deliverables.md). What to hand in:

- **Extended battery** - List >= 4 attacks you added from labs 6, 12, 15, 18 (one JSON line each) and append them to `lessons/lab23/attacks.jsonl`.
- **Before / after** - Fill the table in `deliverables.md`.
- **Risk register** - Fill the table in `deliverables.md`.
- **Management summary** - Fill the one-page template below.

## 5. Go further (optional)

- Present your result to a teammate using the six steps of Figure 11.

## If something goes wrong

- "Connection refused": start both gateways, each in its own terminal.
