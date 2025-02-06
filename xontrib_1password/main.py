import subprocess
import sys


if not __xonsh__.imp.shutil.which('op'):
    print('xontrib-1password: OnePassword CLI tool not found. Install: https://developer.1password.com/docs/cli/get-started/', file=sys.stderr)


_1password_cache = {}


class OnePass:
    def __init__(self, url):
        self.url = url
    
    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        if __xonsh__.env.get("XONTRIB_1PASSWORD_ENABLED", True):
            if self.url not in _1password_cache:
                result = subprocess.run(["op", "read", self.url], capture_output=True, text=True)
                key = result.stdout.strip()
                if result.stderr:
                    print(f"xontrib-1password error for {self.url!r}: {result.stderr}", file=sys.stderr)

                if __xonsh__.env.get("XONTRIB_1PASSWORD_DEBUG", False):
                    print(
                        "Your 1Password environmental secret "
                        f"{self.url} is live in your environment",
                        file=sys.stderr,
                    )
                _1password_cache[self.url] = key
            return _1password_cache[self.url]
        else:
            if self.url in _1password_cache:
                if __xonsh__.env.get("XONTRIB_1PASSWORD_DEBUG", False):
                    print(
                        "Your 1Password environmental secret "
                        f"{self.url} is no longer in your environment",
                        file=sys.stderr,
                    )
                del _1password_cache[self.url]
            return self.url
