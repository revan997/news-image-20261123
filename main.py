#!/usr/bin/env python3
"""news-image-20261123 entrypoint (Python 3.13, standard library only).

The entry image is the entry.png beside this file: a one-page newspaper
front page summing up Monday 23 November 2026's world news (COP31 collapses
in Antalya, tankers burn in the Strait of Hormuz, and six more stories),
drawn this session and checked at full size.

This program does three things, in order:
  1. reads entry.png and proves it is a whole, well-formed PNG of exactly
     1024x1024 pixels and at most 1 MiB (magic bytes, IHDR geometry, a CRC
     on every chunk, an IEND trailer, and no trailing bytes);
  2. copies it byte-for-byte to $MAKEFUN_OUTPUT_DIR/entry.png
     (default /output);
  3. reads the copy back and proves it again, so a bad write cannot slip
     through silently.

No network, no randomness, no dependencies: two runs write the same bytes.
"""

import binascii
import hashlib
import os
import struct
import sys
import zlib
from pathlib import Path

PNG_MAGIC = b"\x89PNG\r\n\x1a\n"
MAX_BYTES = 1_048_576
WANT_WIDTH = 1024
WANT_HEIGHT = 1024
# colour type 2 (truecolour RGB) at 8 bits per channel: 3 bytes per pixel.
_CHANNELS = {0: 1, 2: 3, 3: 1, 4: 2, 6: 4}


class EntryError(ValueError):
    """Raised when the entry image fails any whole-file check."""


def _chunks(data):
    """Yield (type, payload) for every chunk, verifying lengths and CRCs."""
    if data[:8] != PNG_MAGIC:
        raise EntryError("bad PNG magic bytes")
    pos = 8
    seen = []
    while pos < len(data):
        if pos + 8 > len(data):
            raise EntryError("truncated chunk header at offset %d" % pos)
        length = struct.unpack(">I", data[pos:pos + 4])[0]
        ctype = data[pos + 4:pos + 8]
        end = pos + 8 + length + 4
        if end > len(data):
            raise EntryError("truncated %s chunk" % ctype.decode("latin1"))
        payload = data[pos + 8:pos + 8 + length]
        stored_crc = struct.unpack(">I", data[pos + 8 + length:end])[0]
        actual_crc = binascii.crc32(ctype + payload) & 0xFFFFFFFF
        if stored_crc != actual_crc:
            raise EntryError("CRC mismatch in %s chunk" % ctype.decode("latin1"))
        seen.append((ctype, payload))
        pos = end
    if not seen or seen[0][0] != b"IHDR":
        raise EntryError("first chunk is not IHDR")
    if seen[-1][0] != b"IEND":
        raise EntryError("last chunk is not IEND")
    if pos != len(data):
        raise EntryError("trailing bytes after IEND")
    return seen


def check_image(data):
    """Validate the entry bytes; return (width, height) or raise EntryError."""
    if len(data) > MAX_BYTES:
        raise EntryError("file is %d bytes, over the 1 MiB limit" % len(data))
    if len(data) < 8 + 25:
        raise EntryError("file too short to be a PNG")
    chunks = _chunks(data)
    ihdr = chunks[0][1]
    if len(ihdr) != 13:
        raise EntryError("IHDR is %d bytes, expected 13" % len(ihdr))
    width, height, depth, ctype, comp, filt, interlace = struct.unpack(
        ">IIBBBBB", ihdr)
    if (width, height) != (WANT_WIDTH, WANT_HEIGHT):
        raise EntryError("image is %dx%d, expected 1024x1024"
                         % (width, height))
    if depth != 8 or ctype not in _CHANNELS:
        raise EntryError("unsupported bit depth %d / colour type %d"
                         % (depth, ctype))
    if comp != 0 or filt != 0:
        raise EntryError("unsupported compression/filter method")
    if interlace not in (0, 1):
        raise EntryError("unsupported interlace method %d" % interlace)
    if sum(1 for t, _ in chunks if t == b"IHDR") != 1:
        raise EntryError("more than one IHDR chunk")
    idat = b"".join(p for t, p in chunks if t == b"IDAT")
    if not idat:
        raise EntryError("no IDAT chunk")
    if interlace == 0:
        # A non-interlaced image's raw data is one filter byte plus one
        # row of pixels per scanline; prove the deflate stream is intact
        # and inflates to exactly that size.
        row_bytes = 1 + width * _CHANNELS[ctype] * depth // 8
        try:
            raw = zlib.decompress(idat)
        except zlib.error as exc:
            raise EntryError("IDAT data does not decompress: %s" % exc)
        if len(raw) != height * row_bytes:
            raise EntryError("decompressed image is %d bytes, expected %d"
                             % (len(raw), height * row_bytes))
    return width, height


def main():
    here = Path(__file__).resolve().parent
    src = here / "entry.png"
    if not src.is_file():
        print("entry.png not found beside main.py", file=sys.stderr)
        return 1
    data = src.read_bytes()
    try:
        width, height = check_image(data)
    except EntryError as exc:
        print("entry.png failed validation: %s" % exc, file=sys.stderr)
        return 1
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    out = out_dir / "entry.png"
    out.write_bytes(data)
    try:
        check_image(out.read_bytes())
    except EntryError as exc:
        print("written copy failed validation: %s" % exc, file=sys.stderr)
        return 1
    digest = hashlib.sha256(data).hexdigest()
    print("wrote %s (%d bytes, %dx%d, sha256 %s)"
          % (out, len(data), width, height, digest))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
