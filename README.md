<p align="center">
1password support for xonsh
</p>

<p align="center">
If you like the idea click ⭐ on the repo and <a href="https://twitter.com/intent/tweet?text=Nice%20xontrib%20for%20the%20xonsh%20shell!&url=https://github.com/drmikecrowe/xontrib-1password" target="_blank">tweet</a>.
</p>

> **ALPHA**:  This is the initial release.  Issues/pull requests are welcome.

## Introduction

This xontrib adds support for 1Password secrets to the xonsh shell by utilizing the [op (1password CLI)][https://developer.1password.com/docs/cli/]. It works by allowing you to securely store and access your passwords in 1Password. To use:

1. Store your passwords in 1Password.
2. In your xonsh environment, reference the passwords using the OnePass function:
```xsh
$OPENAI_API_KEY = OnePass("op://Private/OpenAI-API-Key/api-key")
```
3. To expose the variables in your environment, set:
```xsh
$ONEPASS_ENABLED = 1
```

This approach ensures your sensitive information remains secure while being easily accessible in your xonsh shell.  The URL is basically: `op://<Vault>/<title>/<field>`.  To find this, here's the commands I used to determine these fields:

```sh
➜  xonsh op item list --format json | jq '.[].title | select(. | contains("OpenAI"))' 
"OpenAI-API-Key"
➜  xonsh op item get OpenAI-API-Key --format json | jq '.fields[] | select(.type == "CONCEALED") | .label'
"api-key"
```

## Installation

To install use pip:

```xsh
xpip install xontrib-1password
# or: xpip install -U git+https://github.com/drmikecrowe/xontrib-1password
```

## Usage


This xontrib will get loaded automatically for interactive sessions.
To stop this, set

```xsh
$XONTRIBS_AUTOLOAD_DISABLED = ["1password", ]
# if you have set this for other xontribs, you should append the vale
```


## Examples

![Example](./1password-example.png)

## Known issues

None

## Development

- activate [pre-commit](https://github.com/pre-commit/pre-commit) hooks
```sh
# install pre-commit plugins and activate the commit hook
pre-commit install
pre-commit autoupdate
```


## Releasing your package

- Bump the version of your package.
- Create a GitHub release (The release notes are automatically generated as a draft release after each push).
- And publish with `poetry publish --build` or `twine`

## Credits

This package was created with [xontrib template](https://github.com/xonsh/xontrib-template).

