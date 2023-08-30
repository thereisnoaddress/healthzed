## Health-Zed
### The Canadian way of pronouncing `/healthz`

This is to stop my procrastination and actually start working on this project that I had envisioned for a long time :) 

### Goal: 
To create a project that works similar to the [Kubernetes /healthz endpoint](https://kubernetes.io/docs/reference/using-api/health-checks/), but instead of checking on pods, it checks on people!

### Inspiration:

Rohan <3 

### Running locally: 

1. `poetry install`
2. `pre-commit install`
3. Make sure you have AWS credentials in your .env file. Ask Chris to add your phone number to the list of AWS verified numbers and confirm an OTP. 
4. `uvicorn healthzed.endpoint:app --reload`

### Running Docker image 
1. Build docker image: 
` docker build --build-arg YOUR_ENV=production -t healthz:250823 .`
Note: you can use any name for `YOUR_ENV` and the image tag.
2. Run the docker container: 
` docker run -p 8000:8000 my-fastapi-app:latest`
Note: you can use any port as long as you define it in the `Dockerfile` and here after `-p`. 