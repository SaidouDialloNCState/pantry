from pathlib import Path
from typing import Any, Dict
from omegaconf import OmegaConf

def load_config(config_name: str = "defaults") -> Dict[str, Any]:
    root = Path(__file__).resolve().parents[2]  # repo root
    conf_dir = root / "conf"
    cfg = OmegaConf.load(conf_dir / f"{config_name}.yaml")
    # expand nested defaults files:
    # env, agent, eval will be in subdirs; merge them in order
    env = OmegaConf.load(conf_dir / "env" / f"{cfg.env}.yaml") if isinstance(cfg.env, str) else cfg.env
    agent = OmegaConf.load(conf_dir / "agent" / f"{cfg.agent}.yaml") if isinstance(cfg.agent, str) else cfg.agent
    eval_ = OmegaConf.load(conf_dir / "eval" / f"{cfg.eval}.yaml") if isinstance(cfg.eval, str) else cfg.eval
    merged = OmegaConf.merge(cfg, {"env": env, "agent": agent, "eval": eval_})
    return OmegaConf.to_container(merged, resolve=True)  # as plain dict
