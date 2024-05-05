from awcnglib import AWCNGClient, internal_miner
from os import path, popen
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
miner=""
if path.exists("miner-cpp-binary"):
    print("Using C++ Miner")
    miner="binary"
else:
    print("Using internal miner")
    miner="internal"
while 1:
    try:
        print("Requesting mission...")
        mission=client.create_pow_mission()
        print("OK!")
        if miner == "binary":
            cmdline=f"./miner-cpp-binary {mission.salt} {mission.chunk_difficult} {mission.problem.upper()}"
            print(f"> {cmdline}")
            result=popen(cmdline).read()
            print(f"< {result}")
        else:
            result=internal_miner(mission.salt, mission.chunk_difficult, mission.problem)
        print("Submit result:",mission.finish(result))
        print("Current balance:",client.balance)
    except:
        print("Failed mining, ignoring.")