from rich import print
from vla.envs.gridworld import GridWorld
from vla.agents.heuristic import plan as heuristic_plan
from vla.agents.planner import plan as planner_plan
from vla.utils.trace import TraceLogger
from vla.utils.config import load_config

def main():
    cfg = load_config("defaults")
    seed = int(cfg["seed"])
    instr = str(cfg["instruction"])
    agent_name = str(cfg["agent"]["name"])
    w = int(cfg["env"]["w"]); h = int(cfg["env"]["h"])

    env = GridWorld(w=w, h=h, seed=seed)
    planner = planner_plan if agent_name=="planner" else heuristic_plan
    logger = TraceLogger()

    print(f"[bold]Instruction:[/bold] {instr}")
    print(f"[bold]Agent:[/bold] {agent_name}")

    obs = env.observe()
    logger.log(event="reset", obs=obs, instruction=instr, agent=agent_name, seed=seed)

    for t, act in enumerate(planner(env, instr), start=1):
        logger.log(event="act", t=t, action=getattr(act, "model_dump", lambda: act.__dict__)())
        logger.log(event="obs", obs=env.observe())

    delivered = {c: int(o["delivered"]) for c,o in env.observe()["objects"].items()}
    print("[green]Delivered:[/green]", delivered)
    logger.log(event="done", delivered=delivered)
    logger.close()

if __name__ == "__main__":
    main()
