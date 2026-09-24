"""
wp_credentials.py

Where a WordPress site credential comes from, for every tool in this folder.

The project's connection file (.claude/connections/<connection>.md) names where its credential
lives. The tools look in every place a connection file can name, in this order, and use the first
COMPLETE set (site, username and password together). They never mix a site from one place with a
password from another.

1. Environment variables WP_SITE_URL (or WP_API_URL), WP_API_USERNAME and WP_API_PASSWORD. Claude
   Code sets these from the `env` block of .claude/settings.local.json, which is where the
   WordPress REST connection keeps them.
2. That same `env` block, read straight from .claude/settings.local.json in the project, for when
   a tool runs outside a Claude session or the session started before the file was written.
3. The MCP record that `claude mcp add` wrote to ~/.claude.json, preferring the server registered
   for this project folder. The Breakdance native and bridge connections keep it there.

The password is never read from or written to a committed file.
"""
import json, os
from urllib.parse import urlparse

WHERE = ("no credentials found. The connection file in .claude/connections/ says where this "
         "project's credential lives: .claude/settings.local.json for the WordPress REST "
         "connection, or the local Claude config written by `claude mcp add` for an MCP or bridge "
         "connection. Or set WP_SITE_URL / WP_API_USERNAME / WP_API_PASSWORD.")


def derive_base(api_url):
    if not api_url:
        return None
    p = urlparse(api_url)
    return f"{p.scheme}://{p.netloc}" if p.scheme and p.netloc else None


def _from_env_map(env):
    base = (env.get("WP_SITE_URL") or derive_base(env.get("WP_API_URL")) or "").rstrip("/")
    user, pw = env.get("WP_API_USERNAME"), env.get("WP_API_PASSWORD")
    return (base, user, pw) if base and user and pw else None


def project_dir():
    """The project folder: CLAUDE_PROJECT_DIR if set, else the nearest folder holding .claude."""
    env_dir = os.environ.get("CLAUDE_PROJECT_DIR")
    if env_dir:
        return env_dir
    d = os.getcwd()
    while True:
        if os.path.isdir(os.path.join(d, ".claude")):
            return d
        parent = os.path.dirname(d)
        if parent == d:
            return os.getcwd()
        d = parent


def _from_settings_local():
    path = os.path.join(project_dir(), ".claude", "settings.local.json")
    if not os.path.exists(path):
        return None
    try:
        with open(path, encoding="utf-8") as f:
            return _from_env_map((json.load(f) or {}).get("env") or {})
    except Exception:
        return None


def _from_claude_config():
    """Read WP credentials from ~/.claude.json, where `claude mcp add` stored them.
    Prefers the MCP server whose project path matches the current directory."""
    path = os.path.expanduser("~/.claude.json")
    if not os.path.exists(path):
        return None
    try:
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
    except Exception:
        return None
    candidates = []  # (project_path_or_None, env)
    for _name, cfg in (data.get("mcpServers") or {}).items():
        env = (cfg or {}).get("env") or {}
        if env.get("WP_API_PASSWORD"):
            candidates.append((None, env))
    for proj, pcfg in (data.get("projects") or {}).items():
        for _name, cfg in ((pcfg or {}).get("mcpServers") or {}).items():
            env = (cfg or {}).get("env") or {}
            if env.get("WP_API_PASSWORD"):
                candidates.append((proj, env))
    if not candidates:
        return None
    norm = lambda s: os.path.normcase(os.path.abspath(s)).replace("\\", "/")
    cwd = norm(os.getcwd())

    def score(proj):
        if not proj:
            return 0
        p = norm(proj)
        return 2 if p == cwd else (1 if cwd.startswith(p) else 0)

    # A server registered for a DIFFERENT project folder is another client's site. Never use it:
    # falling back to it would write to the wrong site. Only this project's servers, or a
    # user-wide server with no project, qualify.
    usable = [(proj, env) for proj, env in candidates if not proj or score(proj) > 0]
    if not usable:
        return None
    usable.sort(key=lambda t: score(t[0]), reverse=True)
    return _from_env_map(usable[0][1])


def resolve_credentials():
    """Return (site_base_url, username, password), or (None, None, None) if none is complete."""
    for source in (lambda: _from_env_map(os.environ), _from_settings_local, _from_claude_config):
        found = source()
        if found:
            return found
    return None, None, None
