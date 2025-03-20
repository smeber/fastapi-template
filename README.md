# fastapi-template

Template repo for FastAPI. Includes CI/CD on Azure Web App using Github Actions. Uses [Poetry](https://python-poetry.org/) for dependency management.

### Setup and run locally

1. Clone the repo: `git clone https://github.com/jmargutt/fastapi-template.git`.
2. Change code as needed.
3. Add needed environment variables to `.env` file.
> [!WARNING]  
> Do not store credentials/passswords/keys in the code, use the `.env` file instead.
> This file will not be pushed to the repository, as it is listed in the `.gitignore` file, so your credentials 
> won't be exposed.
4. Add needed packages to `pyproject.toml`, under `[tool.poetry.dependencies]`.
5. Run `pip install poetry` to install poetry.
5. Run `poetry install` to install the packages (or `python -m poetry install`, if `poetry` command is not found).
6. Run `poetry run uvicorn main:app --reload` to start the server  (or `python -m poetry run uvicorn main:app --reload`, if `poetry` command is not found)
7. Go to `http://127.0.0.1:8000/docs` and test if the app runs as expected.

### Development Tips
1. Use a linter to check the code for errors and style issues (usually already built-in in your IDE of choice).
2. Use a formatter (I like [Black](https://marketplace.visualstudio.com/items?itemName=ms-python.black-formatter)) to automatically format the code.
3. Add [tests for your endpoints](https://fastapi.tiangolo.com/tutorial/testing/). Use a dedicated directory (`/tests`).
4. Don't cram everything into the `main.py` file! Use separate files and directory for routers, models, etc. This will make your code more understandable and maintainable. See e.g. [kobo-connect](https://github.com/rodekruis/kobo-connect).

### Deploy to Azure with GitHub Actions

1. Create a new App Service Plan in Azure, or choose a pre-existing one.
2. Create a new Web App in Azure:
   * choose a meaningful name, e.g. `fastapi-template-jacopo`
   * select `Operating System`: `Linux`
   * select `Region`: `West Europe`
   * select the App Service Plan you created in step 1
   * Create the Web App
3. Enable basic authentication
   * Go to the Web App in the Azure portal
   * Under `Settings`, select `Configuration` -> `General settings` -> `Platform settings`
   * Set `SCM Basic Auth Publishing Credentials` to `On`
   * Set `FTP Basic Auth Publishing Credentials` to `On`
   * Save the changes
   * Go back to the `Overview` and click `Restart`
3. Get a Web App Publish Profile, to deploy from GitHub
   * Go to your app service in the Azure portal. 
   * On the Overview page, select `Download publish profile`. 
   * Save the downloaded file. You'll use the contents of the file to create a GitHub secret.
1. Create a new Azure Container Registry or choose a pre-existing one.
   * Go to the registry -> `Access keys` -> Enable `Admin user` -> Copy the username and password
3. Give permissions to the Web App to access the Container Registry
   * Go to your app service in the Azure portal.
   * Under `Configuration`, update the `Application settings`:
     * `DOCKER_REGISTRY_SERVER_URL`: the URL of the Azure Container Registry, e.g. `fastapiregister.azurecr.io`
     * `DOCKER_REGISTRY_SERVER_USERNAME`: the username of the Azure Container Registry, e.g. `fastapiregister`
     * `DOCKER_REGISTRY_SERVER_PASSWORD`: the password of the Azure Container Registry
> [!IMPORTANT]  
> These `Application settings` determine which environment variables are accessible by the web app. 
> If you change/add environment variables in the GitHub repository, don't forget to update the Web App `Configuration` in the Azure portal.

8. Create the GitHub secrets and variables, so that GitHub Actions can deploy to Azure
   * Go to your GitHub repository
   * Go to `Settings` -> `Secrets and variables` -> `Actions` -> `New repository secret`
   * Add the following **repository secrets**:
     * `AZURE_WEBAPP_PUBLISH_PROFILE`: the contents of the downloaded file from step 3
     * `REGISTRY_PASSWORD`: the password of the Azure Container Registry
   * Go to `Settings` -> `Secrets and variables` -> `Actions` -> `New repository variable`
   * Add the following **repository variables**:
     * `AZURE_WEBAPP_NAME`: the name of your web app, e.g. `fastapi-template-jacopo`
     * `REGISTRY_NAME`: the name of the Azure Container Registry, e.g. `fastapiregister`
5. Push a change to the repository to trigger the GitHub Actions workflow.
4. Wait 5-10 minutes, then go to `<my-api-name>.azurewebsites.net` and see the app running.
5. If the app is not running
   * Go to the `Actions` tab in your GitHub repository and check the logs of the failed workflow.
   * Go to the `Overview` tab of your Web App in the Azure portal and check `Deployment logs` -> `Logs`.
