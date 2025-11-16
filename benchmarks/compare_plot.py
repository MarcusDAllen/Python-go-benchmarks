# compare_plot.py
import sys, shutil, subprocess as sp
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent

PY = sys.executable

SCAN_PY = ROOT / "python" / "scan_py.py"
SCAN_GO_SRC = ROOT / "go" / "scan_go.go"
SCAN_GO_EXE = ROOT / "go" / "scan_go.exe"

SIZES = [1_000, 10_000, 100_000, 1_000_000, 10_000_000, 100_000_000]

def run_capture(cmd, desc):
    try:
        out = sp.check_output(cmd, cwd=HERE, text=True, stderr=sp.STDOUT)
    except FileNotFoundError as e:
        print(f"[ERROR] {desc}: {e}")
        sys.exit(1)
    except sp.CalledProcessError as e:
        print(f"[ERROR] {desc} failed.\n{e.output}")
        sys.exit(1)

    parts = out.strip().split()
    if len(parts) != 3:
        print(f"[ERROR] Unexpected output from {desc}:\n{out}")
        sys.exit(1)
    n, sec, cnt = parts
    return int(n), float(sec), int(cnt)

def main():
    print("Benchmark starting...\n")
    py_times, go_times = [], []

    for n in SIZES:
        print(f"→ Python n={n}...", end="", flush=True)
        n_py, t_py, _ = run_capture([PY, str(SCAN_PY), str(n)], "Python scan")
        print(" done ✓")

        print(f"→ Go     n={n}...", end="", flush=True)
        if shutil.which("go") and SCAN_GO_SRC.exists():
            n_go, t_go, _ = run_capture(["go", "run", str(SCAN_GO_SRC), str(n)], "Go scan (go run)")
        elif SCAN_GO_EXE.exists():
            n_go, t_go, _ = run_capture([str(SCAN_GO_EXE), str(n)], "Go scan (exe)")
        else:
            print("\n[ERROR] Go not found or exe missing.")
            sys.exit(1)
        print(" done ✓")

        py_times.append((n_py, t_py))
        go_times.append((n_go, t_go))

    # Extract data
    sizes = [n for n, _ in py_times]
    t_py = [t for _, t in py_times]
    t_go = [t for _, t in go_times]

    print("\nSize         Python(s)        Go(s)")
    for n, p, g in zip(sizes, t_py, t_go):
        print(f"{n:<12} {p:<15.6f} {g:<.6f}")

    # Bar chart setup
    x = np.arange(len(sizes))
    width = 0.35

    fig, ax = plt.subplots(figsize=(9,6))
    ax.bar(x - width/2, t_py, width, label="Python", color="#3572A5")
    ax.bar(x + width/2, t_go, width, label="Go", color="#E69F00")

    ax.set_xticks(x)
    ax.set_xticklabels([f"{n:,}" for n in sizes])
    ax.set_xlabel("Number of generated values (n)")
    ax.set_ylabel("Runtime (seconds)")
    ax.set_title("Python vs Go: Generate + Check Benchmark (Bar Chart)")
    ax.legend()
    ax.grid(True, axis="y", linestyle="--", alpha=0.6)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()
