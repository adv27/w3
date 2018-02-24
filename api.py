import random
from multiprocessing import (
    Pool,
    freeze_support
)
from string import Template

import requests
from web3.auto import w3

pk_len = 64
hex_list = list('0123456789abcdef')
api = Template(r'https://api.etherscan.io/api?' \
               r'module=account' \
               r'&action=balance' \
               r'&address=$address' \
               r'&tag=latest')


def gen_pk() -> str():
    len = pk_len
    privatekey = str()
    while len > 0:
        privatekey += hex_list[random.randint(0, 15)]
        len -= 1
    return privatekey


def foo():
    while True:
        pk = gen_pk()
        account = w3.eth.account.privateKeyToAccount(pk)
        address = account.address
        url = api.substitute(address=address)
        status = ''
        eth_value = ''
        while status is not '1':
            r = requests.get(url)
            json_data = r.json()
            status = json_data['status']
            eth_value = json_data['result']
        # if eth_value is not '0':
        print('{} {} {}'.format(pk, address, eth_value))


def throw_away_function(_):
    foo()


if __name__ == '__main__':
    freeze_support()
    with Pool(15) as pool:
        pool.map(throw_away_function, range(15))
