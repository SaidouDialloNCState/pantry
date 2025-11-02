from rich import print
from vla.utils.config import load_config
from vla.scripts.eval_suite import evaluate

def main():
    cfg = load_config("defaults")
    agent_name = str(cfg["agent"]["name"])
    episodes = int(cfg["eval"]["episodes"])
    seed = int(cfg["seed"])
    rate, _ = evaluate(agent=agent_name, episodes=episodes, seed=seed, split="compositional")
    print(f"{agent_name} success on held-out order: {rate:.2%}")

if __name__ == "__main__":
    main()
