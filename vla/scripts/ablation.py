import csv, random
from pathlib import Path
from typing import List, Tuple
import numpy as np
from vla.envs.gridworld import GridWorld
from vla.agents.heuristic import plan as heuristic_plan, parse_instruction
from vla.agents.planner import plan as planner_plan

def run_agent(agent_name: str, episodes: int, seed: int) -> Tuple[float, List[bool]]:
    rng = random.Random(seed)
    success = []
    # held-out compositional split: always test ("blue","red")
    order = ("blue","red")
    instr = f"pick {order[0]} then {order[1]} into bin"
    for i in range(episodes):
        env = GridWorld(seed=seed+i)
        planner = planner_plan if agent_name=="planner" else heuristic_plan
        delivered_seq = []
        for act in planner(env, instr):
            obs = env.observe()
            for c, o in obs["objects"].items():
                if o["delivered"] and c not in delivered_seq:
                    delivered_seq.append(c)
        success.append(tuple(delivered_seq) == order)
    return (sum(success)/len(success), success)

def bootstrap_ci(success_bools: List[bool], iters: int = 2000, alpha: float = 0.05):
    arr = np.array(success_bools, dtype=float)
    n = len(arr)
    stats = []
    rng = np.random.default_rng(0)
    for _ in range(iters):
        idx = rng.integers(0, n, size=n)
        stats.append(arr[idx].mean())
    low = np.quantile(stats, alpha/2)
    high = np.quantile(stats, 1 - alpha/2)
    return float(low), float(high)

def main(episodes=80, seed=0, out_csv="runs/ablation.csv"):
    Path("runs").mkdir(parents=True, exist_ok=True)
    rows = []
    for agent in ["heuristic", "planner"]:
        rate, success = run_agent(agent, episodes, seed)
        lo, hi = bootstrap_ci(success)
        rows.append({"agent": agent, "episodes": episodes, "seed": seed, "success_rate": f"{rate:.4f}", "ci_low": f"{lo:.4f}", "ci_high": f"{hi:.4f}"})
        print(f"{agent}: {rate:.2%} (95% CI [{lo:.2%}, {hi:.2%}])")

    with open(out_csv, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader(); w.writerows(rows)
    print(f"Wrote {out_csv}")

if __name__ == "__main__":
    main()
