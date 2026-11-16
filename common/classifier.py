"""Open-source prompt-injection classifier (small DeBERTa model) used in Labs 12b, 15, 18."""
import os

_clf = None


def clf():
    global _clf
    if _clf is None:
        from transformers import pipeline
        _clf = pipeline(
            "text-classification",
            model=os.getenv("AISEC_INJ_MODEL", "protectai/deberta-v3-base-prompt-injection-v2"),
            truncation=True, max_length=512,
        )
    return _clf


def flag(text):
    """True if the classifier labels the text as a prompt injection."""
    return clf()(text[:4000])[0]["label"] == "INJECTION"
