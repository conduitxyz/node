ARG CELESTIA_NODE_VERSION=latest
FROM ghcr.io/celestiaorg/celestia-node:${CELESTIA_NODE_VERSION}

COPY --chmod=755 celestia-node-entrypoint /opt/conduit/bin/celestia-node-entrypoint
ENTRYPOINT [ "/opt/conduit/bin/celestia-node-entrypoint" ]
