# Security Policy

## Supported versions

This kit is developed on `master`. Security fixes are applied to `master` and included in
the next tagged release. Older tags are not maintained.

## Reporting a vulnerability

Please report suspected vulnerabilities **privately** via GitHub Security Advisories
("Report a vulnerability") on the repository:

  https://github.com/parkwoo/wawoo-skills/security/advisories/new

If you cannot use advisories, open a minimal issue asking for a private channel — **do not**
include exploit details, secrets, or personal data in public issues.

Include, where possible:
- affected version / commit,
- the component (e.g. `mcp/server.py`, a skill, an install script),
- reproduction steps and impact,
- any suggested remediation.

## Scope and expectations

- This kit runs locally; the MCP server is a stdio process. Treat MCP inputs/outputs as
  untrusted when wiring it into other tools.
- Do not test against systems you do not own or have permission to test. No denial-of-service,
  no data exfiltration, no social engineering.
- We aim to acknowledge reports within a reasonable time and will credit reporters who wish
  to be named.

## Secrets

Do not commit secrets. `memory_save` rejects common secret patterns, and `scripts/validate_assets.py`
scans `docs/memory/` for them. Report any secret that appears to be committed so it can be removed
and rotated.
