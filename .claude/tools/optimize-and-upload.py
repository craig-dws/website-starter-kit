#!/usr/bin/env python3
"""
optimize-and-upload.py

Resize and compress an image, then upload it to the WordPress Media Library via the
REST API (POST /wp-json/wp/v2/media) using an Application Password.

This is the SAFE upload path. It is scoped to media only: it creates an image
attachment, exactly as a human does in wp-admin > Add Media. It does NOT use the
dangerous file-write / shell / php-eval abilities and cannot run code or write
arbitrary files on the server.

Credentials: by default it reads the site URL, username and Application Password
straight from your local Claude config (~/.claude.json), where `claude mcp add`
already stored them for this project. So there is nothing to set up. If you prefer,
set WP_SITE_URL (or WP_API_URL), WP_API_USERNAME and WP_API_PASSWORD in the
environment and those override the config. The password is never read from or
written to the repo.

Usage:
  # optimise only (no creds needed), overwrite the file in place:
  python optimize-and-upload.py IMAGE --in-place --optimize-only

  # optimise and upload, return the media id and URL:
  python optimize-and-upload.py IMAGE --max-width 1600 --alt "..." --title "..."

  # update metadata on an existing attachment (no upload):
  python optimize-and-upload.py --update 431 --alt "..." --description "..."

Notes:
  --max-width caps the width (contained images ~1600, full-width heroes ~2500).
  Format is preserved: images with transparency stay PNG, everything else becomes JPEG.
  WebP Express converts to WebP on the server, so do not pre-convert; just size it right.
"""
import argparse, io, os, sys
from urllib.parse import urlparse


def derive_base(api_url):
    if not api_url:
        return None
    p = urlparse(api_url)
    return f"{p.scheme}://{p.netloc}" if p.scheme and p.netloc else None


def creds_from_claude_config():
    """Read WP credentials from ~/.claude.json, where `claude mcp add` stored them.
    Prefers the MCP server whose project path matches the current directory.
    Returns (wp_api_url, username, password) or None."""
    path = os.path.expanduser("~/.claude.json")
    if not os.path.exists(path):
        return None
    import json
    try:
        data = json.load(open(path, encoding="utf-8"))
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

    candidates.sort(key=lambda t: score(t[0]), reverse=True)
    env = candidates[0][1]
    return env.get("WP_API_URL"), env.get("WP_API_USERNAME"), env.get("WP_API_PASSWORD")


def resolve_credentials():
    base = os.environ.get("WP_SITE_URL") or derive_base(os.environ.get("WP_API_URL"))
    user = os.environ.get("WP_API_USERNAME")
    pw = os.environ.get("WP_API_PASSWORD")
    if base and user and pw:
        return base, user, pw
    cfg = creds_from_claude_config()
    if cfg:
        c_api, c_user, c_pw = cfg
        base = base or derive_base(c_api)
        user = user or c_user
        pw = pw or c_pw
    return base, user, pw


def optimize(path, max_width, quality):
    from PIL import Image
    im = Image.open(path)
    has_alpha = im.mode in ("RGBA", "LA") or (im.mode == "P" and "transparency" in im.info)
    w, h = im.size
    if w > max_width:
        h = round(h * max_width / w)
        im = im.resize((max_width, h), Image.LANCZOS)
    buf = io.BytesIO()
    if has_alpha:
        im = im.convert("RGBA")
        im.save(buf, "PNG", optimize=True)
        ext, mime = ".png", "image/png"
    else:
        im = im.convert("RGB")
        im.save(buf, "JPEG", quality=quality, optimize=True, progressive=True)
        ext, mime = ".jpg", "image/jpeg"
    buf.seek(0)
    return buf, im.size, ext, mime


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("image", nargs="?")
    ap.add_argument("--max-width", type=int, default=1600)
    ap.add_argument("--quality", type=int, default=82)
    ap.add_argument("--alt", default="")
    ap.add_argument("--title", default="")
    ap.add_argument("--caption", default="")
    ap.add_argument("--description", default="")
    ap.add_argument("--update", type=int, default=0,
                    help="update the metadata of an existing media id (no file upload)")
    ap.add_argument("--optimize-only", action="store_true")
    ap.add_argument("--in-place", action="store_true",
                    help="overwrite the source file with the optimised version")
    a = ap.parse_args()

    # Update-only mode: patch metadata on an existing attachment, no file upload.
    if a.update:
        import requests
        base, user, pw = resolve_credentials()
        if not (base and user and pw):
            sys.exit("no credentials found: run `claude mcp add` in this project, or set "
                     "WP_SITE_URL / WP_API_USERNAME / WP_API_PASSWORD")
        fields = {}
        if a.alt:
            fields["alt_text"] = a.alt
        if a.title:
            fields["title"] = a.title
        if a.caption:
            fields["caption"] = a.caption
        if a.description:
            fields["description"] = a.description
        if not fields:
            sys.exit("nothing to update: pass --alt / --title / --caption / --description")
        r = requests.post(f"{base}/wp-json/wp/v2/media/{a.update}", auth=(user, pw),
                          json=fields, timeout=60)
        if r.status_code not in (200, 201):
            sys.exit(f"update failed {r.status_code}: {r.text[:300]}")
        j = r.json()
        print(f"updated id={j.get('id')} alt={(j.get('alt_text') or '')[:80]!r}")
        return

    if not a.image:
        sys.exit("provide an image path, or use --update <id> with metadata fields")
    if not os.path.exists(a.image):
        sys.exit(f"not found: {a.image}")

    buf, (nw, nh), ext, mime = optimize(a.image, a.max_width, a.quality)
    kb = len(buf.getvalue()) // 1024
    print(f"optimised {os.path.basename(a.image)} -> {nw}x{nh} {kb}KB ({mime})")

    if a.in_place:
        with open(a.image, "wb") as f:
            f.write(buf.getvalue())
        buf.seek(0)

    if a.optimize_only:
        return

    import requests
    base, user, pw = resolve_credentials()
    if not (base and user and pw):
        sys.exit("no credentials found: run `claude mcp add` in this project so they are in "
                 "~/.claude.json, or set WP_SITE_URL / WP_API_USERNAME / WP_API_PASSWORD")

    filename = os.path.splitext(os.path.basename(a.image))[0] + ext
    url = base + "/wp-json/wp/v2/media"
    data = {}
    if a.title:
        data["title"] = a.title
    if a.alt:
        data["alt_text"] = a.alt
    if a.caption:
        data["caption"] = a.caption
    if a.description:
        data["description"] = a.description
    r = requests.post(url, auth=(user, pw),
                      files={"file": (filename, buf, mime)},
                      data=data, timeout=120)
    if r.status_code not in (200, 201):
        sys.exit(f"upload failed {r.status_code}: {r.text[:300]}")
    j = r.json()
    print(f"uploaded id={j.get('id')} url={j.get('source_url')}")


if __name__ == "__main__":
    main()
