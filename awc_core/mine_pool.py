from typing import Dict
from uuid import uuid4
from awc_core.mine_mission import Mission

class MinePool:
    missions: Dict[str, Mission]
    difficult: int
    try_limits: int
    def __init__(self, difficult: int, try_limits: int = 5) -> None:
        self.missions = {}
        self.difficult = difficult
        self.try_limits = try_limits
    
    def generate_mission(self):
        mission_id = uuid4().hex
        mission = Mission(self.difficult, self.try_limits)
        self.missions.update({mission_id: mission})
        return mission_id, mission
    
    def resolve(self, mission_id, answer):
        if mission_id not in self.missions.keys():
            return False, "MISSION_NONEXT"
        if not self.missions[mission_id].resolve(answer):
            return False, "WRN_ANS"
        del self.missions[mission_id]
        return True, "OK"
    