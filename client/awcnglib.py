import requests
import hashlib
from typing import Optional

CLIENT_VERSION = 1

class RequestError(Exception):
    pass

def internal_miner(salt: str, difficult: int, problem: str):
    mine_to=int("0b"+(difficult*"1"), 2)
    print(f"Mining: from 0 to {mine_to}...")
    for i in range(0, mine_to+1):
        i=bin(i)[2:]
        i="0"*(difficult-len(i))+i
        hashed=hashlib.sha512((i+salt).encode("utf-8")).hexdigest()
        print("\r"+i, end="", flush=True)
        if hashed == problem:
            print()
            return i+salt
    raise ValueError("Didn't found answer")

class AWCPoWMineMission:
    def __init__(self, mission_id: str, problem: str, salt: str, reward_to: str, client: "AWCNGClient") -> None:
        self.mission_id, self.problem, self.salt, self.reward_to, self.client, self.chunk_difficult = mission_id, problem, salt, reward_to, client, client.chunk_difficult
    def finish(self, answer: str):
        return self.client._request("/mining/pow/finish",params={
            "mission_id": self.mission_id,
            "answer": answer,
            "reward_to": self.reward_to
        })

class AWCNGClient:
    def __init__(self, server: str, public_key: Optional[str] = None, private_key: Optional[str] = None, debug: bool = False) -> None:
        self.server=server
        self.debug = debug
        self._request_cache = {}
        self.ping()
        if not public_key or not private_key:
            self.create_keypair()
        else:
            self.public_key, self.private_key = public_key, private_key
        if not self.validate_keypair():
            raise ValueError("Invaild keypair")
        server_version=self.server_info()["server_version"]
        if server_version != CLIENT_VERSION:
            raise ConnectionError(f"The client is for AWC-NG Version {CLIENT_VERSION}, but the server version is {server_version}. Try upgrading your awcnglib.")
    def _request(self, path, params={}, process_errors=True, cache=False) -> dict:
        if cache and f"{path}@{params}" in self._request_cache.keys():
            print(f"awcngclient._request: (cache hit) requesting {path} with params {params}")
            request:requests.Response=self._request_cache[f"{path}@{params}"]
        else:
            for _ in range(5):
                if self.debug:
                    print(f"awcngclient._request: requesting {path} with params {params}")
                try:
                    request:requests.Response = requests.get(self.server+path[1:] if self.server.endswith("/") else self.server+path,
                                            params=params if params else None)
                    break
                except KeyboardInterrupt as e:
                    raise e
                except:
                    pass
            if cache:
                print(f"awcngclient._request: (cache miss) updating cache for {path}")
                self._request_cache[f"{path}@{params}"]=request
        if request.status_code == 500:
            raise RequestError("Server internal error")
        if request.json()["status"] != 200 and process_errors:
            raise RequestError(request.json().get("code", "UNKNOWN_ERROR"))
        return request.json()

    def create_keypair(self):
        response = self._request("/wallets/create")
        self.public_key = response["public_key"]
        self.private_key = response["private_key"]
    
    def validate_keypair(self):
        return self._request("/wallets/probe", {
            "public_key": self.public_key,
            "private_key": self.private_key
        })["available"]
    
    def ping(self):
        return self._request("/ping")
    
    def create_pow_mission(self) -> AWCPoWMineMission:
        mission = self._request("/mining/pow/create")
        return AWCPoWMineMission(
            mission_id=mission["mission_id"],
            problem=mission["problem"],
            salt=mission["salt"],
            reward_to=self.public_key,
            client=self)

    def wallet_info(self):
        return self._request("/wallets/info", {
            "wallet": self.public_key,
        })
    
    def transfer(self, target: str, amount: int):
        return self._request("/transaction/create",params={
            "public_key": self.public_key,
            "private_key": self.private_key,
            "target_wallet": target,
            "amount": amount
        })
    
    def server_info(self):
        return self._request("/info", cache=True)
    
    @property
    def chunk_reward(self):
        return self.server_info()["chunk_reward"]
    
    @property
    def chunk_difficult(self):
        return self.server_info()["chunk_difficult"]

    @property
    def balance(self):
        return self.wallet_info()["balance"]
    
    @property
    def coin_name(self):
        return self.server_info()["coin_name"]
    
    @property
    def coin_short_name(self):
        return self.server_info()["coin_short_name"].upper()


if __name__ == "__main__":
    print("Connecting...")
    client=AWCNGClient("https://awcng.awa.ac.cn", debug=True)
    print(f"Connected to {client.public_key}@{client.server} ({client.coin_short_name})!")
    print(f"Trying to mine a(n) {client.coin_short_name}...")
    print("Diff:",client.chunk_difficult)
    print("Reward:",client.chunk_reward)
    print("Requesting mission...")
    mission=client.create_pow_mission()
    print("OK!")
    print("Submit result:",mission.finish(internal_miner(mission.salt, mission.chunk_difficult, mission.problem)))
    print("Current balance:",client.balance)
    print("Testing transfer")
    client2=AWCNGClient("https://awcng.awa.ac.cn")
    print(f"@{client.server}: {client.public_key} -> 1 {client.coin_short_name} -> {client2.public_key}")
    print(f"Before: C1: {client.balance}, C2: {client2.balance}")
    client.transfer(client2.public_key, 1)
    print(f"After: C1: {client.balance}, C2: {client2.balance}")