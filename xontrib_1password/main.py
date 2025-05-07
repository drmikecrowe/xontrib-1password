import subprocess
import sys

if not __xonsh__.imp.shutil.which("op"):  # type: ignore
    print(
        "xontrib-1password: OnePassword CLI tool not found. Install: https://developer.1password.com/docs/cli/get-started/",
        file=sys.stderr,
    )

_loaded = False
_urls = []
_1password_cache = {}
_1password_notified = {}


class OnePass:
    def __init__(self, url):
        global _urls
        self.url = url
        _urls.append(url)

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        global __xonsh__
        global _loaded
        global _urls
        env = __xonsh__.env  # type: ignore

        if env.get("ONEPASS_ENABLED", False):
            if not _loaded:
                if env.get("XONTRIB_1PASSWORD_DEBUG", False):
                    print(f"[xontrib-1password] DEBUG: Loading secrets from 1Password")
                tpl = [f"{k[5:]}={k}" for k in _urls]
                open("/tmp/onepass.env", "w").write("\n".join(tpl))
                result = subprocess.run(
                    ["op", "inject", "-i", "/tmp/onepass.env"],
                    capture_output=True,
                    text=True,
                )
                lines = result.stdout.split("\n")
                for line in lines:
                    if "=" not in line:
                        continue
                    first_eq = line.index("=")
                    key = "op://" + line[:first_eq]
                    if key not in _1password_cache:
                        _1password_cache[key] = line[first_eq + 1 :]
                        _1password_notified[key] = False
                    elif env.get("XONTRIB_1PASSWORD_DEBUG", False):
                        print(f"[xontrib-1password] ERROR: Skipping {line}")
                _loaded = True

            if self.url not in _1password_cache:
                result = subprocess.run(
                    ["op", "read", self.url], capture_output=True, text=True
                )
                key = result.stdout.strip()
                _1password_cache[self.url] = key
            if (
                env.get("XONTRIB_1PASSWORD_DEBUG", False)
                and not _1password_notified[self.url]
            ):
                print(
                    "[xontrib-1password] Your 1Password environmental secret "
                    f"{self.url} is live in your environment",
                    file=sys.stderr,
                )
                _1password_notified[self.url] = True
            return _1password_cache[self.url]
        else:
            if self.url in _1password_cache:
                if env.get("XONTRIB_1PASSWORD_DEBUG", False):
                    print(
                        "[xontrib-1password] Your 1Password environmental secret "
                        f"{self.url} is no longer in your environment",
                        file=sys.stderr,
                    )
                del _1password_cache[self.url]
            return ""
