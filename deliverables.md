# Deliverables

This is your **answer sheet** for the whole course. When you finish a lab, open its readme (section *4. Write up* says what each item means), then write your answers under the matching Lab heading here and tick the boxes.

**Collecting numbers:** every script prints each run and then a summary line `[lab-id] key=value | ...` in the terminal; copy the summary lines into a table here (nothing is saved to a hidden log). State model, number of runs (`AISEC_N`) and date next to every table.

**Done means:** every item below is filled with measured data (command + settings noted), failures are kept, and each lab ends with one sentence: *what would I change in a real system because of this?*

---

## Lab 1 - Introduction: smoke test

- [ ] **Environment**
- [ ] **Seed vs sampling**

Results / notes:


---

## Lab 2 - Why AI security matters now: hunt for Shadow AI

- [ ] **AI inventory**
- [ ] **Scan and DNS evidence**
- [ ] **Shadow-AI gap**

### AI inventory (Shadow-AI hunt)

Guide reference: Section 2, Figure 4. Fill one row per AI tool found by the scans (code, DNS log, browser extensions, IDE plugins).

| Tool | Who uses it | Data types sent | Provider | Logging/training opt-out? | Policy exists? |
|---|---|---|---|---|---|
| | | | | | |

Results / notes:


---

## Lab 3 - Real-world vulnerability cases

- [ ] **3a: system-prompt leak**
- [ ] **3b: backdoor**
- [ ] **3c: distillation**

Results / notes:


---

## Lab 4 - Typical AI system architecture and the threat map

- [ ] **Architecture**
- [ ] **First run**

Results / notes:


---

## Lab 5 - From a list of threats to an analysis route

- [ ] **Threat model**
- [ ] **Route summary**

### Threat model - corporate assistant (reference app)

What each column means, with the word lists to use, is in `lessons/lab5/readme.md`. Aim for at least 8 rows covering at least 5 layers.

| # | Layer | Harm (NIST AI RMF) | Asset (ENISA) | Weakness class (OWASP LLM 2025) | Attack tactics (MITRE ATLAS) | Control | Residual risk | Owner |
|---|---|---|---|---|---|---|---|---|
| 1 | AI/data | Data leakage | Knowledge base, user permissions | LLM02 Sensitive Information Disclosure | Initial Access, Collection, Exfiltration | Access-aware retrieval (ACL), masking | Mis-labelled ACLs | Data owner |
| 2 | Application | Off-process action | Workflow systems, model context | LLM01 Prompt Injection | Initial Access, Execution, Impact | Trusted sources, human approval, tool policy | Direct injection by a user | Security |

Results / notes:


---

## Lab 6 - Worked example: harm, assets and weakness classes

- [ ] **Attack rates**
- [ ] **Retrieval (LLM08)**
- [ ] **Excessive agency (LLM06)**

Results / notes:


---

## Lab 7 - Attack chain, controls and residual risk

- [ ] **Controls matrix**
- [ ] **Residual risk**
- [ ] **Prediction check**

Results / notes:


---

## Lab 8 - How AI protection differs from classical software security

- [ ] **Results**
- [ ] **No parameterized prompt**

Results / notes:


---

## Lab 9 - Autoregression, tokenization and glitch tokens

- [ ] **Tokens and glitches**
- [ ] **Implications**

Results / notes:


---

## Lab 10 - Limitations users run into: hallucinations

- [ ] **Results**
- [ ] **Mitigation plan**

Results / notes:


---

## Lab 11 - Knowledge cutoff, memory and the context window

- [ ] **Results**
- [ ] **Effective window**

Results / notes:


---

## Lab 12 - Why models seem to understand: reasoning models and multimodality

- [ ] **Results**
- [ ] **Modality checklist**

Results / notes:


---

## Lab 13 - How models are trained and "made safe"

- [ ] **Results**
- [ ] **Layers of paint**

Results / notes:


---

## Lab 14 - Case study: reward hacking and the goblins

- [ ] **Curves**
- [ ] **Reflection**

Results / notes:


---

## Lab 15 - Alignment is necessary but not sufficient

- [ ] **Results**
- [ ] **Guardrail decision**

Results / notes:


---

## Lab 16 - Safe use of AI: what you send and what goes into the context

- [ ] **Data classification**
- [ ] **Redaction misses**
- [ ] **Context inventory**

### Data classification for AI use (Figure 44)

| File / data type | Example | Class | Allowed with external models? | Required handling |
|---|---|---|---|---|
| Secrets | .env, API keys, passwords | NEVER SEND | No | Rotate if ever sent; secret scanning in pre-commit |
| PII | passports, medical, financial | NEVER SEND | No | Local model only or anonymize first |
| Internal documents | contracts, strategy | CONFIDENTIAL | Only with approved provider + ZDR | |
| Anonymized / public / generic drafts | | OK WITH CAUTION | Yes | |
| (add your own file types) | | | | |

Results / notes:


---

## Lab 17 - The cost of context, prompt caching and economic security

- [ ] **Results**
- [ ] **Cost policy**

Results / notes:


---

## Lab 18 - Security principles: the jailbreak arms race

- [ ] **garak**
- [ ] **Encoding gap**
- [ ] **Multi-turn**
- [ ] **GCG**

Results / notes:


---

## Lab 19 - Zero trust and defense in depth

- [ ] **Results**
- [ ] **Zero-trust checklist**

Results / notes:


---

## Lab 20 - Protection tools: the AI Security Gateway

- [ ] **Gateway results**
- [ ] **Evasions**
- [ ] **Collusion**

Results / notes:


---

## Lab 21 - Zero Data Retention, sandboxing, kill switch and incident response

- [ ] **Persistence map**
- [ ] **Provider questionnaire**
- [ ] **Sandbox comparison**
- [ ] **IR playbook**
- [ ] **ZDR is not enough**

### Provider questionnaire (Zero Data Retention, Figure 54)

Fill from the provider's *documentation* (cite the URL and date) for two providers you really use.

| Question | Provider A | Provider B |
|---|---|---|
| Name / plan or tier | | |
| Default retention of prompts and outputs (days) | | |
| Used for model training by default? | | |
| Zero Data Retention available? How is it enabled? | | |
| Sub-processors / intermediaries in the path (search aggregators, gateways) | | |
| Data region | | |
| Can you delete data on request? | | |
| Decision: what may you send to this provider? | | |

### Incident-response playbook (Figure 57) - system: ______

| Step | What it means here (concrete) | Who | Tool / command | Evidence from your drill |
|---|---|---|---|---|
| DETECT | guardrail alert or anomaly in logs | | `lab22b_alerts.py` rule: | |
| CONTAIN | disable the tool / restrict functionality / kill switch | | `results/KILL_SWITCH` | |
| INVESTIGATE | which prompt, which attack vector, what data was affected | | `results/audit.jsonl` | |
| ERADICATE | update input filter / system prompt; remove poisoned chunk, rebuild embeddings | | | |
| RECOVER | restore functionality after testing | | `lab21c_drill.py --recover` | |
| LESSONS | add to red-team dataset | | `lab21d_add_attack.py` | |

AI-specific: prompt injection -> update filter, rebuild embeddings; data leakage -> remove chunk, add RBAC; denial of wallet -> semantic caching, token limits.

Results / notes:


---

## Lab 22 - Mapping threats to controls, monitoring and audit trails

- [ ] **Control mapping**
- [ ] **Alerts**
- [ ] **Dashboard**
- [ ] **Logging decisions**

### Threat -> control mapping (open-source edition)

| Layer | Threat | Control from your labs | Open-source option | Measured effect |
|---|---|---|---|---|
| Interface | Unauthorized access, DoS, wallet abuse | gateway token limit, `num_predict` cap | nginx/Caddy rate limits, LiteLLM budgets | |
| Application | Injection, jailbreak, improper output handling | LLM Guard, output escaping | NeMo Guardrails, Llama Guard | |
| AI / data | Poisoning, leakage, RAG manipulation | `acl`, `scan_docs`, `redact()` | Presidio, detect-secrets | |
| Agents | Tool misuse, excess privilege, collusion | `policy.check`, HITL, sandbox | Docker/gVisor, OPA | |
| Infrastructure | Secrets, misconfiguration, no monitoring | `--network none`, read-only FS | Vault/sops, Trivy | |
| Testing / lifecycle | No inventory, no regression tests | `attacks.jsonl`, garak in CI | promptfoo, garak | |

Results / notes:


---

## Lab 23 - Conclusion: red team / blue team capstone

- [ ] **Extended battery**
- [ ] **Before / after**
- [ ] **Risk register**
- [ ] **Management summary**

### Before / after (attack battery)

| Attack | OWASP / ATLAS tag | Baseline (:9001) | Hardened (:9000) | Notes |
|---|---|---|---|---|

### Residual-risk register

Guide reference: Section 7 (Figure 17 'management outcome'), Section 5 (route step 6).

| # | Residual risk | OWASP / ATLAS tag | Likelihood | Impact | Controls in place | Decision (accept / reduce / transfer) | Owner | Review date |
|---|---|---|---|---|---|---|---|---|

### Management summary (one page)

1. **Harm and assets at stake** (Section 6):
2. **What the attack battery showed** (numbers from the Before / after table above):
3. **Controls that mattered and why** (deterministic vs probabilistic):
4. **Residual risk we accept, and why** (see the Risk register above):
5. **Next three actions, owners, dates**:

Results / notes:


