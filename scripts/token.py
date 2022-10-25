#!/usr/bin/python3

from brownie import PuntosRecompensasCoin, accounts,config, network

LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["development"]

def main():
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        account = accounts[0]
    if network.show_active() in config["networks"]:
        account = accounts.add(config["wallets"]["from_key"])

    return PuntosRecompensasCoin.deploy({'from': account})
