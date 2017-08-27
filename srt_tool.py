#!/usr/bin/env python3

import sys
import re

rt = re.compile("""(\d{2}):(\d{2}):(\d{2}),(\d{3})""")

def get_seconds(time_str):
    sec = 0
    for p in time_str.split(":"):
        sec = sec * 60 + int(p)
    return sec

def s2t(s):
    m = rt.match(s).groups()
    return ((int(m[0]) * 60 + int(m[1])) * 60 + int(m[2])) * 1000 + int(m[3])

def t2s(t):
    micro_second = t % 1000
    second = int(t / 1000) % 60
    minute = int(t / 60 / 1000) % 60
    hour = int(t / 60 / 60 / 1000)
    return "{0:02d}:{1:02d}:{2:02d},{3:03d}".format(hour, minute, second, micro_second)

def process(file_name, shift_milliseconds, scale):
    seq = 1
    buf = []
    def flush_buf(drop_last=True):
        for e in buf[slice(None, -1 if drop_last else None)]:
            print(e, end="")

    with open(file_name, "rt") as f:
        for l in f:
            if l.find("-->") < 0:
                buf.append(l)
            else:
                flush_buf()
                print(seq)
                seq += 1
                buf.clear()
                print(" --> ".join(map(
                        lambda st: t2s(
                                int((s2t(st.strip()) + shift_milliseconds) * scale)
                            ),
                        l.split("-->")
                    )))
    flush_buf(False)

if "__main__" == __name__:
    if len(sys.argv) != 6:
        print("Usage: {0} srt_file first_srt_time[hh:mm:ss] first_video_time second_srt_time second_video_time".format(sys.argv[0]), file=sys.stderr)
        sys.exit(1)

    process_file = sys.argv[1]
    x1, y1, x2, y2 = map(get_seconds, sys.argv[2:])
    scale = float((y2-y1)/(x2-x1))
    shift_sec = y2 / scale - x2
    process(process_file, shift_sec * 1000, scale)

