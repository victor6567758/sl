# Lab 8 - How AI protection differs from classical software security

## 1. Read

Let us now look at the fundamental limitations and vulnerabilities of AI systems. We start by understanding how protecting AI systems differs from protecting classical software. First, AI systems have probabilistic logic, as opposed to the deterministic logic of classical software. Also, in AI systems data and code are often inseparable: the instructions given to a model are given as ordinary text, which is data. The interpretability of AI models, especially large ones, is quite limited and difficult.

So, unlike ordinary code, which we can read, whose logic we can understand and where we can change a condition, control in AI systems can be far less transparent. At the same time, the protective mechanisms of classical software do not go away; we cannot abandon them. But where in classical software static code analysis, dynamic application analysis and a web application firewall are usually enough, in AI systems this is no longer sufficient.

![Figure 18](../../docs/figures/fig18.jpg)
*Figure 18*

For example, to simplify: in classical software there is an NX bit in the CPU that forbids running code from data. In AI systems, as we said, instructions are data. For example, we give the system a system prompt with some restrictions. The application may give its own instructions, and the user adds theirs. For the model all of this is a single, physically inseparable sequence of tokens. It is the model's own responsibility to work out which part is instructions, which part is data, and where an attack is taking place.

An analogy comes to mind here: classical software also has a vulnerability where code and data get mixed, namely SQL injection. But we actually understand well what to do about SQL injection: parameterized queries, a ban on concatenating queries with user input, sanitizing user input and so on. What to do about prompt injections, we do not fully know today; the problem is unsolved.

![Figure 19](../../docs/figures/fig19.jpg)
*Figure 19*

It is interesting to note, however, that even though we know what to do about SQL injections and have all the necessary tools, it still has not left the top of the OWASP threats today. Having tools and solutions does not mean they are always actually applied correctly.

**Key takeaways**

- AI systems are probabilistic, mix code and data, and are hard to interpret, so SAST, DAST and WAF are necessary but not sufficient.
- SQL injection is a solved class; prompt injection is not.

**References used by this lab** (full list: [References](../../README.md#references))

- **[1]** OWASP GenAI Security Project. OWASP Top 10 for LLM Applications 2025. https://genai.owasp.org/resource/owasp-top-10-for-llm-applications-2025/
- **[13]** Greshake, K., et al. “Not what you’ve signed up for: Compromising Real-World LLM-Integrated Applications with Indirect Prompt Injection.” arXiv:2302.12173, 2023. https://arxiv.org/abs/2302.12173

## 2. Goal

See why SQL injection is a solved problem while prompt injection is not.

## 3. Do it

### Step 1 - SQL: a fix that always works

```bash
python lessons/lab8/lab8a_sqli.py
```

Runs the same attack against a concatenated and a parameterized query.

**You should see:** The concatenated query leaks Alice's row; the parameterized one returns nothing, every time.

### Step 2 - Prompts: defenses that mostly work

```bash
python lessons/lab8/lab8b_prompt_injection.py
```

A summarizer gets a document with a hidden order. Four prompt layouts are compared on 2 models: none, role split, delimiters, datamarking.

**You should see:**

- Attack rates fall with each defense but never reach a guaranteed zero. The model cannot tell data from instructions the way a CPU's NX bit can (Figure 19).
- Compare `none` with `role_split`: does the system role help?

## 4. Write up

Write your answers in the **Lab 8** section of [`deliverables.md`](../../deliverables.md). What to hand in:

- **Results** - SQL output; the 4x2 attack-rate table (4 prompt layouts x 2 models); one observation about putting the instruction in the system vs user role.
- **No parameterized prompt** - One paragraph (Figure 19): why LLMs have no equivalent of a parameterized query.

## 5. Go further (optional)

- Make the injection stronger (edit `DOC`: longer, other language, encoded) and see which defense breaks first.

## If something goes wrong

- The attack rate is always 0%: make the document more insistent.
