import subprocess

from xonsh.built_ins import __xonsh__


class OnePass:
    def __init__(self, url):
        self.url = url
        self.cache = None

    def __repr__(self):
        if __xonsh__.env.get("ONEPASS_ENABLED", False):
            if not self.cache:
                result = subprocess.run(
                    ["op", "read", "op://" + self.url], capture_output=True, text=True
                )
                print(
                    "Your 1Password environmental secret "
                    f"{self.url} is live in your environment"
                )
                self.cache = result.stdout.strip()
            return self.cache
        else:
            if self.cache:
                print(
                    "Your 1Password environmental secret "
                    f"{self.url} is no longer in your environment"
                )
                self.cache = None
            return ""
