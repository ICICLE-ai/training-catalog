---
tags:
  - Food-Access
  - Smart-Foodsheds
title: "FEAST: How-To Guides"
sidebar_label: "How-To Guides"
pagination_label: "How-To Guides"
description: "How-To Guides for FEAST. The Food Equity Access Simulation Technology (FEAST) tool — previously known as the Food Access and Strategy Simulation (FASS) tool —…"
---
# How-To Guides

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

1. Select the store(s) you want to remove (e.g., "Charlie’s Market"). To select multiple stores,
hold down the shift or command key as you select. To deselect stores, click on the map.
2. Click the "Remove Store" button.
3. Confirm the removal. The store(s) will disappear from the map.
4. Use the Step Function to evaluate the effects of this change on household food access.

## How to Call the API Programmatically

The backend is a FastAPI service and ships with a machine-readable OpenAPI
specification so you can generate clients, import endpoints into tools like
Postman or Insomnia, or wire FEAST into other ICICLE components.

- **Static spec file:** [`openapi.json`](https://github.com/ICICLE-ai/Food-Access-Model/blob/main/openapi.json) in the repo root. Re-generate
  it from the live app with:
  ```sh
  uv run python -c "from food_access_model.main import app; import json; print(json.dumps(app.openapi(), indent=2))" > openapi.json
  ```
- **Live interactive docs:** when the server is running, Swagger UI is served at
  `/docs` and ReDoc at `/redoc`. For the ICICLE deployment this is
  `https://fassback.pods.icicleai.tapis.io/docs`.

All endpoints are grouped under `/api` (for example `GET /api/simulation-instances`).
Every endpoint accepts an optional `Authorization: Bearer <Tapis token>` header:

- With no header, the caller sees the shared public pool of simulation instances
  (any row with `owner_id IS NULL`). This is the same behavior as pre-#102.
- With a valid Tapis token, the caller sees ONLY the instances they own; writes
  are stamped with `owner_id = <token sub>`.

Minimal curl example (replace `$TOKEN` with your Tapis token from
`https://icicleai.tapis.io`):

```sh
curl -H "Authorization: Bearer $TOKEN" \
     https://fassback.pods.icicleai.tapis.io/api/simulation-instances
```

Health check (no auth):
```sh
curl https://fassback.pods.icicleai.tapis.io/api/health
```

## Tips for Effective Use

- Analyze Community Needs: Before making changes, review community-level data to
target areas with low food access.
- Simulate Iteratively: Run multiple steps to identify trends and long-term effects.

### Troubleshooting Common Issues
**"Simulation taking forever"**
- **Normal:** Large simulations (50k+ households) can take 10-30 minutes per step
- **Solution:** Use reduced sample size

By using the FEAST simulation tool, you can make informed decisions to
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

4. Get a free API Key at [https://api.census.gov/data/key_signup.html](https://api.census.gov/data/key_signup.html). This is only necessary if you want to create new data. The current database will hold brown county data.

5. create a file `.env` at the root and enter your API in `config.py`
   ```py
   API_KEY=[CENSUS API KEY (optional)]
   DB_NAME=[NAME OF DATABASE]
   DB_USER=[DATABASE USER NAME]
   DB_PASS=[DATABASE PASSWORD]
   DB_HOST=[DATABASE HOST]
   DB_PORT=[DATABASE PORT FOR DATABASE]
   ```

### Optional per-request user scoping (#102)

Every API endpoint accepts an optional `Authorization: Bearer <token>` header.
With no header, the request sees the shared public pool (`simulation_instances`
rows where `owner_id IS NULL`) and all pre-scoping behavior is preserved.
With a header, the token is verified via JWKS (`food_access_model/api/token_verification.py`)
and the request sees ONLY instances owned by that user — public instances are
not mixed in. "Exists but not yours" and "doesn't exist" both return 404 so
ownership doesn't leak.

Verification is JWKS-backed via `pyjwt[crypto]` and config-driven via env vars
(`JWT_JWKS_URL`, `JWT_ISSUER`, `JWT_AUDIENCE`, `JWT_USER_CLAIM`, `JWT_ALGORITHMS`).
When `JWT_JWKS_URL` is unset the verifier is a no-op that returns `None` for
every token — a local dev operator who doesn't want to stand up an OIDC
provider gets public-pool-only behavior, not trust-as-is. For the ICICLE/Tapis
deployment, point `JWT_JWKS_URL` at the Tapis JWKS (e.g.
`https://icicle.tapis.io/v3/tokens/.well-known/jwks.json`) and set
`JWT_ISSUER` to the matching token service URL. Tapis tokens have no `aud`
claim and `sub` is `username@tenant`, so leave `JWT_AUDIENCE` and
`JWT_USER_CLAIM` unset. See `.env.example` for the full config surface.

**Required manual DB migration for live databases.** This change adds a
nullable `owner_id TEXT` column to `simulation_instances` and scopes the
instance-name uniqueness per owner. New databases get both via the updated
`CREATE TABLE` in `preprocessing/get_data.py`. For databases that have
already been seeded and are not going to re-run preprocessing, run (requires
PostgreSQL 15+):

```sql
ALTER TABLE simulation_instances ADD COLUMN IF NOT EXISTS owner_id TEXT;
ALTER TABLE simulation_instances DROP CONSTRAINT IF EXISTS simulation_instances_name_key;
ALTER TABLE simulation_instances
    ADD CONSTRAINT simulation_instances_owner_name_key
    UNIQUE (owner_id, name) NULLS NOT DISTINCT;
```

Existing rows stay `NULL` on `owner_id` (public) which preserves the
pre-scoping shared-pool behavior for anything that already existed. The
constraint swap is why PG15+ is required: `NULLS NOT DISTINCT` keeps the
public pool uniquely-named without needing a separate catch for anonymous
collisions.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- USAGE EXAMPLES -->
## Usage

You can run this project on localhost with:
```sh
   uv run run.py
```
Beyond testing api calls, running this project and the front end service contained in the [FASS-Frontend](https://github.com/ICICLE-ai/FASS-Frontend) concurrently results in a user-experience
using data within the database.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- CONTRIBUTING -->
## Contributing

CONTRIBUTORS:

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Contributors
- [Steve](https://github.com/blue442)
- [Abanish](https://github.com/abanishkhatry) 
- [Oscar Almaraz](https://github.com/OscarA974)
- [Ira](https://github.com/irahande22)
- [Shrivas](https://github.com/shrivasshankar)
- [Sophia](https://github.com/schen625)
- [Edric](https://github.com/MiniMiniFridge)
- [Tanish Upakare](https://github.com/tanishhh2077)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/ICICLE-ai/Food-Access-Model.svg?style=for-the-badge
[contributors-url]: https://github.com/ICICLE-ai/Food-Access-Model/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/ICICLE-ai/Food-Access-Model.svg?style=for-the-badge
[forks-url]: https://github.com/ICICLE-ai/Food-Access-Model/network/members
[stars-shield]: https://img.shields.io/github/stars/ICICLE-ai/Food-Access-Model.svg?style=for-the-badge
[stars-url]: https://github.com/ICICLE-ai/Food-Access-Model/stargazers
[issues-shield]: https://img.shields.io/github/issues/ICICLE-ai/Food-Access-Model.svg?style=for-the-badge
[issues-url]: https://github.com/ICICLE-ai/Food-Access-Model/issues
[license-shield]: https://img.shields.io/github/license/ICICLE-ai/Food-Access-Model.svg?style=for-the-badge
[license-url]: https://github.com/ICICLE-ai/Food-Access-Model/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/linkedin_username
[product-screenshot]: images/screenshot.png
[Next.js]: https://img.shields.io/badge/next.js-000000?style=for-the-badge&logo=nextdotjs&logoColor=white
[Next-url]: https://nextjs.org/
[React.js]: https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB
[React-url]: https://reactjs.org/
[Vue.js]: https://img.shields.io/badge/Vue.js-35495E?style=for-the-badge&logo=vuedotjs&logoColor=4FC08D
[Vue-url]: https://vuejs.org/
[Angular.io]: https://img.shields.io/badge/Angular-DD0031?style=for-the-badge&logo=angular&logoColor=white
[Angular-url]: https://angular.io/
[Svelte.dev]: https://img.shields.io/badge/Svelte-4A4A55?style=for-the-badge&logo=svelte&logoColor=FF3E00
[Svelte-url]: https://svelte.dev/
[Laravel.com]: https://img.shields.io/badge/Laravel-FF2D20?style=for-the-badge&logo=laravel&logoColor=white
[Laravel-url]: https://laravel.com
[Bootstrap.com]: https://img.shields.io/badge/Bootstrap-563D7C?style=for-the-badge&logo=bootstrap&logoColor=white
[Bootstrap-url]: https://getbootstrap.com
[JQuery.com]: https://img.shields.io/badge/jQuery-0769AD?style=for-the-badge&logo=jquery&logoColor=white
[JQuery-url]: https://jquery.com
