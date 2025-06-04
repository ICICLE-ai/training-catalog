---
tags:
  - CI4AI
---

# How-To Guides

## Try it Out

```sh
# Dependencies
sudo apt-get install -y curl runc bridge-utils iptables net-tools python3-venv sysstat containerd jq pkg-config cmake gcc g++ libssl-dev pkg-config libprotobuf-dev
# Rust, more at https://www.rust-lang.org/tools/install
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh

# Install non-apt dependencies and build Ilúvatar, assumes python3 exists
cd src/Ilúvatar/docs/examples
./sample_setup.sh
sudo ../../target/debug/iluvatar_worker -c ../../iluvatar_worker/src/worker.dev.json &
worker_pid=$(echo $!)
```

Register a function with the worker.

```sh
../../target/debug/iluvatar_worker_cli --address "127.0.0.1" --port 8079 register --name "hello" --version 1 --image "docker.io/alfuerst/hello-iluvatar-action:latest" --memory 128 --cpu 1
```

Invoke the newly registered function, passing custom arguments.

```sh
../../target/debug/iluvatar_worker_cli --address "127.0.0.1" --port 8079 invoke --name "hello" --version 1 -a name=`whoami`
```

Kill the worker running in the background.

```sh
sudo kill --signal SIGINT $worker_pid
```

You can run more advanced scenarios [here](https://github.com/COS-IN/iluvatar-faas/blob/gpu-support/src/Il%C3%BAvatar/docs/examples/README.md).