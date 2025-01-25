import sys
import subprocess

cache = {}


class OnePass:
    def __init__(self, url):
        self.url = url

    def __repr__(self):
        if __xonsh__.env.get("ONEPASS_ENABLED", False):
            if self.url not in cache:
                result = subprocess.run(
                    ["op", "read", "op://" + self.url], capture_output=True, text=True
                )
                print(
                    "Your 1Password environmental secret "
                    f"{self.url} is live in your environment", file=sys.stderr
                )
                cache[self.url] = result.stdout.strip()
            return cache[self.url]
        else:
            if self.url in cache:
                print(
                    "Your 1Password environmental secret "
                    f"{self.url} is no longer in your environment", file=sys.stderr
                )
                del cache[self.url]
            return ""
