#!/usr/bin/env python3
"""
create-post.py

Create, read, snapshot or update a WordPress post or page via the REST API
(/wp-json/wp/v2/<rest_base>) using an Application Password.

This is the SAFE, scoped path, the same shape as optimize-and-upload.py. It creates a post
exactly as a human does in wp-admin, and cannot run code or write arbitrary files. It does
NOT use the dangerous shell / php-eval / file-write abilities.

A blog post is content, not layout: the single-post TEMPLATE (built via prompts/blog.md)
renders it. So for a blog post this only sets the post's fields (title, body, excerpt, slug,
category, featured image); the design comes from the template, not from a per-post layout.

On a WordPress block theme the body IS the layout (block markup), so the same calls read and
write a page's layout. That is the WordPress REST connection (.claude/connections/wordpress-rest.md).

Credentials: read from wherever this project's connection file says they live, through
wp_credentials.py beside this script: the environment, then .claude/settings.local.json, then
~/.claude.json (where `claude mcp add` stored them). The password is never read from or written
to the repo.

Usage:
  # which site and user is this connected as? (read-only)
  python create-post.py --whoami

  # create a DRAFT post from a body file (new posts default to draft, so nothing goes live by
  # accident):
  python create-post.py --title "What to expect from cataract surgery" \
      --slug cataract-surgery-what-to-expect --content-file body.html \
      --excerpt "A plain guide to the day." --category 5 --featured 512

  # publish it when it is ready:
  python create-post.py --title "..." --content-file body.html --status publish

  # read a page's raw block markup (needs the password; the public page has the block comments
  # stripped):
  python create-post.py --rest-base pages --read 42

  # snapshot a page to build-log/snapshots/ before changing it:
  python create-post.py --rest-base pages --snapshot 42

  # update an existing post or page. A snapshot is taken first, automatically, and the update
  # is refused if it cannot be. Status, slug and title are left alone unless passed:
  python create-post.py --rest-base pages --update 42 --content-file body.html

  # put a snapshot back (snapshots the current state first):
  python create-post.py --restore build-log/snapshots/pages-42-divorce-20260924-101500.json

  # a custom post type: pass its REST base, read from <site>/wp-json/wp/v2/types:
  python create-post.py --rest-base resources --title "..." --content-file body.html

Notes:
  A new post defaults to draft. Pass --status publish when it is ready to be live on staging.
  An update never changes the status unless --status is passed, so a published page stays published.
  content is stored as the post body HTML. Pass real HTML (paragraphs, headings), not markdown;
  on a block theme, pass block markup.
  category and featured take numeric IDs. featured sets the post's featured image (featured_media).
  A custom post type must be REST-enabled (show_in_rest); standard posts already are.
"""
import argparse, json, os, re, sys
from datetime import datetime

from wp_credentials import WHERE, project_dir, resolve_credentials


def api(base, rest_base, item=None):
    url = f"{base}/wp-json/wp/v2/{rest_base}"
    return f"{url}/{item}" if item not in (None, "") else url


def fetch_edit(requests, base, auth, rest_base, item):
    """The stored post, including raw block markup. Needs authentication."""
    r = requests.get(api(base, rest_base, item), auth=auth, params={"context": "edit"}, timeout=60)
    if r.status_code != 200:
        sys.exit(f"read failed {r.status_code}: {r.text[:300]}")
    return r.json()


def raw(field):
    return field.get("raw", field.get("rendered", "")) if isinstance(field, dict) else (field or "")


def snapshot(requests, base, auth, rest_base, item):
    """Save the stored post to build-log/snapshots/ and return the file path."""
    j = fetch_edit(requests, base, auth, rest_base, item)
    snap = {
        "site": base,
        "rest_base": rest_base,
        "id": j.get("id", item),
        "slug": j.get("slug"),
        "status": j.get("status"),
        "link": j.get("link"),
        "modified": j.get("modified"),
        "title": raw(j.get("title")),
        "content": raw(j.get("content")),
        "taken": datetime.now().isoformat(timespec="seconds"),
    }
    folder = os.path.join(project_dir(), "build-log", "snapshots")
    os.makedirs(folder, exist_ok=True)
    safe = re.sub(r"[^A-Za-z0-9_-]+", "-", f"{rest_base}-{snap['id']}-{snap['slug'] or ''}").strip("-")
    stem = os.path.join(folder, f"{safe}-{datetime.now():%Y%m%d-%H%M%S}")
    path, n = f"{stem}.json", 2
    while os.path.exists(path):  # never overwrite an earlier snapshot taken in the same second
        path, n = f"{stem}-{n}.json", n + 1
    with open(path, "x", encoding="utf-8") as f:
        json.dump(snap, f, ensure_ascii=False, indent=2)
    return path


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--title", default="")
    ap.add_argument("--content", default="", help="post body HTML (or use --content-file)")
    ap.add_argument("--content-file", default="", help="read the post body from this file")
    ap.add_argument("--excerpt", default="")
    ap.add_argument("--slug", default="")
    ap.add_argument("--status", default=None,
                    choices=["draft", "publish", "pending", "private"],
                    help="new posts default to draft; an update leaves the status alone unless passed")
    ap.add_argument("--category", default="", help="comma-separated category IDs")
    ap.add_argument("--featured", type=int, default=0, help="featured image media id")
    ap.add_argument("--rest-base", default="posts",
                    help="REST base for the post type (posts, pages, or a CPT's rest_base)")
    ap.add_argument("--update", type=int, default=0,
                    help="update an existing post id instead of creating (snapshots it first)")
    ap.add_argument("--whoami", action="store_true",
                    help="print the site and user this credential reaches, and write nothing")
    ap.add_argument("--read", default="", help="print the raw stored body of this id")
    ap.add_argument("--snapshot", default="", help="save this id to build-log/snapshots/")
    ap.add_argument("--restore", default="", help="write a snapshot file's title and body back")
    a = ap.parse_args()

    import requests
    base, user, pw = resolve_credentials()
    if not (base and user and pw):
        sys.exit(WHERE)
    auth = (user, pw)

    if a.whoami:
        site = requests.get(f"{base}/wp-json/", timeout=60)
        if site.status_code != 200:
            sys.exit(f"site index failed {site.status_code}: {site.text[:300]}")
        s = site.json()
        me = requests.get(api(base, "users", "me"), auth=auth, params={"context": "edit"},
                          timeout=60)
        if me.status_code == 200:
            who = me.json().get("username") or me.json().get("slug")
        else:
            who = f"NOT AUTHENTICATED ({me.status_code})"
        print(f"site name: {s.get('name')}\nsite address: {s.get('url')}\n"
              f"home address: {s.get('home')}\nlogged in as: {who}")
        return

    if a.read:
        print(raw(fetch_edit(requests, base, auth, a.rest_base, a.read).get("content")))
        return

    if a.snapshot:
        print(f"snapshot saved: {snapshot(requests, base, auth, a.rest_base, a.snapshot)}")
        return

    if a.restore:
        with open(a.restore, encoding="utf-8") as f:
            snap = json.load(f)
        if snap.get("site", "").rstrip("/") != base.rstrip("/"):
            sys.exit(f"refused: the snapshot is from {snap.get('site')}, but this credential "
                     f"reaches {base}")
        before = snapshot(requests, base, auth, snap["rest_base"], snap["id"])
        print(f"current state saved first: {before}")
        r = requests.post(api(base, snap["rest_base"], snap["id"]), auth=auth,
                          json={"title": snap["title"], "content": snap["content"]}, timeout=120)
        if r.status_code not in (200, 201):
            sys.exit(f"restore failed {r.status_code}: {r.text[:400]}")
        j = r.json()
        print(f"restored id={j.get('id')} status={j.get('status')} slug={j.get('slug')} "
              f"link={j.get('link')}")
        return

    body = a.content
    if a.content_file:
        if not os.path.exists(a.content_file):
            sys.exit(f"not found: {a.content_file}")
        body = open(a.content_file, encoding="utf-8").read()

    fields = {}
    if a.status or not a.update:
        fields["status"] = a.status or "draft"
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

    if a.update:
        if not fields:
            sys.exit("nothing to update: pass --content-file, --title or another field")
        # No snapshot, no overwrite. fetch_edit exits if the post cannot be read.
        print(f"snapshot saved: {snapshot(requests, base, auth, a.rest_base, a.update)}")
    elif not a.title:
        sys.exit("a new post needs at least --title")

    r = requests.post(api(base, a.rest_base, a.update or None), auth=auth, json=fields, timeout=120)
    if r.status_code not in (200, 201):
        sys.exit(f"{'update' if a.update else 'create'} failed {r.status_code}: {r.text[:400]}")
    j = r.json()
    print(f"{'updated' if a.update else 'created'} id={j.get('id')} status={j.get('status')} "
          f"slug={j.get('slug')} link={j.get('link')}")


if __name__ == "__main__":
    main()
