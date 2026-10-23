"""
Chrome's MediaRecorder writes a fragmented MP4 whose header says nothing of its length, so players show the length
of the first fragment. This adds it, without touching the video: the total of the fragments' sample durations goes
into mvhd, tkhd and mdhd, and a mehd box (movie extends header) goes into mvex. Fragments address their data from
their own moof (default-base-is-moof), so the bytes added before them move nothing they point to.

    python3 tools/mp4_duration.py media/film.mp4
"""
import struct
import sys
from pathlib import Path


def boxes(buf: bytes, off: int, end: int):
    while off + 8 <= end:
        size, kind = struct.unpack(">I4s", buf[off:off + 8])
        yield kind.decode("latin1"), off, size
        off += size


def child(buf: bytes, parent: tuple, kind: str) -> tuple:
    return next(b for b in boxes(buf, parent[1] + 8, parent[1] + parent[2]) if b[0] == kind)


def main(path: Path) -> None:
    d = bytearray(path.read_bytes())
    top = list(boxes(d, 0, len(d)))
    moov = next(b for b in top if b[0] == "moov")
    mvhd, trak, mvex = child(d, moov, "mvhd"), child(d, moov, "trak"), child(d, moov, "mvex")
    tkhd, mdia = child(d, trak, "tkhd"), child(d, trak, "mdia")
    mdhd = child(d, mdia, "mdhd")
    assert d[mvhd[1] + 8] == d[tkhd[1] + 8] == d[mdhd[1] + 8] == 1, "expected version 1 headers"
    if any(b[0] == "mehd" for b in boxes(d, mvex[1] + 8, mvex[1] + mvex[2])):
        sys.exit("already has a mehd box")
    movie_scale = struct.unpack(">I", d[mvhd[1] + 28:mvhd[1] + 32])[0]
    media_scale = struct.unpack(">I", d[mdhd[1] + 28:mdhd[1] + 32])[0]

    end = 0
    for moof in (b for b in top if b[0] == "moof"):
        traf = child(d, moof, "traf")
        tfdt, trun = child(d, traf, "tfdt"), child(d, traf, "trun")
        base = struct.unpack(">Q", d[tfdt[1] + 12:tfdt[1] + 20])[0] if d[tfdt[1] + 8] == 1 \
            else struct.unpack(">I", d[tfdt[1] + 12:tfdt[1] + 16])[0]
        flags = struct.unpack(">I", d[trun[1] + 8:trun[1] + 12])[0] & 0xFFFFFF
        assert flags & 0x100, "sample durations expected in trun"
        count = struct.unpack(">I", d[trun[1] + 12:trun[1] + 16])[0]
        pos = trun[1] + 16 + (4 if flags & 0x1 else 0) + (4 if flags & 0x4 else 0)
        per = 4 * sum(bool(flags & f) for f in (0x100, 0x200, 0x400, 0x800))
        total = sum(struct.unpack(">I", d[pos + i * per:pos + i * per + 4])[0] for i in range(count))
        end = max(end, base + total)

    movie = round(end * movie_scale / media_scale)
    d[mvhd[1] + 32:mvhd[1] + 40] = struct.pack(">Q", movie)
    d[tkhd[1] + 36:tkhd[1] + 44] = struct.pack(">Q", movie)
    d[mdhd[1] + 32:mdhd[1] + 40] = struct.pack(">Q", end)
    mehd = struct.pack(">I4sI", 20, b"mehd", 1 << 24) + struct.pack(">Q", movie)
    at = mvex[1] + 8
    d[at:at] = mehd
    for box in (moov, mvex):
        d[box[1]:box[1] + 4] = struct.pack(">I", box[2] + len(mehd))
    path.write_bytes(bytes(d))
    print(f"{path.name}: {movie / movie_scale:.2f} s")


if __name__ == "__main__":
    main(Path(sys.argv[1]))
