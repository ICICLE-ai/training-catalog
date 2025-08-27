---
tags:
  - Software
  - Digital-Agriculture
  - Animal-Ecology
  - Release 2025-08
---

# How-To Guides

### Quick Guide
```bash
# Clone the git repository
git clone https://github.com/ICICLE-ai/OpenPass.git

# Search for the cloned repository
cd OpenPass

# Run install.sh script inside the same directory
bash install.sh

# ⚠️Note: Don't worry if the application displays this error: error: Internal error occurred: unable to upgrade connection: container not found ("apache"). It will take some time and application will automatically processed with futher installation.

# ⚠️Note: OpenPass directory is only for installation. Once done the application must be controlled and runned from icicleEdge folder created inside the /home/icicle/icicleEdge/

# Check if pods are READ and in RUNNING state
kubecmd get pods

cd icicleEdge/ea1openpass/

# One all the pods are RUNNING
bash restartASU.sh

#Once all pods are in READY state run 
bash home/icicle/icicleEdge/ea1openpass/startWebsite.sh
```

```bash
# If application already installed
cd icicleEdge
cd ea1openpass/restartMicroservices.sh

# Check if pods are READ and in RUNNING state
kubecmd get pods

# One all the pods are RUNNING
bash restartASU.sh

#Once all pods are in READY state run 
bash home/icicle/icicleEdge/ea1openpass/startWebsite.sh
```


After running the startWebsite.sh you can see this dashborad:
![](https://raw.githubusercontent.com/ICICLE-ai/OpenPass/dev/docs/images/dashboard.png)

Note: OpenPass offers several missions that can be used for data collection. These include missions utilizing GPS as well as movement-based (X,Y,Z axis) missions. OpenPass also provides an Orthomosaic Mission, which generates an orthomosaic of one acre of land. Each mission has its own description displayed on its respective button. Once you click on the mission button you can also have a look at the detailed description of the mission.  

We are currently working on and testing missions that support YOLO libraries, enabling real-time object detection during mission execution on OpenPass.
## Overview

This installation script automates the deployment of OpenPASS and its required dependencies on edge computing devices, specifically configured for laptop-based implementations. The system establishes a complete microservice environment with containerized applications, networking configuration, and essential development tools.

## Installation Process

### System Configuration
The installation begins by configuring the Ubuntu system to optimize performance for edge computing operations. The script disables system hibernation, sleep modes, and screen locking features that could interfere with continuous microservice operations. These modifications ensure uninterrupted service availability during extended operational periods.

### Package Installation
The script installs a comprehensive set of software packages required for the OpenPASS ecosystem. Core components include Docker for containerization, Python 3 for application development, Git for version control, and various networking utilities. Additional packages support database connectivity through MariaDB libraries and multimedia processing capabilities via SDL2 libraries.

### Network Configuration
A critical component of the installation involves DNS resolution configuration. The script replaces the default systemd-resolved service with traditional resolv.conf configuration, pointing to Google's public DNS servers (8.8.4.4). This change ensures reliable network connectivity for containerized services and external API communications.

### Development Environment Setup
The installation configures Git with default user credentials and repository settings, establishing a standardized development environment. Helm package manager installation through Snap provides Kubernetes application deployment capabilities essential for microservice orchestration.

### Repository and File Structure
The script clones the OpenPASS repository from GitHub and establishes a structured directory hierarchy within the icicleEdge folder. This includes separate directories for binary executables, OpenPASS applications, and Helm configuration files. The installation creates convenient aliases for Kubernetes command-line operations.

### Network Interface Configuration
A virtual network interface (icl231) is created using Linux dummy network drivers, configured with a specific MAC address and IP address (192.168.231.231/24). This interface provides isolated networking capabilities for testing and development scenarios without requiring physical network hardware.

### Python Environment
The installation configures Python dependencies through pip3, installing specialized packages for software pilot operations, multimedia processing, and API development. These packages support the core functionality required for drone operations and data processing workflows.

### Security Configuration
SSH key management is automated through the installation script, copying necessary authentication credentials from the OpenPASS repository to the user's SSH directory. Proper file permissions are set to ensure secure access to remote repositories and services.

## Post-Installation Operations

### Microservice Initialization
The installation concludes by executing the microservice startup script, which initializes the core OpenPASS services and establishes the runtime environment. This automated startup ensures that all components are properly configured and ready for operational use.

### Verification Steps
Following successful installation, users should verify that Docker services are running, Kubernetes cluster is accessible through the kubecmd alias, and the virtual network interface is properly configured. The OpenPASS web interface should be accessible for mission planning and system monitoring.

## Repository Access

### Default Configuration
The installation uses the "stage" Git repository by default, providing read-only access to stable releases. This configuration ensures operational stability while preventing unauthorized modifications to core system components.

### Development Mode
Alternative repository access can be configured by passing parameters to the installation script, enabling development repository access with write permissions for system administrators and developers.

## Support Considerations

### System Maintenance
Regular updates should be performed through the established Git workflow, ensuring that security patches and feature enhancements are properly integrated. The modular architecture allows for selective component updates without full system reinstallation.

### Troubleshooting
Common installation issues typically relate to user permissions, network connectivity, or conflicting software packages. The script includes error checking for critical prerequisites, providing clear diagnostic messages when installation requirements are not met.

This installation framework provides a robust foundation for deploying OpenPASS on edge computing devices, supporting scalable drone operations and agricultural data processing workflows.
