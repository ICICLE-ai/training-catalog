---
tags:
  - Food-Access
  - Smart-Foodsheds
---

# How To Guide

## How To Use The Tool
Step 1: Adding a Store

1. Navigate to the Features Tab.
2. Select Add Store.
3. Enter the store details:
    - Name (e.g., "Charlie’s Market")
    - Type (e.g., supermarket or convenience store)
    - Location (choose a point on the map using latitude and longitude).
4. Confirm the addition. The new store will now appear on the map.

Step 2: Simulating Changes

- Use the Step Function to simulate changes over time:

    1. Click Step to advance the simulation by one period (currently represents one
    month).
    2. Monitor changes in household food access metrics.
    3. Repeat as needed to observe cumulative impacts over time.

Step 3: Removing a Store

1. Go to the Remove Store feature.
2. Select the store you want to remove (e.g., "Charlie’s Market").
3. Confirm the removal. The store will disappear from the map.
4. Use the Step Function to evaluate the effects of this change on household food access.

## Tips for Effective Use

- Analyze Community Needs: Before making changes, review community-level data to
target areas with low food access.
- Simulate Iteratively: Run multiple steps to identify trends and long-term effects.

By using the Food Access and Strategy Simulation tool, you can make informed decisions to
address food access challenges and create impactful solutions. Explore different scenarios,
monitor the outcomes, and leverage the tool’s insights to drive meaningful community
improvements. Should you need further support or wish to provide feedback, our team is here to
assist.

<!-- GETTING STARTED -->
## Getting Started

To get a local copy up and running follow these simple steps.

### Prerequisites

You will need python to run this application.

### Installation

1. Clone the repo
   ```sh
   git clone https://github.com/ICICLE-ai/Food-Access-Model.git
   ```

2. Switch to the appropriate branch
If you are running the application locally, then switch to the "reduced_household_request" branch.  If you are running the application in a production environment, then switch to the "staging" branch.
```sh
  git checkout reduced_household_request 
  ``` 

3. Install python dependencies from pyproject.toml
   ```sh
   pip install uv
   uv install
   ```

4. Get a free API Key at [https://api.census.gov/data/key_signup.html](https://api.census.gov/data/key_signup.html). This is only neccessary if you want to create new data. The current database will hold brown county data.

5. create a file `.env` at the root and enter your API in `config.py`
   ```py
   API_KEY=[CENSUS API KEY (optional)]
   DB_NAME=[NAME OF DATABASE]
   DB_USER=[DATABASE USER NAME]
   DB_PASS=[DATABASE PASSWORD]
   DB_HOST=[DATABASE HOST]
   DB_PORT=[DATABASE PORT FOR DATABASE]
   ```
<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- USAGE EXAMPLES -->
## Usage

You can run this project on localhost with:
```sh
   uv run run.py
```
Beyond testing api calls, running this project and the FASS-Frontend concurrently results in a user-experience
using data within the database.

<p align="right">(<a href="#readme-top">back to top</a>)</p>
