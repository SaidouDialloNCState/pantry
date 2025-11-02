from __future__ import annotations
from dataclasses import dataclass
from typing import Tuple, Dict, Optional
import numpy as np
from vla.schema.actions import Action, ActMove, ActPick, ActPlace

@dataclass
class Obj:
    color: str
    pos: Tuple[int,int]
    delivered: bool = False

@dataclass
class AgentState:
    pos: Tuple[int,int]
    holding: Optional[str] = None

class GridWorld:
    def __init__(self, w=5, h=5, seed: int = 0):
        self.w, self.h = w, h
        self.rng = np.random.default_rng(seed)
        self.bin = (w-1, h-1)
        self.reset(seed)

    def reset(self, seed: Optional[int] = None):
        if seed is not None:
            self.rng = np.random.default_rng(seed)
        # Place agent and objects
        self.agent = AgentState(pos=(0,0), holding=None)
        red_pos = (int(self.rng.integers(0,self.w)), int(self.rng.integers(0,self.h)))
        blue_pos = (int(self.rng.integers(0,self.w)), int(self.rng.integers(0,self.h)))
        # Avoid spawning exactly at bin to keep it interesting
        if red_pos == self.bin: red_pos = (0, self.h-1)
        if blue_pos == self.bin: blue_pos = (self.w-1, 0)
        self.objs = {
            "red": Obj("red", red_pos, False),
            "blue": Obj("blue", blue_pos, False),
        }
        self.steps = 0
        return self.observe()

    def in_bounds(self, p): 
        x,y = p; return 0 <= x < self.w and 0 <= y < self.h

    def observe(self) -> Dict:
        """Symbolic map (sufficient for this project)."""
        return {
            "agent": {"pos": self.agent.pos, "holding": self.agent.holding},
            "objects": {c: {"pos": o.pos, "delivered": o.delivered} for c,o in self.objs.items()},
            "bin": self.bin,
        }

    def step(self, a: Action) -> Dict:
        self.steps += 1
        if isinstance(a, ActMove):
            dx,dy = {"N":(0,-1),"S":(0,1),"E":(1,0),"W":(-1,0)}[a.direction]
            x,y = self.agent.pos
            np_pos = (x+dx, y+dy)
            if self.in_bounds(np_pos):
                self.agent.pos = np_pos
        elif isinstance(a, ActPick):
            obj = self.objs[a.color]
            if self.agent.holding is None and obj.pos == self.agent.pos and not obj.delivered:
                self.agent.holding = a.color
        elif isinstance(a, ActPlace):
            if self.agent.holding is not None and self.agent.pos == self.bin:
                self.objs[self.agent.holding].delivered = True
                self.agent.holding = None
        return self.observe()

    def is_success_sequence(self, required: list[str]) -> bool:
        """All required colors delivered in any order (sequence checked in eval)."""
        return all(self.objs[c].delivered for c in required)
