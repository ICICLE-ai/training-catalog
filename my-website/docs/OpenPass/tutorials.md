---
tags:
  - Software
  - Digital-Agriculture
  - Animal-Ecology
---

# Tutorials

### Prerequisites
- Ubuntu (22.01 or higher)
- Libraries using apt-get: bash, curl, python3, git, and docker.
- Hardware: at least (1) 4 1.2 Ghz CPU cores, (2) 8 GB Ram, and (3) 256 GB storage.
- Parrot Anafi Drones
- K3s (Lightweight Kubernetes)
 
 
The installation requires an Ubuntu-based edge device with the following configurations:

**User Configuration**: The system must have a user account named "icicle" with passwordless sudo privileges to root access. This user account serves as the primary operator for the OpenPASS installation and ongoing operations.

**Directory Structure**: The installation expects the `/home/icicle` directory to exist and be accessible by the current user. Any existing `icicleEdge` directory will be removed and recreated during the installation process.

**Network Access**: The device requires internet connectivity for package downloads, Git repository access, and DNS resolution configuration.
