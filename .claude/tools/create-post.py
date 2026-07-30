#!/usr/bin/env python3
"""
create-post.py

Create (or update) a WordPress post via the REST API (POST /wp-json/wp/v2/<rest_base>)
using an Application Password.

This is the SAFE, scoped path, the same shape as optimize-and-upload.py. It creates a post
exactly as a human does in wp-admin, and cannot run code or write arbitrary files. It does
NOT use the dangerous shell / php-eval / file-write abilities.

A blog post is content, not layout: the single-post TEMPLATE (built via prompts/blog.md)
renders it. So this only sets the post's fields (title, body, excerpt, slug, category,
featured image); the design comes from the template, not from a per-post layout.

Credentials: reads the site URL, username and Application Password from ~/.claude.json
(where `claude mcp add` stored them for this project), exactly like optimize-and-upload.py.
Or set WP_SITE_URL / WP_API_USERNAME / WP_API_PASSWORD in the environment to override. The
password is never read from or written to the repo.

Usage:
  # create a DRAFT post from a body file (status defaults to draft, so nothing goes live by
  # accident):
  python create-post.py --title "What to expect from cataract surgery" \
      --slug cataract-surgery-what-to-expect --content-file body.html \
      --excerpt "A plain guide to the day." --category 5 --featured 512

  # publish it when it is ready:
  python create-post.py --title "..." --content-file body.html --status publish

  # update an existing post:
  python create-post.py --update 618 --content-file body.html

  # a custom post type: pass its REST base, confirmed with `wp post-type list`:
  python create-post.py --rest-base resources --title "..." --content-file body.html

Notes:
  Status defaults to draft. Pass --status publish when the post is ready to be live on staging.
  content is stored as the post body HTML. Pass real HTML (paragraphs, headings), not markdown.
  category and featured take numeric IDs. featured sets the post's featured image (featured_media).
  A custom post type must be REST-enabled (show_in_rest); standard posts already are.
"""
import argparse, os, sys
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


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--title", default="")
    ap.add_argument("--content", default="", help="post body HTML (or use --content-file)")
    ap.add_argument("--content-file", default="", help="read the post body from this file")
    ap.add_argument("--excerpt", default="")
    ap.add_argument("--slug", default="")
    ap.add_argument("--status", default="draft",
                    choices=["draft", "publish", "pending", "private"])
    ap.add_argument("--category", default="", help="comma-separated category IDs")
    ap.add_argument("--featured", type=int, default=0, help="featured image media id")
    ap.add_argument("--rest-base", default="posts",
                    help="REST base for the post type (posts, or a CPT's rest_base)")
    ap.add_argument("--update", type=int, default=0,
                    help="update an existing post id instead of creating")
    a = ap.parse_args()

    import requests
    base, user, pw = resolve_credentials()
    if not (base and user and pw):
        sys.exit("no credentials found: run `claude mcp add` in this project so they are in "
                 "~/.claude.json, or set WP_SITE_URL / WP_API_USERNAME / WP_API_PASSWORD")

    body = a.content
    if a.content_file:
        if not os.path.exists(a.content_file):
            sys.exit(f"not found: {a.content_file}")
        body = open(a.content_file, encoding="utf-8").read()

    fields = {"status": a.status}
    if a.title:
        fields["title"] = a.title
    if body:
        fields["content"] = body
    if a.excerpt:
        fields["excerpt"] = a.excerpt
    if a.slug:
        fields["slug"] = a.slug
    if a.category:
        fields["categories"] = [int(x) for x in a.category.split(",") if x.strip().isdigit()]
    if a.featured:
        fields["featured_media"] = a.featured

    endpoint = f"{base}/wp-json/wp/v2/{a.rest_base}"
    if a.update:
        endpoint += f"/{a.update}"
    elif not a.title:
        sys.exit("a new post needs at least --title")

    r = requests.post(endpoint, auth=(user, pw), json=fields, timeout=120)
    if r.status_code not in (200, 201):
        sys.exit(f"{'update' if a.update else 'create'} failed {r.status_code}: {r.text[:400]}")
    j = r.json()
    print(f"{'updated' if a.update else 'created'} id={j.get('id')} status={j.get('status')} "
          f"slug={j.get('slug')} link={j.get('link')}")


if __name__ == "__main__":
    main()
