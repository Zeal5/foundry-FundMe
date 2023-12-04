from web3 import Web3, AsyncWeb3, WebsocketProviderV2
import asyncio
from dotenv import load_dotenv
import os
from hexbytes import HexBytes
from dataclasses import dataclass, asdict
from typing import Union, Optional, List
from hexbytes import HexBytes
from pprint import pprint
import aiofiles
import time
load_dotenv()

ALCHEMY_KEY_WSS = os.getenv("alchemy_wss")
ALCHEMY_KEY_HTTP= os.getenv("alchemy_http")

w3_http = Web3(Web3.WebsocketProvider(ALCHEMY_KEY_WSS))
w3_async  = AsyncWeb3(AsyncWeb3.AsyncHTTPProvider(ALCHEMY_KEY_HTTP))

mempool = []

@dataclass
class PendingTransaction:
    _from : Optional[HexBytes] 
    to : HexBytes
    nonce : Optional[int]
    hash : Optional[HexBytes]
    input: Optional[HexBytes]
    gas: Optional[int] = None
    maxFeePerGas: Optional[int] = None
    maxPriorityFeePerGas: Optional[int] = None
    gasPrice: Optional[int] = None
    value: Optional[int] = None
    chainId: Optional[int] = None
    accessList: Optional[List] = None
    type: Optional[int] = None
    yParity: Optional[int] = None
    v: Optional[int] = None
    r: Optional[HexBytes] = None
    s: Optional[HexBytes] = None
    blockHash: Optional[str] = None
    blockNumber:Optional[int] = None
    transactionIndex : Optional[str] = None

    
async def get_rawTransaction_data():
    while True:
        if mempool:
            tx = mempool[0]
            del mempool[0]
            async with aiofiles.open("new_tokens.txt",mode='a') as f:
                await f.write(f"{time.time():<22}{tx.hash.hex()}\n")
            # check input data to check if txns had CREATE op code (contract deployment)
            # if tx.input.hex()[0:11] == '0x60806040':
            #     print(f"{tx._from}\t->\t{tx.to}\n {tx.hash.hex()}\t {tx.input.hex()}\n\n")
            continue
        await asyncio.sleep(0.1)

    

async def main():
    async with AsyncWeb3.persistent_websocket(WebsocketProviderV2(ALCHEMY_KEY_WSS)) as w3:
        # alchemy_pendingTransactions can only be subscribed using alchemy node provider
        sub_id =await  w3.eth.subscribe("alchemy_pendingTransactions")
        async for response in w3.ws.listen_to_websocket():
            result = response.get('result').__dict__
            result['_from'] = result.pop('from')
            txn_obj = PendingTransaction(**result)
            mempool.append(txn_obj)



if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(get_rawTransaction_data())
    loop.run_until_complete(main())

