# AI Security and the Vulnerability Landscape: a hands-on course

This repository turns the learning guide *AI Security and the Vulnerability Landscape* into 23 labs you run on your own computer, with local open-source models. **Lab `N` is guide Section `N`.** Each lab readme contains the guide's text for that section, so you never need the original PDF: you open a lab, read, do the steps, and write down what you measured.

## The idea in one page

AI is adopted faster than it is protected. People start using it because it makes work easier; protection never appears by itself. The gap between the two is where most vulnerabilities live, and much of it is invisible, because nobody knows which tools are already in use ([lab 2](lessons/lab2/readme.md)).

To reason about that gap you need a map. An AI system is a stack: an interface, an application, a language model with its data and memory, agents with tools, and the infrastructure and lifecycle around them. Every layer has its own threats, and standard catalogues (OWASP, MITRE ATLAS, NIST, ENISA) already name them. The useful question is not "which threats exist?" but a route: what harm, to what asset, through which weakness, by which attack chain, stopped by which control, with which risk left over ([lab 3](lessons/lab3/readme.md)-[lab 7](lessons/lab7/readme.md)).

The route only makes sense once you know what a model really is. It writes one token at a time, treats instructions and data as the same stream of text, optimizes for plausible rather than true, forgets everything between chats, uses long contexts badly, and is shaped by training in thin layers that clever prompts can scrape through. None of this is a bug that the next model will fix; it is the architecture ([8](lessons/lab8/readme.md), [9](lessons/lab9/readme.md), [10](lessons/lab10/readme.md), [11](lessons/lab11/readme.md), [12](lessons/lab12/readme.md), [13](lessons/lab13/readme.md), [14](lessons/lab14/readme.md)). So the model must be treated as an **untrusted component**, and protection must be built around it ([lab 15](lessons/lab15/readme.md)).

Around the model, safe use starts with knowing what you send and what it costs ([16](lessons/lab16/readme.md), [17](lessons/lab17/readme.md)). Defense then follows the same pattern everywhere: assume the filter has holes, stack independent layers, keep the deciding rules in code outside the model, give every agent and tool the least privilege, isolate what you cannot control, watch everything, and keep a way to shut it down ([18](lessons/lab18/readme.md), [19](lessons/lab19/readme.md), [20](lessons/lab20/readme.md), [21](lessons/lab21/readme.md), [22](lessons/lab22/readme.md)). Attackers keep finding new angles (encodings, optimized suffixes, multi-turn games), so this is an arms race and not a checklist.

The capstone ([lab 23](lessons/lab23/readme.md)) ties it together: attack your own assistant before and after the defenses, measure, and decide which residual risks you accept and why.

Because attacks on language models are probabilistic, every script repeats its trials and reports a **rate**. A 0% result is still a result.

## How to work through it

1. Do the one-time setup below.
2. Start at [`lessons/lab1/readme.md`](lessons/lab1/readme.md) and go in order. In each lab readme: **1. Read**, **2. Goal**, **3. Do it** (numbered steps with exact commands and what you should see), **4. Write up**, then the optional extras.
3. Write your answers in [`deliverables.md`](deliverables.md), the answer sheet for all labs.

Run every command from the folder that contains `lessons/`.

### One-time setup

```bash
bash lessons/lab1/lab1a_pull_models.sh                  # Ollama (ollama.com) must be installed; pulls models (several GB)
python3 -m venv .venv && source .venv/bin/activate      # Windows: use WSL2
pip install -r requirements.txt && pip install -e .     # -e makes `from common import ...` work anywhere
python -m spacy download en_core_web_lg                 # lab 16 only
```

16 GB RAM is comfortable (8 GB works with the 3B models). A GPU only speeds up the training labs and the suffix search. Docker is needed for labs 21 and 22. Heavy tools (gateway, garak, nanoGCG, mitmproxy) get their own virtual environments, created by their scripts.

### Settings

Optional environment variables (set once per terminal, e.g. `export AISEC_N=5`; PowerShell: `$env:AISEC_N = 5`); the defaults work:

| Variable | Meaning | Default |
|---|---|---|
| `AISEC_N` | repetitions per measurement (lower it on a slow machine) | per lab |
| `AISEC_MODEL` | main model | `llama3.2:3b` |
| `AISEC_MODEL2` | second model for comparisons | `qwen2.5:3b` |

More variables (`OLLAMA_URL`, `AISEC_RESULTS`, ...) are listed in [`common/readme.md`](common/readme.md).

## Guide sections and labs

| Guide section | Core idea | Lab | OWASP LLM 2025 / ATLAS tags |
|---|---|---|---|
| 1 Introduction | the five areas of the course | [lab 1](lessons/lab1/readme.md) | - |
| 2 Why AI security matters now | adoption outruns protection; Shadow AI | [lab 2](lessons/lab2/readme.md) | - |
| 3 Real-world cases | a prompt leak, a backdoor, model theft | [lab 3](lessons/lab3/readme.md) | LLM01, LLM04, LLM10 |
| 4 Architecture and threat map | layers of an AI system and their threats | [lab 4](lessons/lab4/readme.md) | map of all |
| 5 From threat list to route | harm, assets, weakness, attack, controls, residual risk | [lab 5](lessons/lab5/readme.md) | LLM01-10, ATLAS tactics |
| 6 Worked example | a RAG assistant: injection, disclosure, embeddings, agency | [lab 6](lessons/lab6/readme.md) | LLM01, 02, 06, 08 |
| 7 Attack chain and residual risk | break every link; accept what is left on purpose | [lab 7](lessons/lab7/readme.md) | Initial Access ... Impact |
| 8 AI vs classical security | probabilistic, code = data; SQL injection solved, prompt injection not | [lab 8](lessons/lab8/readme.md) | LLM01 |
| 9 Autoregression and tokens | token by token generation; glitch tokens | [lab 9](lessons/lab9/readme.md) | LLM01 (special case) |
| 10 Hallucinations | plausibility is not truth; benchmarks reward guessing | [lab 10](lessons/lab10/readme.md) | LLM09 |
| 11 Cutoff, memory, context window | frozen knowledge; stateless chats; lost in the middle | [lab 11](lessons/lab11/readme.md) | - |
| 12 Reasoning and multimodality | fluent is not understanding; every modality is an attack surface | [lab 12](lessons/lab12/readme.md) | LLM01 |
| 13 Training and "made safe" | pretraining, SFT, RLHF; layers of paint | [lab 13](lessons/lab13/readme.md) | LLM04 |
| 14 Reward hacking | a gamed evaluator; conflicting objectives | [lab 14](lessons/lab14/readme.md) | - |
| 15 Alignment is not enough | the model is an untrusted component; external guardrails | [lab 15](lessons/lab15/readme.md) | LLM01 |
| 16 Safe use: what you send | context is more than a prompt; classify data | [lab 16](lessons/lab16/readme.md) | LLM02 |
| 17 Cost and caching | history is resent; prefix cache; denial of wallet | [lab 17](lessons/lab17/readme.md) | LLM10 |
| 18 The jailbreak arms race | persuasion, filters, encodings, suffixes, multi-turn | [lab 18](lessons/lab18/readme.md) | LLM01, Defense Evasion |
| 19 Zero trust, defense in depth | validate everything; Swiss cheese | [lab 19](lessons/lab19/readme.md) | LLM05, LLM06 |
| 20 AI Security Gateway | ingress, egress, tool, RAG and agent guards; collusion | [lab 20](lessons/lab20/readme.md) | LLM01, 02, 06 |
| 21 ZDR, sandbox, kill switch, IR | ZDR is not full protection; isolate agents; playbook | [lab 21](lessons/lab21/readme.md) | LLM06 |
| 22 Monitoring and audit trails | threat to control mapping; logs, metrics, alerts, SIEM | [lab 22](lessons/lab22/readme.md) | - |
| 23 Conclusion | threat maps, attack chains and layered controls together | [lab 23](lessons/lab23/readme.md) | all |

### Where to practise a concept

| Concept | Labs |
|---|---|
| Direct and indirect prompt injection | 3a, 6, 7, 8b, 15b, 18 |
| System-prompt extraction | 3a |
| Data and model poisoning, backdoors | 3b, 6, 13b |
| Model theft and extraction | 3c |
| Access control, least privilege, human approval | 7, 19a |
| Guardrails and classifiers | 15, 18b, 20 |
| Obfuscation, optimized suffixes, multi-turn attacks | 18 |
| Hallucination and verification | 10 |
| Context window, cost, caching | 11, 17 |
| Data exposure and privacy | 2, 16, 21a |
| Sandboxing, kill switch, incident response | 21 |
| Monitoring and SIEM | 22 |

## Repository layout

```
README.md  deliverables.md     this article; the answer sheet for all labs
lessons/labN/                  one folder per lab: readme.md + scripts
common/                        shared library and the reference assistant (common/readme.md)
docs/figures/                  the guide's figures, used by the lab readmes
data/, results/                generated fake knowledge base; generated logs and artifacts (git-ignored)
```

## Safety and limits

- Attack only models you run yourself. Payloads are harmless markers (`PWNED`, `CANARY-...`), tools are simulated (a log line), and all "sensitive" data is fake.
- The scripts were checked offline only (syntax, shared library, controls and most scripts against a fake Ollama), not against real models. Library options of garak, LLM Guard, nanoGCG and Ollama may need small fixes.
- The guide's statements about specific incidents (Bing Chat, DeepSeek, OpenAI) are the speaker's own account and were not independently verified.
- In guide Section 17 the growth of cost is called exponential. One request grows linearly with the history, and the total cost of a whole conversation grows quadratically ([lab 17](lessons/lab17/readme.md) shows it).
- Four figures of the guide (1, 58, 61, 62: title and closing slides, and two slides listing a vendor's products) are not included; their numbers are skipped in the lab readmes.

## References

The guide's own reference list; numbers `[n]` are the ones used in the lab readmes. Entries [13]-[16] are arXiv links that the guide's author did not re-open while preparing the guide.

### Frameworks and standards

**[1]** OWASP GenAI Security Project. OWASP Top 10 for LLM Applications 2025. https://genai.owasp.org/resource/owasp-top-10-for-llm-applications-2025/  
Weakness classes used in the worked example (prompt injection, sensitive information disclosure, excessive agency, vector and embedding weaknesses). Sections 5–8, 18. Check the OWASP site for newer editions. *Used in: labs 3, 5-8, 18.*

**[2]** National Institute of Standards and Technology. Artificial Intelligence Risk Management Framework (AI RMF 1.0), NIST AI 100-1, January 2023. https://doi.org/10.6028/NIST.AI.100-1  
Harm, context and risk owners; the Govern, Map, Measure and Manage functions. NIST also publishes a Generative AI Profile (NIST AI 600-1, July 2024) as a companion. Sections 5–7, 19. *Used in: labs 5-7, 19.*

**[3]** European Union Agency for Cybersecurity (ENISA). AI Cybersecurity Challenges: Threat Landscape for Artificial Intelligence, December 2020. https://www.enisa.europa.eu/publications/artificial-intelligence-cybersecurity-challenges  
Asset and threat taxonomy for AI systems; useful for defining what you are protecting and from whom. Sections 5–7. The report is from 2020, so it predates modern LLM agents. *Used in: labs 5-7.*

**[4]** MITRE. ATLAS: Adversarial Threat Landscape for AI Systems. https://atlas.mitre.org/  
ATT&CK-style tactics, techniques and case studies for attacks on AI systems, used here to model the attack chain. Sections 5, 7. *Used in: labs 4, 5, 7.*


### Research and primary sources

**[5]** Anthropic. Labor market impacts of AI: A new measure and early evidence, 5 March 2026. https://www.anthropic.com/research/labor-market-impacts  
Compares theoretical LLM capability with observed usage across occupations, the basis of the adoption-gap argument. Section 2. *Used in: lab 2.*

**[6]** Liu, N. F., Lin, K., Hewitt, J., Paranjape, A., Bevilacqua, M., Petroni, F., Liang, P. “Lost in the Middle: How Language Models Use Long Contexts.” Transactions of the ACL 12 (2024): 157–173. https://arxiv.org/abs/2307.03172  
Shows that models use information at the start and end of a long context better than information in the middle. Section 11. *Used in: lab 11.*

**[7]** Rumbelow, J., Watkins, M. “SolidGoldMagikarp (plus, prompt generation).” LessWrong, February 2023. https://www.lesswrong.com/posts/aPeJE8bSo6rAFoLqg  
The original write-up of glitch (anomalous) tokens in GPT models. Section 9. *Used in: lab 9.*

**[8]** Kalai, A. T., Nachum, O., Vempala, S. S., Zhang, E. “Why Language Models Hallucinate.” arXiv:2509.04664, September 2025. https://arxiv.org/abs/2509.04664. Plain-language summary: https://openai.com/index/why-language-models-hallucinate/  
Argues that training and evaluation reward guessing over admitting uncertainty. Section 10. *Used in: lab 10.*

**[9]** OpenAI. Where the goblins came from, 29 April 2026. https://openai.com/index/where-the-goblins-came-from/  
The provider’s own account of how a personality-training reward spread an odd habit across model outputs. Section 14. *Used in: lab 14.*

**[10]** Zou, A., Wang, Z., Carlini, N., Nasr, M., Kolter, J. Z., Fredrikson, M. “Universal and Transferable Adversarial Attacks on Aligned Language Models.” arXiv:2307.15043, 2023. https://arxiv.org/abs/2307.15043  
Optimized adversarial suffixes (GCG) that transfer from open models to closed ones. Section 18. *Used in: lab 18.*

**[11]** Russinovich, M., Salem, A., Eldan, R. “Great, Now Write an Article About That: The Crescendo Multi-Turn LLM Jailbreak Attack.” USENIX Security 2025; arXiv:2404.01833. https://arxiv.org/abs/2404.01833  
Gradual, multi-turn jailbreaks built from benign-looking messages, and why single-message filters miss them. Section 18. *Used in: lab 18.*

**[12]** Anthropic. Prompt caching (API documentation). https://platform.claude.com/docs/en/docs/build-with-claude/prompt-caching  
How reusing an unchanged prompt prefix cuts input cost and latency. Section 17. *Used in: lab 17.*


### Further reading (arXiv links, not re-opened while preparing this guide)

**[13]** Greshake, K., et al. “Not what you’ve signed up for: Compromising Real-World LLM-Integrated Applications with Indirect Prompt Injection.” arXiv:2302.12173, 2023. https://arxiv.org/abs/2302.12173  
Indirect prompt injection through retrieved documents and tools. Sections 6–8. *Used in: labs 6-8.*

**[14]** Wei, A., Haghtalab, N., Steinhardt, J. “Jailbroken: How Does LLM Safety Training Fail?” arXiv:2307.02483, 2023. https://arxiv.org/abs/2307.02483  
Why safety training leaves gaps that jailbreaks exploit. Sections 15, 18. *Used in: labs 13, 15, 18.*

**[15]** Hubinger, E., et al. “Sleeper Agents: Training Deceptive LLMs that Persist Through Safety Training.” arXiv:2401.05566, 2024. https://arxiv.org/abs/2401.05566  
Backdoored models that behave normally until a trigger appears. Section 3. *Used in: labs 3, 13.*

**[16]** Ouyang, L., et al. “Training language models to follow instructions with human feedback.” arXiv:2203.02155, 2022. https://arxiv.org/abs/2203.02155  
The standard description of the SFT plus RLHF pipeline. Section 13. *Used in: lab 13.*
