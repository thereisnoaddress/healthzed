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
4. `uvicorn endpoint:app --reload`