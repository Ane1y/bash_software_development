import os.path
import re
import sys
from typing import List, Tuple

from src.Executable import BuiltIn


class Wc:
    def __init__(self):
        super().__init__()
        self.total_lns: int = 0
        self.total_wrd: int = 0
        self.total_bts: int = 0

    def impl(self, args) -> int:

        files: List[str] = args
        stats: List[Tuple[int, int, int]] = []
        error: bool = False

        for file in files:
            try:
                with open(file, "r+") as f:
                    stats.append(self.count_file(f))
            except OSError as e:
                print(f"wc: {e.filename}: {e.strerror}")
                error = True

        if len(files) == 0:
            for s in self.count_file(sys.stdin):
                print(f"{s:>{8}}", end=" ")

            return 0

        if len(files) > 1:
            stats.append((self.total_lns, self.total_wrd, self.total_bts))
            files.append("total")

        self.print_stats(stats, files)

        if error:
            return 1
        return 0

    def print_stats(self, stats, files):
        max_len = max([len(str(max(stat))) for stat in stats])

        for stat, file in zip(stats, files):
            for s in stat:
                print(f"{s:>{max_len}}", end=" ")
            print(file)

    def count_file(self, file, filename=None) -> Tuple[int, int, int]:
        text = file.read()

        # Lines
        lns: int = text.count("\n")
        self.total_lns += lns

        # Words | split by spaces, filter out empty words
        wrd: int = len(
            list(filter(lambda word: word != "", re.split("\\s+", text)))
        )
        self.total_wrd += wrd

        # Bytes
        bts: int = len(text) if filename is None else os.path.getsize(filename)
        self.total_bts += bts

        return lns, wrd, bts


if __name__ == '__main__':
    Wc().impl(sys.argv[1:])
