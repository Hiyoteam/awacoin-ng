import orjson
from fastapi import FastAPI
from awc_core import MinePool, Wallet
from rich import print
from os import path, mkdir, listdir
from fastapi.middleware.cors import CORSMiddleware

def issecure(*strings):
    for string in strings:
        if "/" in string or ".." in string:
            return False
    return True

if not path.exists("./datas"):
    print("[yellow]WARN[/yellow]:     Config path not found, creating one")
    mkdir("datas")

print("[green]INFO[/green]:     Loading wallets")

if not path.exists("./datas/wallets"):
    print("[yellow]WARN[/yellow]:     Wallets path not found, creating one")
    mkdir("datas/wallets")

print("[green]INFO[/green]:     Loaded", len(listdir("datas/wallets/")), "wallets!")

print("[green]INFO[/green]:     Loading config")

if not path.exists("./datas/config.json"):
    print("[red]FATAL[/red]:     Config not found, created default config, please edit it and reboot.")

    default_config=orjson.dumps({
        "coin_name": "awacoin",
        "coin_short_name": "awc",
        "chunk_reward": 1,
        "chunk_difficult": 8
    })
    with open("./datas/config.json","wb+") as f:
        f.write(default_config)
    exit(1)

with open("./datas/config.json", "rb") as f:
    config = orjson.loads(f.read())

print("[green]INFO[/green]:     Loaded config!")

print("[green]INFO[/green]:     Initing pool")

pool = MinePool(difficult=config["chunk_difficult"])

app = FastAPI()


@app.get("/ping")
async def ping():
    return {"status":200}

@app.get("/info")
async def info():
    result={
        "status":200,
        "server_type":"awc_ng",
        "server_version":1,}
    result.update(config)
    return result

@app.get("/wallets/create")
async def create_wallet():
    wallet=Wallet()
    print(f"[green]INFO[/green]:     Creating wallet {wallet.public_key}")
    with open(f"./datas/wallets/{wallet.public_key}.json", "wb+") as f:
        f.write(orjson.dumps(
            {
                "public_key": wallet.public_key,
                "private_key": wallet.private_key,
                "balance": wallet.balance
            }
        ))
    return {
            "status":200,
            "public_key": wallet.public_key,
            "private_key": wallet.private_key
        }

@app.get("/wallets/info")
async def get_wallet(wallet: str):
    if not issecure(wallet):
        return {"status": 500, "code": "INVAILD_PATH"}
    if not path.exists("./datas/wallets/"+wallet+".json"):
        return {"status": 500, "code": "ERR_WALLET_NOT_FOUND"}
    with open("./datas/wallets/"+wallet+".json", "rb") as f:
        data=orjson.loads(f.read())
    return {"status":200, "balance":data["balance"]}

@app.get("/wallets/probe")
async def detect_wallet_availablity(public_key: str, private_key: str):
    if not issecure(public_key):
        return {"status": 500, "code": "INVAILD_PATH"}
    if not path.exists("./datas/wallets/"+public_key+".json"):
        return {"status": 500, "code": "ERR_WALLET_NOT_FOUND"}
    with open("./datas/wallets/"+public_key+".json", "rb") as f:
        data: dict=orjson.loads(f.read())
    if data["private_key"] != private_key:
        return {"status": 200, "available": False}
    return {"status": 200, "available": True}
    

@app.get('/mining/pow/create')
async def create_pow_mine_mission():
    mission_id, mission = pool.generate_mission()
    return {"status":200, "mission_id": mission_id, "problem":mission.problem, "salt": mission.salt}

@app.get('/mining/pow/finish')
async def finish_pow_mine_mission(mission_id: str, answer: str, reward_to: str):
    if not issecure(reward_to):
        return {"status": 500, "code": "INVAILD_PATH"}
    if not path.exists("./datas/wallets/"+reward_to+".json"):
        return {"status": 500, "code": "ERR_WALLET_NOT_FOUND"}
    successed, message=pool.resolve(mission_id, answer)
    if not successed:
        return {"status": 400, "code": message}
    with open("./datas/wallets/"+reward_to+".json", "rb") as f:
        data: dict=orjson.loads(f.read())
    data.update({"balance": data["balance"]+1})
    with open("./datas/wallets/"+reward_to+".json", "wb+") as f:
        f.write(orjson.dumps(data))
    return {"status": 200, "rewarded_to": reward_to}

@app.get("/transaction/create")
async def transaction(public_key: str, private_key: str, target_wallet: str, amount: int):
    if not issecure(public_key, target_wallet):
        return {"status": 500, "code": "INVAILD_PATH"}
    if not path.exists("./datas/wallets/"+public_key+".json"):
        return {"status": 500, "code": "ERR_WALLET_NOT_FOUND"}
    if not path.exists("./datas/wallets/"+target_wallet+".json"):
        return {"status": 500, "code": "ERR_TARGET_WALLET_NOT_FOUND"}
    with open("./datas/wallets/"+public_key+".json", "rb") as f:
        data: dict=orjson.loads(f.read())
    if data["private_key"] != private_key:
        return {"status": 500, "code": "ERR_WRONG_PRIVATE_KEY"}
    if amount > data["balance"]:
        return {"status": 500, "code": "NO_ENOUGH_BALANCE"}
    data.update({"balance":data["balance"]-amount})
    with open("./datas/wallets/"+public_key+".json", "wb+") as f:
        f.write(orjson.dumps(data))
    with open("./datas/wallets/"+target_wallet+".json", "rb") as f:
        data: dict=orjson.loads(f.read())
    data.update({"balance":data['balance']+amount})
    with open("./datas/wallets/"+target_wallet+".json", "wb+") as f:
        f.write(orjson.dumps(data))
    return {"status": 200}

app.add_middleware(CORSMiddleware,
    allow_origins="*",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"])