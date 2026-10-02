"""
Tugas Kelompok - Berbasis Kasus 01
Robot kurir kampus: GU (Gerbang Utama) -> LK (Lab Komputasi)
Metode: UCS, IDS, GBFS, A*

Graf diverifikasi dari gambar hires (19 edge, undirected).
Tie-break: alfabetis agar deterministik.
"""

import heapq
from collections import defaultdict

# ---------- Graf ----------
GRAPH = {
    "GU":  [("PB", 3), ("R", 4)],
    "PB":  [("GU", 3), ("GKU", 4), ("K", 6)],
    "R":   [("GU", 4), ("PR", 3), ("M", 5)],
    "GKU": [("PB", 4), ("PR", 2), ("K", 3), ("IF", 7)],
    "K":   [("PB", 6), ("GKU", 3), ("AS", 5)],
    "PR":  [("R", 3), ("GKU", 2), ("A", 6), ("IF", 4)],
    "A":   [("PR", 6), ("M", 3), ("LK", 5)],
    "M":   [("R", 5), ("A", 3), ("SC", 6)],
    "IF":  [("GKU", 7), ("PR", 4), ("AS", 4), ("LK", 3)],
    "AS":  [("K", 5), ("IF", 4), ("SC", 6)],
    "SC":  [("M", 6), ("AS", 6), ("LK", 4)],
    "LK":  [("A", 5), ("IF", 3), ("SC", 4)],
}

H = {
    "GU": 12, "PB": 10, "R": 9, "GKU": 7, "PR": 6,
    "K": 9, "M": 7, "A": 4, "AS": 5, "IF": 2, "SC": 3, "LK": 0,
}

NAMA = {
    "GU": "Gerbang Utama", "PB": "Parkir Barat", "R": "Rektorat",
    "GKU": "Gedung Kuliah Umum", "PR": "Perpustakaan", "K": "Kantin",
    "M": "Masjid", "A": "Aula", "AS": "Asrama", "IF": "Teknik Informatika",
    "SC": "Sport Center", "LK": "Lab Komputasi",
}

START, GOAL = "GU", "LK"


def neighbors_sorted(node):
    return sorted(GRAPH[node], key=lambda x: x[0])


def reconstruct(parent, goal):
    path, cur = [goal], goal
    while parent[cur] is not None:
        cur = parent[cur]
        path.append(cur)
    return list(reversed(path))


def path_cost(path):
    total = 0
    for a, b in zip(path, path[1:]):
        for nb, w in GRAPH[a]:
            if nb == b:
                total += w
                break
    return total


# ---------- UCS ----------
def ucs(start=START, goal=GOAL):
    pq = [(0, start)]  # (g, node)
    best = {start: 0}
    parent = {start: None}
    expansion = []     # urutan pop
    pop_g = {}
    visited = set()
    while pq:
        g, n = heapq.heappop(pq)
        if n in visited:
            continue
        # jika ada jalur lebih baik sudah tercatat, skip basi
        if g > best.get(n, float("inf")):
            continue
        visited.add(n)
        expansion.append(n)
        pop_g[n] = g
        if n == goal:
            break
        for nb, w in neighbors_sorted(n):
            ng = g + w
            if nb not in best or ng < best[nb]:
                # izinkan reopen bila lebih baik (penting utk A*, utk UCS sama saja)
                if nb not in visited or ng < best[nb]:
                    best[nb] = ng
                    parent[nb] = n
                    heapq.heappush(pq, (ng, nb))
    path = reconstruct(parent, goal) if goal in parent else []
    return {"expansion": expansion, "path": path,
            "cost": path_cost(path) if path else None, "g": pop_g}


# ---------- GBFS ----------
def gbfs(start=START, goal=GOAL):
    pq = [(H[start], start)]  # (h, node)
    parent = {start: None}
    expansion = []
    visited = set()
    g_cost = {start: 0}
    while pq:
        _, n = heapq.heappop(pq)
        if n in visited:
            continue
        visited.add(n)
        expansion.append(n)
        if n == goal:
            break
        for nb, w in neighbors_sorted(n):
            if nb not in visited and nb not in [x[1] for x in pq]:
                parent[nb] = n
                g_cost[nb] = g_cost[n] + w
                heapq.heappush(pq, (H[nb], nb))
            elif nb in g_cost and g_cost[n] + w < g_cost[nb]:
                # update bila jalur lebih murah meski h sama (variasi umum)
                pass
    path = reconstruct(parent, goal) if goal in parent else []
    return {"expansion": expansion, "path": path,
            "cost": path_cost(path) if path else None}


# ---------- A* ----------
def astar(start=START, goal=GOAL):
    pq = [(H[start], 0, start)]  # (f, g, node)
    best_g = {start: 0}
    parent = {start: None}
    expansion = []
    pop_f = {}
    visited_closed = set()
    while pq:
        f, g, n = heapq.heappop(pq)
        if n in visited_closed and g >= best_g.get(n, float("inf")):
            continue
        if g > best_g.get(n, float("inf")):
            continue
        visited_closed.add(n)
        expansion.append(n)
        pop_f[n] = (g, H[n], f)
        if n == goal:
            break
        for nb, w in neighbors_sorted(n):
            ng = g + w
            if nb not in best_g or ng < best_g[nb]:
                best_g[nb] = ng
                parent[nb] = n
                heapq.heappush(pq, (ng + H[nb], ng, nb))
            elif nb not in visited_closed:
                pass
    path = reconstruct(parent, goal) if goal in parent else []
    return {"expansion": expansion, "path": path,
            "cost": path_cost(path) if path else None, "detail": pop_f}


# ---------- IDS ----------
def dls(limit, start=START, goal=GOAL, log=None):
    """Depth-Limited DFS (path-checking, alfabetis). Return path atau None."""
    found = None
    def rec(n, depth, path, path_set):
        nonlocal found
        if log is not None:
            log.append(n)
        if found is not None:
            return True
        if n == goal:
            found = list(path)
            return True
        if depth == limit:
            return False
        for nb, _ in neighbors_sorted(n):
            if nb in path_set:  # hindari cycle dalam satu jalur
                continue
            path.append(nb)
            path_set.add(nb)
            if rec(nb, depth + 1, path, path_set):
                return True
            path.pop()
            path_set.remove(nb)
        return False
    rec(start, 0, [start], {start})
    return found


def ids(start=START, goal=GOAL, max_depth=10):
    per_limit = {}
    total_expansions = 0
    solution = None
    solution_depth = None
    for lim in range(0, max_depth + 1):
        log = []
        p = dls(lim, start, goal, log)
        per_limit[lim] = {"visited_order": list(log), "count": len(log),
                          "found": p}
        total_expansions += len(log)
        if p is not None:
            solution = p
            solution_depth = lim
            break
    cost = path_cost(solution) if solution else None
    return {"per_limit": per_limit, "path": solution,
            "cost": cost, "depth": solution_depth,
            "total_expanded": total_expansions,
            "expansion": per_limit[solution_depth]["visited_order"] if solution else []}


# ---------- main ----------
def fmt_path(p):
    return " -> ".join(p) if p else "-"


def main():
    u = ucs()
    i = ids()
    g = gbfs()
    a = astar()

    print("=" * 70)
    print("KASUS 01: Robot kurir kampus GU -> LK")
    print("=" * 70)

    print("\n[UCS] Urutan ekspansi (pop terkecil g):")
    print(" ", " -> ".join(u["expansion"]))
    print("  g saat pop:", {n: u["g"][n] for n in u["expansion"]})
    print("  Rute :", fmt_path(u["path"]))
    print("  Cost :", u["cost"], "| node diekspansi:", len(u["expansion"]))

    print("\n[IDS] Iterative Deepening (DFS alfabetis, limit 0..n):")
    for lim, d in i["per_limit"].items():
        status = "KETEMU " + fmt_path(d["found"]) if d["found"] else "belum ketemu"
        print(f"  limit={lim} ({d['count']} kunjungan): {' -> '.join(d['visited_order'])} => {status}")
    print("  Rute :", fmt_path(i["path"]))
    print("  Cost (jumlah bobot) :", i["cost"], "| depth solusi:", i["depth"],
          "| total kunjungan kumulatif:", i["total_expanded"])

    print("\n[GBFS] Urutan ekspansi (pop terkecil h):")
    print(" ", " -> ".join(g["expansion"]))
    print("  Rute :", fmt_path(g["path"]))
    print("  Cost :", g["cost"], "| node diekspansi:", len(g["expansion"]))

    print("\n[A*] Urutan ekspansi (pop terkecil f=g+h):")
    print(" ", " -> ".join(a["expansion"]))
    print("  detail pop (g,h,f):", {n: {"g": v[0], "h": v[1], "f": v[2]} for n, v in a["detail"].items()})
    print("  Rute :", fmt_path(a["path"]))
    print("  Cost :", a["cost"], "| node diekspansi:", len(a["expansion"]))

    print("\n--- RINGKASAN ---")
    for nama, r in [("UCS", u), ("IDS", i), ("GBFS", g), ("A*", a)]:
        n_exp = len(r["expansion"]) if nama != "IDS" else f"{i['total_expanded']} (kumulatif, solusi depth {i['depth']})"
        print(f"{nama:5s} | ekspansi: {n_exp} | rute: {fmt_path(r['path'])} | cost: {r['cost']}")


if __name__ == "__main__":
    main()
