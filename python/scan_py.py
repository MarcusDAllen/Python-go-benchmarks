# scan_py.py
import sys, time, random, string

if len(sys.argv) < 2:
    print("usage: python scan_py.py <n>")
    sys.exit(1)

n = int(sys.argv[1])
alphabet = string.ascii_lowercase + "123456789" + r"""!@#$%^&*()-_=+[]{};:'",.<>/?\|`~"""

# optional: fixed seed so runs are consistent
rng = random.Random(12345)

def generate_and_check(n):
    count = 0
    for _ in range(n):
        ch = rng.choice(alphabet)
        if ch in "aeiou135!":
            count += 1
    return count

t0 = time.perf_counter()
count = generate_and_check(n)
t1 = time.perf_counter()

print(f"{n} {t1 - t0:.6f} {count}")
