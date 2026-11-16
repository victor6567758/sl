"""Client-side redaction before data leaves your machine (labs 16 and 21). Guide: Section 16 (Figure 44), Section 21 (ZDR != full protection).

Needs Presidio and its spaCy model:  python -m spacy download en_core_web_lg
Presidio finds names, e-mails, phones, cards (NER + patterns); the regex adds AWS keys, which Presidio does not know.
Whatever neither catches (passport numbers, passwords, internal project names) goes out in clear text - lab 16a measures that.
"""
import re

_engines = None


def _load(passport):
    global _engines
    if _engines is None or _engines[2] != passport:
        from presidio_analyzer import AnalyzerEngine, Pattern, PatternRecognizer
        from presidio_anonymizer import AnonymizerEngine
        an = AnalyzerEngine()
        if passport:   # optional custom recognizer: one letter followed by seven digits
            an.registry.add_recognizer(PatternRecognizer(supported_entity="PASSPORT", patterns=[Pattern("passport", r"\b[A-Z]\d{7}\b", 0.6)]))
        _engines = (an, AnonymizerEngine(), passport)
    return _engines


def redact(text, passport=False):
    an, anon, _ = _load(passport)
    text = re.sub(r"AKIA[0-9A-Z]{16}", "<AWS_KEY>", text)
    return anon.anonymize(text=text, analyzer_results=an.analyze(text=text, language="en")).text
