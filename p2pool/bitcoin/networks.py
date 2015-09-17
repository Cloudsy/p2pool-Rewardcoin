import os
import platform

from twisted.internet import defer

from . import data
from p2pool.util import math, pack, jsonrpc

@defer.inlineCallbacks
def check_genesis_block(bitcoind, genesis_block_hash):
    try:
        yield bitcoind.rpc_getblock(genesis_block_hash)
    except jsonrpc.Error_for_code(-5):
        defer.returnValue(False)
    else:
        defer.returnValue(True)

nets = dict(
    Rewardcoin=math.Object(
        P2P_PREFIX='f9bbb6d9'.decode('hex'),
        P2P_PORT=1968,
        ADDRESS_VERSION=50,
        RPC_PORT=1925,
        RPC_CHECK=defer.inlineCallbacks(lambda bitcoind: defer.returnValue(
            (yield check_genesis_block(bitcoind, '0167f68b07587c231403069612646700deb086acc423a7b85f3304ac372e81d9')) and
            not (yield bitcoind.rpc_getinfo())['testnet']
        )),
        SUBSIDY_FUNC=lambda height: 280*100000000 * pow(0.95 ,(height + 1) // 1680), # Rewardcoin has a 5% decline every 1680 blocks
        POW_FUNC=data.hash256,
        BLOCK_PERIOD=360, # s
        SYMBOL='MMC',
        CONF_FILE_FUNC=lambda: os.path.join(os.path.join(os.environ['APPDATA'], 'Rewardcoin') if platform.system() == 'Windows' else os.path.expanduser('~/Library/Application Support/Rewardcoin/') if platform.system() == 'Darwin' else os.path.expanduser('~/.Rewardcoin'), 'Rewardcoin.conf'),
        BLOCK_EXPLORER_URL_PREFIX='http://mmcexplorer.info/?query=',
        ADDRESS_EXPLORER_URL_PREFIX='http://mmcexplorer.info/?query=',
        TX_EXPLORER_URL_PREFIX='http://mmcexplorer.info/?query=',
        SANE_TARGET_RANGE=(2**256//4096 - 1, 2**256//2 - 1),
        DUMB_SCRYPT_DIFF=1,
        DUST_THRESHOLD=1e8,
    ),
    Rewardcoin_testnet=math.Object(
        P2P_PREFIX='f9bcb6d9'.decode('hex'),
        P2P_PORT=11968,
        ADDRESS_VERSION=111,
        RPC_PORT=11925,
        RPC_CHECK=defer.inlineCallbacks(lambda bitcoind: defer.returnValue(
            (yield check_genesis_block(bitcoind, '012c479ee7ab1359a632690a32041a9980a66adcd8a9fc0d9bb1f5f0414edc71')) and
            (yield bitcoind.rpc_getinfo())['testnet']
        )),
        SUBSIDY_FUNC=lambda height: 1,#280*100000000 * pow(0.95 ,(height + 1) // 1680), # Rewardcoin has a 5% decline every 1680 blocks
        POW_FUNC=data.hash256,
        BLOCK_PERIOD=360, # s
        SYMBOL='tMMC',
        CONF_FILE_FUNC=lambda: os.path.join(os.path.join(os.environ['APPDATA'], 'Rewardcoin') if platform.system() == 'Windows' else os.path.expanduser('~/Library/Application Support/Rewardcoin/') if platform.system() == 'Darwin' else os.path.expanduser('~/.Rewardcoin'), 'Rewardcoin.conf'),
        BLOCK_EXPLORER_URL_PREFIX='http://mmcexplorer.info/?query=',
        ADDRESS_EXPLORER_URL_PREFIX='http://mmcexplorer.info/?query=',
        TX_EXPLORER_URL_PREFIX='http://mmcexplorer.info/?query=',
        SANE_TARGET_RANGE=(2**256//4096 - 1, 2**256//2 - 1),
        DUMB_SCRYPT_DIFF=1,
        DUST_THRESHOLD=1e8,
    ),
)
for net_name, net in nets.iteritems():
    net.NAME = net_name
