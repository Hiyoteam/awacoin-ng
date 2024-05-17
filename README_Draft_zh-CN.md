# 服务器
## Quickstart
输入以下命令来以默认配置awacoin-ng服务器。

```
$ git clone https://github.com/HiyoTeam/awacoin-ng
$ cd awacoin-ng
$ pip3 install -r requirements.txt
$ uvicorn main:app
$ uvicorn main:app
```
在第一次开启服务器时，服务器会因为找不到配置文件而退出。（我们很快将讲述配置文件）在这里，我们再次运行服务器来使用默认配置来启动服务器。  

当您看见awacoin-ng服务器已经开始运行，尝试访问我们的[在线矿工](https://thz.cool/awcng-miner.html#some_nonexist_address@http://127.0.0.1:8000)来测试服务器是否正常工作。如果您看见“Ping failed”错误，证明服务器没有正常运行，请打开一个Issue并附上所有输出。如果您看见“Start mining”按钮变为蓝色，那证明服务器工作正常。（我们现在还不能开始挖掘，因为我们并没有创建第一个钱包）

接下来，我们简单地创建一个钱包。

访问`http://127.0.0.1:8000/wallets/create`,然后您会看见一个JSON返回，在这里，我们只记住其中的“public_key”字段。

接下来，我们将刚刚的矿工地址中的“some_nonexist_address”替换为这个"public_key"字段。例如：

`https://thz.cool/awcng-miner.html#some_nonexist_address@http://127.0.0.1:8000`
替换至
`https://thz.cool/awcng-miner.html#c06cd23bb438b5ac36032fe3b1e5cd21ccb2fcdc5629e539fa4f890449ed64c6@http://127.0.0.1:8000`

打开这个地址，点击“Start mining”，您应该很快就能看见矿工开始工作，并且时不时弹出“Rewarded 1 AWC to your account!”的提示。接下来，我们访问`http://127.0.0.1:8000/wallets/info?wallet=<你的钱包地址>`，你应该能看见“balance”字段随着矿工的运行而迅速增长！

## 配置文件
配置文件在`/datas/config.json`，一个默认的配置文件看起来是这样：
`{"coin_name":"awacoin","coin_short_name":"awc","chunk_reward":1,"chunk_difficult":8}`
让我们逐字段的解释这个配置文件。
### coin_name 和 coin_short_name
这两个字段关于在客户端侧显示的货币名称，coin_name是货币的全称而coin_short_name是货币的简称。
举个例子，如果您想发行名为“ByteCoin”的AWC-NG分支，你可能会将其修改为`"coin_name":"bytecoin","coin_short_name":"btc"`。这样，在矿工中出现的“Rewarded 1 AWC to your account!”提示就会变为“Rewarded 1 BTC to your account!”。
### chunk_reward
这个字段是每当客户端解决一个PoW任务时得到的奖励货币数。如果其为10，你每完成一个任务就会得到10个货币，以此类推。
### chunk_difficult
这个字段是每个PoW任务的难度系数。客户端在单次运算中解决问题的可能性是$\frac{1}{chunk\_difficult^2}$，简单的说，这个数字越大，运算的工作量就越多。

# 客户端
默认的矿工客户端在`client/`目录里，只需要运行`python3 miner.py`就可以进行挖掘。
如果你想要更好的性能，可以编译`cpp-miner.cpp`为`miner-cpp-binary`，python矿工会自动检测到它并改为使用它来进行计算。此程序需要openssl@3和gmp library.（抱歉，我不擅长C++，这个程序可能比较简陋，请原谅我无法给出更多技术细节。）

## 连接一个私人AWC-NG实例
这很简单，你只需要把其中所有的`https://awcng.awa.ac.cn`替换为你的实例地址，然后它应该就能完美运行了!