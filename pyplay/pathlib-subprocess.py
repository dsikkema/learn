from pathlib import Path
import subprocess
def find_file_by_pattern(name_pattern: str) -> Path:
    data_dir = Path(__file__).parent / 'data'
    for subd in ('dir_a', 'dir_b'):
        for p in (data_dir / subd).iterdir():
            if p.is_file() and p.match(f"*{name_pattern}*"): # match uses glob pattern.
                return p

def grep_file_for_pattern(filepath: Path, line_pattern: str):
    print(f"Whole output:\n{filepath.read_text()}")
    proc = subprocess.Popen(
        ['grep', line_pattern, filepath.absolute()],
        stdin=None,
        stdout=subprocess.PIPE
    )

    proc.wait(timeout=0.5)
    print(f"Grepped output:\n{proc.stdout.read().decode()}")

f = find_file_by_pattern('dolphin')
grep_file_for_pattern(f, 'swim')