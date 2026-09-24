#!/usr/bin/env python3
"""
optimize-and-upload.py

Resize and compress an image, then upload it to the WordPress Media Library via the
REST API (POST /wp-json/wp/v2/media) using an Application Password.

This is the SAFE upload path. It is scoped to media only: it creates an image
attachment, exactly as a human does in wp-admin > Add Media. It does NOT use the
dangerous file-write / shell / php-eval abilities and cannot run code or write
arbitrary files on the server.

Credentials: read from wherever this project's connection file (.claude/connections/)
says they live, through wp_credentials.py beside this script: the environment, then
.claude/settings.local.json (the WordPress REST connection), then your local Claude
config (~/.claude.json), where `claude mcp add` stored them for an MCP or bridge
connection. So there is nothing to set up once the site is connected. The password is
never read from or written to the repo.

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

from wp_credentials import WHERE, resolve_credentials


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
            sys.exit(WHERE)
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
        sys.exit(WHERE)

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
