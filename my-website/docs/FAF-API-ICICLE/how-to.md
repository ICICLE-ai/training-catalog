---
tags:
  - Food-Access
  - Smart-Foodsheds
---

# How-to Guides

For a complete overview of how to use the API, please refer to the [API_README.md](https://github.com/ICICLE-ai/faf-api-ICICLE/blob/main/API_README.md) file located in the same directory. This file provides a detailed explanation of each endpoint, including:
- Required input parameters
- Returned data
- A description of the endpoint's functionality
- Example requests demonstrating the expected input format

**Note:** All POST request bodies must be formatted as **JSON**. For GET requests, parameters should be passed as query strings. 

The Swagger UI to the API is here https://fafserver.pods.icicleai.tapis.io/api/schema/swagger-ui/#/

---
## Setting Up Your Own Server
The retrieved values are then provided via endpoints defined in the `urls.py` and `views.py` files, both of which are housed within the `Rest_API` application. These endpoints interact with classes located at the base of the `src` directory, which are responsible for constructing queries sent to the database using the `faf_mapping.py` and `state_mapping.py` files.

It is advisable to create a Python virtual environment before installing the server dependencies. To accomplish this, execute the following command:
* For Linux & macOS users:
```python3 -m venv environment_name```
* For Windows Users:
 ```python -m venv environment_name```
 
To activate the virtual environment:
* On Linux & macOS, run:
```source environment_name/bin/activate```
* On Windows, run:
```environment_name\Scripts\activate```

After activating the environment, proceed by cloning this repository into the virtual environment.

The dependencies for the server are listed in the `QueryTool_Project/requirements.txt` file, with all versions kept up to date. The server is currently using Python version 3.8.10, but any Python version up to 3.12.3 is compatible. To install the dependencies, use the following command in the root directory of the server:
```pip install -r requirements.txt```

To run the server, ensure that the Python virtual environment is activated and all dependencies listed in `requirements.txt` are installed. Once these steps are completed, navigate to the root directory of the server and execute the following command:
```python3 manage.py runserver```

For Windows users, omit the `3` from the command, so use:
```python manage.py runserver```

If you would like the server to run on a specific port, use the following command:
```python3 manage.py runserver #.#.#.#:port_number"```
for example:
```python2 manage.py runserver 0.0.0.0:12121```

After this final step, the server should now be running. 

For local deployment, once the server is running, you can access the API documentation by visiting:
``` http://localhost:port_number/api/schema/swagger-ui/# ```
Replace PORT with the port number you're using (e.g., 12121).
