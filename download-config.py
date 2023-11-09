#!/usr/bin/env python3
"""
Quick script for downloading the necessary files running your own node against Conduit.
"""

import urllib.request
import argparse
import pathlib

CONDUIT_API_URL='https://api.conduit.xyz/'
BOOTNODES_API_PATH='/public/network/bootnodes/'
STATICPEERS_API_PATH='/public/network/staticPeers/'
ROLLUP_API_PATH='/file/v1/optimism/rollup/'
GENESIS_API_PATH='/file/v1/optimism/genesis/'
CONDUIT_RPC_SUFFIX='t.conduit.xyz'

ENV_TEMPLATE='''
OP_GETH_SEQUENCER_HTTP={rpc_url}
#OP_NODE_P2P_BOOTNODES={bootnodes}
OP_NODE_P2P_STATIC={staticPeers}
'''

def fetch_data(api_path, slug):
    with urllib.request.urlopen(f'{CONDUIT_API_URL}{api_path}{slug}') as response:
        return response.read()

parser = argparse.ArgumentParser(description='Download Conduit Configs')
parser.add_argument('slug', metavar='SLUG', type=str, help='Slug of the stack you want to download configs for.')
parser.add_argument('-p', '--path', metavar='PATH', type=str, help='Path to save the files to. Defaults to `network/<slug>/`.')
args = parser.parse_args()

# Set up directories
repo_dir = pathlib.Path(__file__).parent
network_dir = repo_dir / 'networks'
slug_dir = network_dir / args.slug
slug_dir.mkdir(exist_ok=True, parents=True)

print("Downloading rollup.json")
try:
    rollup = fetch_data(ROLLUP_API_PATH, args.slug)
    with open(slug_dir / 'rollup.json', 'wb') as f:
        f.write(rollup)
    print("Downloading genesis.json")
    genesis = fetch_data(GENESIS_API_PATH, args.slug)
    with open(slug_dir / 'genesis.json', 'wb') as f:
        f.write(genesis)
except Exception as e:
    print("Failed to download with exception:", e)
    print("Do you have the right network slug?")

print("Fetching bootnodes")
bootnodes = ''
try:
    bootnodes = fetch_data(BOOTNODES_API_PATH, args.slug).decode('utf-8')
except Exception as e:
    print("Failed to fetch bootnodes with exception:", e)
    print("Are external nodes enabled for this network?")
    exit(1)

print("Fetching static peers")
staticPeers = ''
try:
    staticPeers = fetch_data(STATICPEERS_API_PATH, args.slug).decode('utf-8')
except Exception as e:
    print("Failed to fetch static peers with exception:", e)
    print("Are external nodes enabled for this network?")
    exit(1)

try:
    env_file = ENV_TEMPLATE.format(rpc_url=f'https://rpc-{args.slug}.{CONDUIT_RPC_SUFFIX}', bootnodes=bootnodes, staticPeers=staticPeers)
    with open(slug_dir / '.env', 'w') as f:
        f.write(env_file)
except Exception as e:
    print("Unable to write configuration:", e)
    exit(1)