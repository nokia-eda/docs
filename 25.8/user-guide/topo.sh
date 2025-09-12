#!/bin/bash

# Usage:
#   topo.sh load <path to topology yaml>
#   topo.sh remove

# command/operation; either `load` or `remove`
CMD=${1}
# path to the topology yaml file (required for `load` command)
TOPO_YAML=${2}
# namespace where the topology configmap is stored (default: eda)
TOPO_NS=${TOPO_NS:-eda}
# namespace where the toolbox pod is running (default: eda-system)
CORE_NS=${CORE_NS:-eda-system}

if [[ "${CMD}" == "load" ]]; then
  if [ -z "${TOPO_YAML}" ]; then
    echo "Error: Path to topology YAML file is required for 'load'"
    exit 1
  fi
  if [ ! -f "${TOPO_YAML}" ]; then
    echo "Topology file ${TOPO_YAML} does not exist"
    exit 1
  fi
  echo "Loading topology from ${TOPO_YAML}"
  cat <<EOF | kubectl apply -n ${TOPO_NS} -f -
apiVersion: v1
kind: ConfigMap
metadata:
  name: eda-topology
data:
  eda.yaml: |
$(sed 's/^/    /' "${TOPO_YAML}")
EOF

elif [[ "${CMD}" == "remove" ]]; then
  echo "Removing topology from namespace ${TOPO_NS}"
  cat <<EOF | kubectl apply -n ${TOPO_NS} -f -
apiVersion: v1
kind: ConfigMap
metadata:
  name: eda-topology
data:
  eda.yaml: |
    {}
EOF

else
  echo "Usage:"
  echo "  $0 load <path to topology yaml> [TOPO_NS] [CORE_NS]"
  echo "  $0 remove [TOPO_NS] [CORE_NS]"
  exit 1
fi

kubectl -n ${CORE_NS} exec -it \
  $(kubectl get -n ${CORE_NS} pods \
  -l eda.nokia.com/app=eda-toolbox -o jsonpath="{.items[0].metadata.name}") \
  -- api-server-topo -n ${TOPO_NS}