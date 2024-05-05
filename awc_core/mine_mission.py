from hashlib import sha512
from random import randint
from pydantic import BaseModel
from secrets import token_urlsafe

class Mission:
    answer: str
    problem: str
    try_times: int
    try_limits: int
    def __init__(self, difficult: int, try_limits: int = 5):
        answer = [ randint(0,1) for _ in range(difficult) ]
        self.answer = "".join([ str(i) for i in answer ])
        self.salt = token_urlsafe(8)
        self.answer += self.salt
        self.problem = sha512(self.answer.encode("utf-8")).hexdigest()
        self.try_times = 0
        self.try_limits = try_limits
    def resolve(self, answer):
        if (self.try_times + 1) > self.try_limits and self.try_limits != 0:
            return False
        self.try_times+=1
        if answer != self.answer:
            return False
        return True