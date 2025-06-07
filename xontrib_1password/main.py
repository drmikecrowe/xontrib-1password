import subprocess
import sys

from xontrib_1password import __version__

if not __xonsh__.imp.shutil.which("op"):  # type: ignore
    print(
        "xontrib-1password: OnePassword CLI tool not found. Install: https://developer.1password.com/docs/cli/get-started/",
        file=sys.stderr,
    )


_1password_cache = {}
_urls = {}
_notifications = set()


class OnePass:
    def __init__(self, url):
        global _urls
        self.url = url
        self.notified = False
        self.active = False
        _urls[url.replace("op://", "")] = url

    def __str__(self):
        return self.__repr__()

    def enabled(self):
        enabled = __xonsh__.env.get("XONTRIB_1PASSWORD_ENABLED", False)  # type: ignore
        return enabled

    def cache_mode(self):
        mode = self.enabled() and __xonsh__.env.get(
            "XONTRIB_1PASSWORD_CACHE", "not_empty"
        )  # type: ignore
        return mode

    def no_cache_mode(self):
        return self.cache_mode() in ["off", False]

    def log(self, *args, **kwargs):
        if self.enabled() and __xonsh__.env.get("XONTRIB_1PASSWORD_DEBUG", False):  # type: ignore
            print(*args, **kwargs, file=sys.stderr)

    def log_once(self, *args, **kwargs):
        global _notifications
        if not __xonsh__.env.get("XONTRIB_1PASSWORD_ENABLED", False):  # type: ignore
            return
        msg = " ".join(args)
        if msg not in _notifications:
            _notifications.add(msg)
            self.log(msg)

    def all_unloaded_secrets(self):
        """
        Returns a dictionary of all 1password secrets that are not already in the cache.
        """
        global _1password_cache, _urls
        return {k: v for k, v in _urls.items() if k not in _1password_cache}

    def op_read(self) -> dict[str, str] | None:
        """
        Reads all secrets from 1password and returns a dictionary of them.
        We'll load all secrets from 1password since it's now a single call and there's no additional overhead.
        """
        todo = self.all_unloaded_secrets()
        if not todo:
            return {}
        tpl = [f"{k}={v}" for k, v in _urls.items()]
        with open("/tmp/onepass.env", "w") as f:
            f.write("\n".join(tpl))
        result = subprocess.run(
            ["op", "inject", "-i", "/tmp/onepass.env"],
            capture_output=True,
            text=True,
        )
        if result.stderr:
            print(
                f"xontrib-1password: (see /tmp/onepass.env) {result.stderr} ",
                file=sys.stderr,
            )
            return
        lines = result.stdout.strip().split("\n")
        results = {}
        for line in lines:
            if "=" not in line:
                continue
            first_eq = line.index("=")
            key = line[:first_eq]
            results[key] = line[first_eq + 1 :]
        return results

    def load_secrets(self):
        """
        Returns a dictionary of 1Password secrets. If cache_mode is enabled, values are
        persisted to a cache and reused rather than fetched from 1Password.
        """
        global _1password_cache

        todo = self.all_unloaded_secrets()
        if not self.enabled() or not todo:
            return
        self.log(f"xontrib-1password: {len(todo)} unloaded secrets")
        loaded_secrets = self.op_read()
        if loaded_secrets:
            self.log(f"Read {len(loaded_secrets)} results from 1password")
            for k, v in loaded_secrets.items():
                _1password_cache[k] = v

    def __repr__(self):
        global _1password_cache

        self.log_once(f"xontrib-1password: enabled: {__version__}")
        if not self.enabled():
            _1password_cache.clear()
            return self.url
        self.load_secrets()
        if not _1password_cache:
            return self.url
        key = self.url.replace("op://", "")
        if key not in _1password_cache:
            self.log(f"ERROR: can't find {key} in {_1password_cache.keys()}")
            return self.url
        value = _1password_cache.get(key, "")
        if self.no_cache_mode():
            self.log("xontrib-1password: cache disabled, clearing")
            _1password_cache.clear()
        if value:
            if not self.active:
                self.active = True
            return value
        else:
            if self.active:
                self.active = False
            return self.url
