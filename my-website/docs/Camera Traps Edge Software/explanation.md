---
tags:
  - Software
  - CI4AI
  - Animal-Ecology
title: "Camera Traps Edge Software: Explanation"
sidebar_label: "Explanation"
pagination_label: "Explanation"
description: "Explanation for Camera Traps Edge Software. The Camera Traps application is both a simulator and IoT device software for utilizing machine learning on the…"
---
# Explanation

## Architectual Overview
The actual camera-traps software consists of a set of tightly integrated plugins running on the same IoT device as separate containers (and thus, separate OS processes).

Camera-traps uses the [event-engine](https://github.com/tapis-project/event-engine) library to implement its plugin architecture and event-driven communication.  The engine uses [zmq](https://zeromq.org/) sockets to deliver events between senders and the subscribers interested in specific events.

The event-engine supports *internal* and *external* plugins.  Internal plugins are Rust plugins delivered with camera-traps and run in the camera-traps process.  External plugins are configured by camera-traps to run outside the camera-traps process and use a TCP port to send and receive events.  By using TCP, external plugins can be written in any language that supports the [flatbuffers](https://google.github.io/flatbuffers/) wire protocol.

## Application Configuration

The camera-traps application requires configuration through environment variables or configuration files.  When launching the application from a *releases* subdirectory, the specific release's *config* directory will contain the default configuration files for running a short simulation test.

In general, plugins can also depend on their own environment variables and/or configuration files, and the same is true of test programs.  The [releases](https://github.com/tapis-project/camera-traps/tree/main/releases) directory contains docker-compose files that use default configurations, which can serve as a template for production environment configuration.


| **Target**               | **Environment  Variable**     | **Default  File**        | **Notes**                         |
| -------------------------- | ------------------------------- | -------------------------- | ----------------------------------- |
| camera-traps application | TRAPS_CONFIG_FILE             | ~/traps.toml             | Can be 1st command line parameter |
| image_gen_plugin         |                               | /input.json              |                                   |
| video_generating_plugin  | TRAPS_VIDEO_OUTPUT_PATH       |                          |                                   | 
| image_detecting_plugin   |                               | /etc/motion/motion.conf  |
| detection_reporter_plugin| TRAPS_DETECTION_REPORTER_*    | /traps-detection.toml    |
| image_store_plugin       | TRAPS_IMAGE_STORE_FILE        | ~/traps-image-store.toml |                                   |
| power_measure_plugin     | TRAPS_POWER_LOG_PATH          | ~/logs                   |                                   |
| ckn_plugin               | TRAPS_CKN_OUTPUT_PATH         | ~/output                 |                                   |
| image_uploading_plugin   | TRAPS_UPLOAD_FILE             | /traps-upload.toml       |                                   |
| integration tests        | TRAPS_INTEGRATION_CONFIG_FILE | ~/traps-integration.toml |                                   |
| logger                   | TRAPS_LOG4RS_CONFIG_FILE      | resources/log4rs.yml     | Packaged with application         |

The external python plugins run in their own processes and do not currently use environment variables.

The camera-traps application uses [log4rs](https://docs.rs/log4rs/latest/log4rs/) as its log manager.  The log settings in [resources/log4rs.yml](https://github.com/tapis-project/camera-traps/blob/main/resources/log4rs.yml) source code will be used unless overridden by assigning a log4rs.yml configuration filepath to the TRAPS_LOG4RS_CONFIG_FILE environment variable.  To maximize logging, set root level to *trace* in the effective log4rs.yml file.  Also, include the *observer_plugin* in the internal plugins list in the effective traps.toml file.

## Plugin Configuration

Camera-traps uses a [TOML](https://toml.io/en/) file to configure the internal and external plugins it loads.  Internal plugins are registered with the event-engine by simply specfying their names since their runtime characteristics are compiled into the application.  External plugins, on the other hand, require more detailed information in order to be registered.  An up-to-date toml file is maintained with the installer in this [template file](https://github.com/tapis-project/camera-traps/blob/main/installer/templates/config/traps.toml). Here is an example resources/traps.toml file content:

> \# This is the camera-traps application configuration file for versions 0.x.y of the application.<br/>
> \# It assumes the use of containers and docker-compose as the deployment mechanism.<br/>
> title = "Camera-Traps Application Configuration v0.3.2"<br/>
>
> \# The event engine's publish and subscribe port used to create the event_engine::App instance.<br/>
> publish_port = 5559
> subscribe_port = 5560
>
> \# An absolute path to the image directory is required but a file name prefix is optional.<br/>
> \# If present the prefix is preprended to generated image file names.  This is the directory<br/>
> \# into which the image_recv_plugin writes incoming images and the image_store_plugin may<br/>
> \# delete images or output the scores for images.<br/>
> images_output_dir = "/root/camera-traps/images"<br/>
> \# image_file_prefix = ""
>
> \# The container for both internal and external plugins.  Internal plugins are written in rust<br/>
> \# and compiled into the camera-traps application.  External plugins are usually written in<br/>
> \# python but can be written in any language.  External plugins run in their own processes<br/>
> \# and communicate via tcp or ipc.<br/>
> [plugins]
> \# Uncomment the internal plugins loaded when the camera-traps application starts.<br/>
> internal = [<br/>
> \#    "image_gen_plugin",<br/>
> "image_recv_plugin",<br/>
> \#    "image_score_plugin",<br/>
> "image_store_plugin",<br/>
> \#    "observer_plugin"<br/>
> ]
>
> \# Configure each of the active internal plugins with the image processing action they should<br/>
> \# take when new work is received.  If no action is specified for a plugin, its no-op action<br/>
> \# is used by default.<br/>
> internal_actions = [<br/>
> "image_recv_write_file_action",<br/>
> "image_store_file_action"<br/>
> ]
>
> \# External plugins require more configuration information than internal plugins.<br/>
> \# Each plugin must subscribe to PluginTerminateEvent.<br/>
> \# <br/>
> \# Note that each plugin must specify the external port to use in TWO PLACES: here as well as<br/>
> \# in the docker-compose.yml file. If external_port changes here, it must ALSO be changed in the<br/>
> \# docker-compose.yml file.<br/>
> [[plugins.external]]<br/>
> plugin_name = "ext_image_gen_plugin"<br/>
> id = "d3266646-41ec-11ed-a96f-5391348bab46"<br/>
> external_port = 6000<br/>
> subscriptions = [<br/>
> "PluginTerminateEvent"<br/>
> ]<br/>
> [[plugins.external]]<br/>
> plugin_name = "ext_image_score_plugin"<br/>
> id = "d6e8e42a-41ec-11ed-a36f-a3dcc1cc761a"<br/>
> external_port = 6001<br/>
> subscriptions = [<br/>
> "ImageReceivedEvent",<br/>
> "PluginTerminateEvent"<br/>
> ]<br/>
> [[plugins.external]]<br/>
> plugin_name = "ext_power_monitor_plugin"<br/>
> id = "4a0fca25-1935-472a-8674-58f22c3a32b3"<br/>
> external_port = 6010<br/>
> subscriptions = [<br/>
> "MonitorPowerStartEvent",<br/>
> "MonitorPowerStopEvent",<br/>
> "PluginTerminateEvent"<br/>
> ]<br/>
> [[plugins.external]]<br/>
> plugin_name = "ext_power_control_plugin"<br/>
> id = "a59621f2-4db6-4892-bda1-59ecb7ff24ae"<br/>
> external_port = 6011<br/>
> subscriptions = [<br/>
> "PluginTerminateEvent"<br/>
> ]<br/>
> [[plugins.external]]<br/>
>   plugin_name = "ext_ckn_plugin"<br/>
>   id = "6e153711-9823-4ee6-b608-58e2e801db51"<br/>
>  external_port = 6011<br/>
> subscriptions = [<br/>
>       "ImageScoredEvent",<br/>
>       "ImageStoredEvent",<br/>
>       "ImageDeletedEvent",<br/>
>       "PluginTerminateEvent"<br/>
>   ]<br/>
>
>


Every plugin must subscribe to the PluginTerminateEvent, which upon receipt causes the plugin to stop.  Subscriptions are statically defined in internal plugin code and explicitly configured for external plugins.  External plugins also provide their predetermined UUIDs and external TCP ports.

Camera-traps looks for its configuration file using these methods in the order shown:

1. The environment variable $TRAPS_CONFIG_FILE.
2. The first command line argument.
3. $HOME/traps.toml

The first file it finds it uses.  If no configuration file is found the program aborts.

### Internal Plugin Configuration

The names listed in the *internal* list are the rust plugin file names.  These plugins run as separate threads in the camera-traps process.  The *internal_actions* list contains the file names that implement the different algorithms or actions associated with each internal plugin.

A naming convention is used to associate actions with their plugins:  An action name starts with its plugin name minus the trailing "plugin" part, followed by an action identifier part, and ends with "_action".  Each plugin has a no-op action that causes it to take no action other than, possibly, generating the next event in the pipeline.  For example, *image_gen_noop_action* is associated with the *image_gen_plugin*.

Internal plugins for which no corresponding action is specified are assigned their no-op plugin by default.

### image_recv_plugin

When *image_recv_write_file_action* is specifed, the *image_recv_plugin* uses the *image_dir* and *image_file_prefix* parameters to manage files.  The image_dir is the directory into which image files are placed.  Image file names are constructed from the information received in a NewImageEvent and have this format:

`<image_file_prefix><image_uuid>.<image_format>`
The *image_uuid* and *image_format* are from the NewImageEvent.  The image_file_prefix can be the empty string and the image_format is always lowercased when used in the file name.
