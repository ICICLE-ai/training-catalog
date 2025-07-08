---
tags:
  - Animal-Ecology
  - Software
  - CI4AI
---

# How-To Guides

## Quick Start

To quickly start the application under [Docker](https://docs.docker.com/get-docker/) using docker-compose, follow these steps:

1. ./installer/install.sh $PWD ./installer/example_input.yml
2. cd test
3. docker-compose up
4. docker-compose down

## Support for NVIDIA
The Image Scoring plugin can make use of NVIDIA GPUs to improve the performance of object detection and classification with some ML models. In order to make use of NVIDIA GPUs in the Camera Traps application, the following steps must be taken:

1. *Ensure the NVIDIA drivers are installed natively on the machine*. For example, on Ubuntu LTS, follow the instructions in Section 3.1 [here](https://docs.nvidia.com/datacenter/tesla/tesla-installation-notes/index.html). Be sure to reboot your machine after adding the keyring and installing the drivers. You can check to see if the drivers are installed properly and communicating with the hardware by running the following command: 

```
nvidia-smi
```

2. *Install the NVIDIA Container Toolkit and configure the Docker Runtime*. See the instructions [here](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html). Make sure to restart Docker after installing and configuring the toolkit. To check if the toolkit and Docker are installed and configured correctly, run the following:

```
docker run --gpus=all --rm -it ubuntu nvidia-smi
```
The output should be similar to the output from Step 1.

3. *Update the Camera Traps Compose File to Use GPUs*. Starting with release 0.4, the installer includes options for making NVIDIA GPUs available to 
both the Image Scoring and Power Monitoring plugins. See the [Installer README](https://github.com/tapis-project/camera-traps/blob/main/installer/README.md) for more details.

## Using an MQTT Broker

If running configuring a run directory using the installer with `mode: demo`,
the `docker-compose.yml` file will be configured with to send detection events
to an MQTT broker. By default, it is expected that the broker is already
running on your local machine, although that can be changed in your configure
YAML file.

On linux, you can install and run with

```
sudo apt-get install mosquitto mosquitto-clients -y
sudo systemctl start mosquitto
```

On MacOS, it can be installed and run with HomeBrew with:

```
brew install mosquitto
brew services run mosquitto
```

To verify that detection events are flowing to the MQTT broker, you should be able to run

```
mosquitto_sub -t cameratrap/images -t cameratrap/events
```
on the same machine as the broker and see the events being printed to stdout.

Note: you may need to add the following mosquitto config file in order for the docker image to able to publish to the mqtt broker:

```
cat /etc/mosquitto/conf.d/my.conf
listener 1883 0.0.0.0
allow_anonymous true
```

## Developer Information

### Using Flatbuffers

In-memory representations of events are translated into flatbuffer binary streams plus a leading two byte sequence that identifies the event type.  These statically defined byte sequences are specified in the [events.rs](https://github.com/tapis-project/camera-traps/blob/main/src/events.rs) source file and repeated here for convenience.

// Each event is assigned a binary prefix that zqm uses to route incoming binary streams to all of the event's subscribers.
pub const NEW_IMAGE_PREFIX:           [u8; 2] = [0x01, 0x00];
pub const IMAGE_RECEIVED_PREFIX:      [u8; 2] = [0x02, 0x00];
pub const IMAGE_SCORED_PREFIX:        [u8; 2] = [0x03, 0x00];
pub const IMAGE_STORED_PREFIX:        [u8; 2] = [0x04, 0x00];
pub const IMAGE_DELETED_PREFIX:       [u8; 2] = [0x05, 0x00];
pub const PLUGIN_STARTED_PREFIX:      [u8; 2] = [0x10, 0x00];
pub const PLUGIN_TERMINATING_PREFIX:  [u8; 2] = [0x11, 0x00];
pub const PLUGIN_TERMINATE_PREFIX:    [u8; 2] = [0x12, 0x00];
pub const MONITOR_POWER_START_PREFIX: [u8; 2] = [0x20, 0x00];
pub const MONITOR_POWER_STOP_PREFIX:  [u8; 2] = [0x21, 0x00];

Each event sent or received begins with its two byte prefix followed by its serialized form as defined in the camera-traps flatbuffer definition file ([events.fbs](https://github.com/tapis-project/camera-traps/blob/main/resources/events.fbs)).  The following section describes how to generate Rust source code from this definition file, a similar process can be used for any language supported by flatbuffers.

### Updating the flatbuffers messages

Flatbuffers info: https://google.github.io/flatbuffers/

The flatbuffers messages schema is defined in the `resources/events.fsb` file. To change the message formats do the following:

1. Edit the `resources/events.fsb` file with your changes.
2. From the camera-traps directory, regenerate the `events_generated.rs` code with the command:

```
$ flatc --rust -o src resources/events.fbs
```

3. (Optional) Add the following line to the top of the `src/events_generated.rs` file so that clippy warnings are suppressed:

```
// this line added to keep clippy happy
#![allow(clippy::all)]
```

### Plugin Start and Stop Protocol

Each plugin is required to conform to the following conventions:

1. Register for the *PluginTerminateEvent*.
2. Send a *PluginStartedEvent* when it begins executing.
3. Send a *PluginTerminatingEvent* when it shuts down.

The *PluginStartedEvent* advertises a plugin's name and uuid when it starts.  When a plugin receives a *PluginTerminateEvent*, it checks if the event's *target_plugin_name* matches its name or the wildcard name (*).  If either is true, then the plugin is expected to gracefully terminate.  The plugin is also expected to gracefully terminate if the event's *target_plugin_uuid* matches the plugin's uuid.  Part of plugin termination is for it to send a *PluginTerminatingEvent* to advertise that it's shutting down, whether in response to a *PluginTerminateEvent* or for any other reason.

### Building and Running under Docker

The instructions in this section assume [Docker](https://docs.docker.com/get-docker/) (and docker-compose) are installed, as well as [Rust](https://www.rust-lang.org/tools/install), [cargo](https://doc.rust-lang.org/cargo/getting-started/installation.html) and make.

From the top-level camera-traps directory, issue the following command to build the application's Docker images:

make build
See [Makefile](https://github.com/tapis-project/camera-traps/blob/main/Makefile) for details.  Use the installer [install script](https://github.com/tapis-project/camera-traps/blob/main/installer/install.sh) to create a run directory. See the installer [README](https://github.com/tapis-project/camera-traps/blob/main/installer/README.md) for more details. Then, navigate to the new run directory. Issue the following command to run the application, including the external plugins for which it's configured:

docker-compose up
See [docker-compose.yaml](https://github.com/tapis-project/camera-traps/blob/main/installer/templates/docker-compose.yml) for details.  From the same release directory, issue the following command to stop the application:

docker-compose down

### Building and Running the Rust Code

If you're just interested in building the Rust, issue *cargo build* from the top-level camera-traps directory.  Alternatively, issue *cargo run* to build and run it.  External plugins are not started using this approach.  The internal plugins and their actions are configured using a *traps.toml* file, as discussed above.

### Integration Testing

The camera-traps/tests directory contains [integration_tests.rs](https://github.com/tapis-project/camera-traps/blob/main/tests/integration_tests.rs) program.  The integration test program runs as an external plugin configured via a *traps.toml* file as shown above.  See the top-level comments in the source code for details.

### Plugin Development

This section addresses two questions:

- Why would I want to create a plugin?
- What kind of plugin should I create?



One would want to create their own plugin if they wanted to read or write events and perform some new action that isn't currently implemented.  If an existing plugin doesn't do what you want, you have the option of modifying that plugin or creating another plugin that acts on the same events and does what you need.

For example, the *image_gen_plugin* injects new images into the event stream, the *image_recv_plugin* writes new images to file, etc.  The *observer_plugin* is one that subscribes to all events and logs them for debugging purposes.  Most of the time we don't run the *observer_plugin*, but if we want extended logging we just include it to run in the traps.toml file.  In this case, having a separate plugin from which we can customize the logging of all events is more convenient then adding that logging capability to each existing plugin.

Another reason for introducing a new plugin would be to also service new events.  As the application evolves new capabilities might require new events.  This occurred as we develop support for power monitoring, which introduces 2 new events and a plugin to handle them.

When implementing a plugin the choice between internal and external is often technology driven.  Do we want to write a plugin in Rust and compile it into the application (internal) or do we want to write it in some other language and start it up in its own container (external)?  Considerations as to which approach to take include performance, resource usage, and availability of domain-specific libraries.