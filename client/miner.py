from awcnglib import AWCNGClient, internal_miner
from os import path
SERVER="https://awcng.awa.ac.cn"
if not path.exists(".awcng_wallet"):
    client=AWCNGClient(SERVER)
    with open(".awcng_wallet","w+") as f:
        f.write(SERVER+"$$"+client.public_key+"$$"+client.private_key)
else:
    with open(".awcng_wallet","r") as f:
        data=f.read().split("$$")
        SERVER=data[0]
        pub=data[1]
        sec=data[2]
        client=AWCNGClient(SERVER, pub, sec)
print(f"Logged in as {client.public_key}@{client.server}")
print(f"Start mining.")
print("Diff:",client.chunk_difficult)
while 1:
    print("Requesting mission...")
    mission=client.create_pow_mission()
    print("OK!")
    print("Submit result:",mission.finish(internal_miner(mission.salt, mission.chunk_difficult, mission.problem)))
    print("Current balance:",client.balance)