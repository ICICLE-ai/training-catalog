---
tags:
  - Food-Access
---

# How-To Guides

Follow these steps in order to clone the repository, set up your environment, install dependencies, and generate the CSV files.

1. **Clone the Repository**  
   ```bash
   git clone https://github.com/ICICLE-ai/ag_routing_data_generator.git
   cd agricultural-routing-data-template
2. **Create a Python Virtual Environment**
    ```bash
    python3 -m venv venv
3. **Activate the Virtual Environment**
    - For macOS/Linux
        ```bash
        source venv/bin/activate
    - Windows/Powershell
        ```bash
        .\venv\Scripts\Activate.ps1
4. **Install Required Packages**
    ```bash
    pip install -r requirements.txt
5. **Run the Data Generator Script**
    ```bash
    python data_generator_script.py \
    --num_records 20 \
    --lat 44.3538510 \
    --lon -89.2031370 \
    --radius 400 \
    --locations_output locations.csv \
    --vehicles_output vehicles.csv
- --num_records: Total location rows to generate (including the fixed depot L001).

- --lat and --lon: Center coordinates (decimal degrees) for the fixed depot.

- --radius: Radius in miles around (lat, lon) to randomly generate additional locations.

- --locations_output: Output filename for locations.csv.

- --vehicles_output: Output filename for vehicles.csv.