import pandas as pd
import matplotlib.pyplot as plt

def main(csv_path="runs/ablation.csv", out_png="runs/ablation.png"):
    df = pd.read_csv(csv_path)
    x = range(len(df))
    y = df["success_rate"].astype(float)
    yerr = [y - df["ci_low"].astype(float), df["ci_high"].astype(float) - y]

    plt.figure()
    plt.bar(x, y, yerr=yerr)
    plt.xticks(x, df["agent"])
    plt.ylabel("Success Rate")
    plt.title("Planner vs Heuristic (Held-out Order)")
    plt.savefig(out_png, bbox_inches="tight")
    print(f"Wrote {out_png}")

if __name__ == "__main__":
    main()
