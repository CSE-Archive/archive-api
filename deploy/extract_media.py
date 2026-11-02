#!/usr/bin/env python3
"""Extract the CSE Archive backup zip produced by the old server.

The old server's zip stores non-ASCII (Persian) filenames as raw UTF-8 bytes
without the zip UTF-8 flag, so most unzip tools write mojibake names that no
longer match the paths stored in the database. This script re-decodes every
name (cp437 -> UTF-8) while extracting.

Usage:
    python3 extract_media.py <archive-backup.zip> [media_dest] [dump_dest]

Defaults follow the canonical layout (README.md):
    media_dest = /opt/csearchive/data/media
    dump_dest  = /opt/csearchive/backups/temp.backup

The zip layout is:
    archive-backup/repos/archive-api/media/**   -> media files (MEDIA_ROOT)
    archive-backup/temp.backup                  -> postgres custom-format dump
"""

import os
import sys
import zipfile

MEDIA_PREFIX = "archive-backup/repos/archive-api/media/"
DUMP_ENTRY = "archive-backup/temp.backup"


def fixed_name(name: str) -> str:
    try:
        return name.encode("cp437").decode("utf-8")
    except (UnicodeEncodeError, UnicodeDecodeError):
        return name


def main() -> int:
    if len(sys.argv) < 2:
        print(__doc__, file=sys.stderr)
        return 2
    zip_path = sys.argv[1]
    media_root = sys.argv[2] if len(sys.argv) > 2 else "/opt/csearchive/data/media"
    dump_dest = sys.argv[3] if len(sys.argv) > 3 else "/opt/csearchive/backups/temp.backup"

    z = zipfile.ZipFile(zip_path)
    os.makedirs(media_root, exist_ok=True)
    os.makedirs(os.path.dirname(dump_dest), exist_ok=True)

    count, total = 0, 0
    for info in z.infolist():
        name = info.filename
        if name.startswith(MEDIA_PREFIX) and not name.endswith("/"):
            dest = os.path.join(media_root, fixed_name(name[len(MEDIA_PREFIX):]))
            os.makedirs(os.path.dirname(dest), exist_ok=True)
            with z.open(info) as src, open(dest, "wb") as out:
                while chunk := src.read(1 << 20):
                    out.write(chunk)
            count += 1
            total += info.file_size
            if count % 1000 == 0:
                print(f"  {count} files, {total / 1e9:.2f} GB", flush=True)
        elif name == DUMP_ENTRY:
            with z.open(info) as src, open(dump_dest, "wb") as out:
                while chunk := src.read(1 << 20):
                    out.write(chunk)
            print(f"dump extracted: {dump_dest} ({info.file_size} bytes)")

    print(f"media: {count} files, {total / 1e9:.2f} GB -> {media_root}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
