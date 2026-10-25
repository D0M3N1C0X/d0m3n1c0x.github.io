"""
Chrome's MediaRecorder writes a fragmented MP4 whose header says nothing of its length, so players show the length
of the first fragment. This adds it, without touching the video: for each track, the end of its last sample (from the
fragments' tfdt and trun boxes) goes into tkhd and mdhd, the longest track into mvhd, and a mehd box (movie extends
header) goes into mvex.

Bytes are inserted before the fragments, so the script refuses any file whose fragments address data by absolute
offset (a tfhd base-data-offset, or no default-base-is-moof) or that carries an mfra index: those would break.

    python3 tools/mp4_duration.py media/film.mp4
"""
import struct
import sys
from pathlib import Path


def boxes(buf: bytes, off: int, end: int):
    """(type, offset, size, header length) for each box between off and end; sizes 0 (to the end) and 1 (64-bit)."""
    while off + 8 <= end:
        size, kind = struct.unpack(">I4s", buf[off:off + 8])
        head = 8
        if size == 1:
            size, head = struct.unpack(">Q", buf[off + 8:off + 16])[0], 16
        elif size == 0:
            size = end - off
        if size < head:
            raise ValueError(f"malformed box {kind!r} at {off}")
        yield kind.decode("latin1"), off, size, head
        off += size


def children(buf: bytes, box: tuple, kind: str) -> list[tuple]:
    _, off, size, head = box
    return [b for b in boxes(buf, off + head, off + size) if b[0] == kind]


def child(buf: bytes, box: tuple, kind: str) -> tuple:
    found = children(buf, box, kind)
    if not found:
        raise ValueError(f"no {kind} inside {box[0]} at {box[1]}")
    return found[0]


def full(buf: bytes, box: tuple) -> tuple[int, int, int]:
    """Version, flags and where the box's payload starts, for a full box."""
    _, off, _, head = box
    vf = struct.unpack(">I", buf[off + head:off + head + 4])[0]
    return vf >> 24, vf & 0xFFFFFF, off + head + 4


def main(path: Path) -> None:
    d = bytearray(path.read_bytes())
    top = list(boxes(d, 0, len(d)))
    kinds = {b[0] for b in top}
    if "moof" not in kinds:
        sys.exit(f"{path.name}: not a fragmented MP4, nothing to do")
    if "mfra" in kinds:
        sys.exit(f"{path.name}: has an mfra index with absolute offsets; refusing to insert bytes")
    moov = next(b for b in top if b[0] == "moov")
    mvhd, mvex = child(d, moov, "mvhd"), child(d, moov, "mvex")
    if children(d, mvex, "mehd"):
        sys.exit(f"{path.name}: already has a mehd box")
    v, _, p = full(d, mvhd)
    movie_scale = struct.unpack(">I", d[p + (16 if v else 8):p + (20 if v else 12)])[0]

    tracks = {}                                      # track_ID -> {tkhd, mdhd, scale, end}
    for trak in children(d, moov, "trak"):
        tkhd, mdhd = child(d, trak, "tkhd"), child(d, child(d, trak, "mdia"), "mdhd")
        tv, _, tp = full(d, tkhd)
        track_id = struct.unpack(">I", d[tp + (16 if tv else 8):tp + (20 if tv else 12)])[0]
        mv, _, mp = full(d, mdhd)
        scale = struct.unpack(">I", d[mp + (16 if mv else 8):mp + (20 if mv else 12)])[0]
        tracks[track_id] = {"tkhd": tkhd, "mdhd": mdhd, "scale": scale, "end": 0}

    for moof in (b for b in top if b[0] == "moof"):
        for traf in children(d, moof, "traf"):
            _, flags, tp = full(d, child(d, traf, "tfhd"))
            if flags & 0x1 or not flags & 0x20000:
                sys.exit(f"{path.name}: fragments use absolute data offsets; refusing to insert bytes")
            track = tracks[struct.unpack(">I", d[tp:tp + 4])[0]]
            default = None
            q = tp + 4 + (8 if flags & 0x1 else 0) + (4 if flags & 0x2 else 0)
            if flags & 0x8:
                default = struct.unpack(">I", d[q:q + 4])[0]
            fv, _, fp = full(d, child(d, traf, "tfdt"))
            base = struct.unpack(">Q" if fv else ">I", d[fp:fp + (8 if fv else 4)])[0]
            total = 0
            for trun in children(d, traf, "trun"):
                _, tflags, rp = full(d, trun)
                count = struct.unpack(">I", d[rp:rp + 4])[0]
                pos = rp + 4 + (4 if tflags & 0x1 else 0) + (4 if tflags & 0x4 else 0)
                per = 4 * sum(bool(tflags & f) for f in (0x100, 0x200, 0x400, 0x800))
                for i in range(count):
                    if tflags & 0x100:
                        total += struct.unpack(">I", d[pos + i * per:pos + i * per + 4])[0]
                    elif default is not None:
                        total += default
                    else:
                        sys.exit(f"{path.name}: no sample durations in the fragments")
            track["end"] = max(track["end"], base + total)

    movie = 0
    for track in tracks.values():
        in_movie = round(track["end"] * movie_scale / track["scale"])
        movie = max(movie, in_movie)
        tv, _, tp = full(d, track["tkhd"])
        if tv:
            d[tp + 24:tp + 32] = struct.pack(">Q", in_movie)
        else:
            d[tp + 16:tp + 20] = struct.pack(">I", in_movie)
        mv, _, mp = full(d, track["mdhd"])
        if mv:
            d[mp + 20:mp + 28] = struct.pack(">Q", track["end"])
        else:
            d[mp + 12:mp + 16] = struct.pack(">I", track["end"])
    if v:
        d[p + 20:p + 28] = struct.pack(">Q", movie)
    else:
        d[p + 12:p + 16] = struct.pack(">I", movie)

    mehd = struct.pack(">I4sI", 20, b"mehd", 1 << 24) + struct.pack(">Q", movie)
    at = mvex[1] + mvex[3]
    d[at:at] = mehd
    for box in (moov, mvex):
        if box[3] != 8:
            sys.exit(f"{path.name}: 64-bit {box[0]} size; not handled")
        d[box[1]:box[1] + 4] = struct.pack(">I", box[2] + len(mehd))
    path.write_bytes(bytes(d))
    print(f"{path.name}: {movie / movie_scale:.2f} s")


if __name__ == "__main__":
    main(Path(sys.argv[1]))
