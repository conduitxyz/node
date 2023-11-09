![Conduit](logo.png)

# Conduit node

Conduit provides fully-managed, production-grade rollups on Ethereum.

It currently supports Optimism’s open-source [OP Stack](https://stack.optimism.io/).

This repository contains the relevant Docker builds to run your own node on the specific Conduit network.

<!-- Badge row 1 - status -->

[![GitHub contributors](https://img.shields.io/github/contributors/conduitxyz/node)](https://github.com/conduitxyz/node/graphs/contributors)
[![GitHub commit activity](https://img.shields.io/github/commit-activity/w/conduitxyz/node)](https://github.com/conduitxyz/node/graphs/contributors)
[![GitHub Stars](https://img.shields.io/github/stars/conduitxyz/node)](https://github.com/conduitxyz/node/stargazers)
![GitHub repo size](https://img.shields.io/github/repo-size/conduitxyz/node)
[![GitHub](https://img.shields.io/github/license/conduitxyz/node?color=blue)](https://github.com/conduitxyz/node/blob/main/LICENSE)

<!-- Badge row 2 - links and profiles -->

[![Website conduit.xyz](https://img.shields.io/website-up-down-green-red/https/conduit.xyz.svg)](https://conduit.xyz)
[![Blog](https://img.shields.io/badge/blog-up-green)](https://conduit.xyz/blog)
[![Docs](https://img.shields.io/badge/docs-up-green)](https://conduit-xyz.notion.site/Documentation-a823096e3439465bb9a8a5f22d36638c)
[![Twitter Conduit](https://img.shields.io/twitter/follow/conduitxyz?style=social)](https://twitter.com/conduitxyz)

<!-- Badge row 3 - detailed status -->

[![GitHub pull requests by-label](https://img.shields.io/github/issues-pr-raw/conduitxyz/node.svg)](https://github.com/conduitxyz/node/pulls)
[![GitHub Issues](https://img.shields.io/github/issues-raw/conduitxyz/node.svg)](https://github.com/conduitxyz/node/issues)

### Hardware requirements

We recommend you have this configuration to run a node:

- at least 16 GB RAM
- an SSD drive with at least 200 GB free

### Troubleshooting

If you encounter problems with your node, please open a [GitHub issue](https://github.com/conduitxyz/node/issues/new/choose) or reach out on our [Discord](https://discord.com/invite/X5Yn3NzVRh):

### Supported networks

| Ethereum Network | Status | Slug |
|------------------| ------ | ---- |
| Zora Sepolia  | ✅     | zora-sepolia-0thyhxtf5e |
| PGN Sepolia  | ✅     | pgn-sepolia-i4td3ji6i0 |

### Usage

1. Download the network you want to run by using `download-config.py`. You will need to know the slug of the network. You can find this in the Conduit console. For example: `./download-config.py zora-sepolia-0thyhxtf5e`. Note: The external nodes feature must be enabled on the network for this to work.

2. Select the network you want to run (it should exist in the `networks` folder) and set `CONDUIT_NETWORK` env variable. Example:

```
# for Zora Goerli
export CONDUIT_NETWORK=zora-sepolia-0thyhxtf5e
```

3. Ensure you have an Ethereum L1 full node RPC available (not Conduit), and copy `.env.example` to `.env` setting `OP_NODE_L1_ETH_RPC`. If running your own L1 node, it needs to be synced before the specific Conduit network will be able to fully sync.

4. Run:

```
docker compose up --build
```

5. You should now be able to `curl` your Conduit node:

```
curl -d '{"id":0,"jsonrpc":"2.0","method":"eth_getBlockByNumber","params":["latest",false]}' \
  -H "Content-Type: application/json" http://localhost:8545
```

Note: Some L1 nodes (e.g. Erigon) do not support fetching storage proofs. You can work around this by specifying `--l1.trustrpc` when starting op-node (add it in `op-node-entrypoint` and rebuild the docker image with `docker compose build`.) Do not do this unless you fully trust the L1 node provider.

You can map a local data directory for `op-geth` by adding a volume mapping to the `docker-compose.yaml`:

```yaml
services:
  geth: # this is Optimism's geth client
    ...
    volumes:
      - ./geth-data:/data
```

### Snapshots

TBD

### Syncing

Sync speed depends on your L1 node, as the majority of the chain is derived from data submitted to the L1. You can check your syncing status using the `optimism_syncStatus` RPC on the `op-node` container. Example:

```
command -v jq  &> /dev/null || { echo "jq is not installed" 1>&2 ; }
echo Latest synced block behind by: \
$((($( date +%s )-\
$( curl -s -d '{"id":0,"jsonrpc":"2.0","method":"optimism_syncStatus"}' -H "Content-Type: application/json" http://localhost:7545 |
   jq -r .result.unsafe_l2.timestamp))/60)) minutes
```
