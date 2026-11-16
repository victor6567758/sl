"""Untrusted 'agent-written' code used by lab 21b. It only PROBES what the sandbox allows; it does nothing harmful."""
import os
import urllib.request


def probe(name, action):
    """Run one action and print whether the sandbox allowed it."""
    try:
        print(f"{name:12} ALLOWED  {str(action())[:50]}", flush=True)
    except Exception as e:  # noqa: BLE001
        print(f"{name:12} BLOCKED  {type(e).__name__}", flush=True)


def network():
    return urllib.request.urlopen("http://example.com", timeout=3).status


def read_shadow():
    return open("/etc/shadow").read()


def write_root():
    return open("/etc/pwned", "w").write("x")


def write_work():
    return open("/work/ok.txt", "w").write("x")


def memory_hog():
    return bytearray(2 * 1024 ** 3)      # last: may get the whole process killed (exit 137)


probe("network", network)
probe("read_shadow", read_shadow)
probe("write_root", write_root)
probe("write_work", write_work)
probe("uid", os.getuid)
probe("memory_hog", memory_hog)
