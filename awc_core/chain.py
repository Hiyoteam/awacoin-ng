from pydantic import BaseModel
from typing import Dict
from awc_core.mine_pool import MinePool

class Chain(BaseModel):
    wallets: Dict[str, str]
    decimal_units: int
    def __init__(self, decimal_units: int = 18, difficult: int = 32, try_limits: int = 5):
        self.wallets = {}
        self.decimal_units = decimal_units
        self.pool = MinePool(difficult=difficult, try_limits=try_limits)
    