## Health-Zed
### The Canadian way of pronouncing `/healthz`

### Goal

To create a service that sends a ping to someone to check in on them and make sure they are alive. 

Inspired by the [Kubernetes /healthz endpoint](https://kubernetes.io/docs/reference/using-api/health-checks/), but instead of checking on pods, it checks on people! (Please don't sue me Kubernetes 😭 but I will rename if required)

### Inspiration

Rohan <3 

**Backstory**: When life gets overwhelming, we sometimes just want to disconnect and disappear from the world. It's a healthy (?) coping mechanism, but others might worry about our safety and / or liveliness. 

I wanted to create a simple service that has a low barrier of entry to make this easy to do. See _Stretch Goal_ to see the final form of this project.


### Live Demo (hosted on Render)

https://healthzed-on-render.onrender.com/docs

It should be up and running but it won't send texts because you need to verify your phone number with AWS SNS. 

Currently, only my phone number +16478611345 has been verified, so if you want to show me some love, you can spam me with some messages at that number and I can confirm that it's working :) 

### Running locally

1. `poetry install`
2. `pre-commit install`
3. Make sure you have AWS credentials in your .env file. Ask Chris to add your phone number to the list of AWS verified numbers and confirm an OTP. 
4. `uvicorn healthzed.endpoint:app --reload`

### Running in Docker

1. Build docker image: 

`docker build --build-arg YOUR_ENV=production -t healthzed:latest .`

Note: you can use any name for `YOUR_ENV` and the image tag (specified with `-t`).

2. Run the docker container: 

`docker run -p 8000:8000 healthzed:latest`

Note: you can use any port as long as you expose it in the `Dockerfile` and here after `-p`.

------

### Stretch Goal 
_Stretch goal_ and original vision: to create a companion hardware that will act as a receiver and acknowledge liveliness checks. 

It would be a very simple design so that it won't be distracting (like phones!) and it will have a low barrier of entry and no learning curve. It should just receive pings and have a button to acknowledge them. 

I initially envisioned it to look like my CO2 monitor with a screen and one button:

![image](https://github.com/thereisnoaddress/healthzed/assets/5344037/3cedd1ff-15c5-41e5-b8a4-58a042acfea0)

Maybe in future iterations, it will have multiple buttons to respond with "I'm okay but I don't want to talk" or "I'm okay and I want to talk but don't know how to reach out". And it'll probably look better. Maybe. If you've seen my sense of fashion, you probably know I can't design things that much better. Maybe I'll pay my friend Winnie to design something that I can prototype if she's not too busy at school. 

It would be cool to eventually get one working prototype that I can give to Rohan, but that's all hinging on me getting the software up and running first. Ah, this isn't Notion and not my personal journal, but I hope someone will find this idea releatable! 

