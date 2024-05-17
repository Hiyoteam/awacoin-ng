# awacoin-ng
Next awacoin.

Disclaimer: awacoin-ng is **purely recreational** **centralized virtual currency** and is not linked to **any** real currency. Please **DO NOT USE FOR COMMERCIAL USE**.

## Server
### Quickstart
Enter the following command to configure the awacoin-ng server by default.

```
$ git clone https://github.com/HiyoTeam/awacoin-ng
$ cd awacoin-ng
$ pip3 install -r requirements.txt
$ uvicorn main:app
$ uvicorn main:app
```
When you turn on the server for the first time, the server quits because it can't find the configuration file. (We'll talk about configuration files shortly.) Here, we run the server again to start the server with the default configuration.  

When you see that the awacoin-ng server is up and running, try visiting our [online miner](https://thz.cool/awcng-miner.html#some_nonexist_address@http://127.0.0.1:8000) to test if the server is working properly. If you see a "Ping failed" error, which proves that the server is not working properly, please open an Issue and attach all outputs. If you see the "Start mining" button turn blue, the server is working. (We can't start mining yet, because we haven't created the first wallet)

Next, let's simply create a wallet.

Go to `http://127.0.0.1:8000/wallets/create` and you will see a JSON return, where we will only remember the "public_key" field.

Next, we'll replace the "some_nonexist_address" in the miner's address with the "public_key" field. For example:

`https://thz.cool/awcng-miner.html#some_nonexist_address@http://127.0.0.1:8000`
Replace with
`https://thz.cool/awcng-miner.html#c06cd23bb438b5ac36032fe3b1e5cd21ccb2fcdc5629e539fa4f890449ed64c6@http://127.0.0.1:8000`

Open this address and click on "Start mining", you should soon see the miner start working and the occasional "Rewarded 1 AWC to your account!" pop up. Next, let's go to `http://127.0.0.1:8000/wallets/info?wallet=<your wallet address>` and you should see the `balance` field grow rapidly as the miner runs!

### Configuration files
The configuration file is in `/datas/config.json`, a default configuration file looks like this:
`{"coin_name": "awacoin", "coin_short_name": "awc", "chunk_reward":1, "chunk_difficult":8}`
Let's explain this configuration file field by field.
#### coin_name and coin_short_name
These two fields are about the name of the currency that is displayed on the client side. coin_name is the full name of the currency and coin_short_name is the short name of the currency.
For example, if you want to issue an AWC-NG branch called "ByteCoin", you might change it to `"coin_name": "bytecoin", "coin_short_name": "btc"`. This will change the "Rewarded 1 AWC to your account!" message in the miner to "Rewarded 1 BTC to your account!".
#### chunk_reward
This field is the amount of reward currency the client receives whenever it solves a PoW task. If it's 10, you'll get 10 currencies for each task you complete, and so on.
#### chunk_difficult
This field is the difficulty factor of each PoW task. The likelihood of the client solving the problem in a single operation is $\frac{1}{chunkdifficult^2}$, which simply means that the higher this number is, the more work the operation will take.

## Client
The default miner client is in the `client/` directory, just run `python3 miner.py` to mine.

If you want better performance, you can compile `cpp-miner.cpp` to `miner-cpp-binary`, and the python miner will automatically detect it and use it for calculations instead. This program requires openssl@3 and the gmp library.(Sorry, I'm not good at C++, this program may be rudimentary, so please forgive me for not being able to give more technical details.)

### Connecting to a private AWC-NG instance
It's pretty simple, you just need to replace all the `https://awcng.awa.ac.cn` in it with the address of your instance and it should work perfectly!

Translated with DeepL.com (free version)
(sorry for using machine translation.)