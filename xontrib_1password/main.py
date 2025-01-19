from xonsh.built_ins import XonshSession
import subprocess


class OnePass:
    def __init__(self, url):
        self.url = url
        self.cache = None

    def __repr__(self):
        if __xonsh__.env.get("ONEPASS_ENABLED", False):
            if not self.cache:
                result = subprocess.run(
                    ["op", "read", self.url], capture_output=True, text=True
                )
                print(
                    f"Your 1Password environmental secret {self.url} is live in your environment"
                )
                self.cache = result.stdout.strip()
            return self.cache
        else:
            if self.cache:
                print(
                    f"Your 1Password environmental secret {self.url} is no longer in your environment"
                )
                self.cache = None
            return self.url
