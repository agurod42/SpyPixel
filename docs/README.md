# Spypixel

Spy pixel server based on a Dockerized simple flask app on python3.

To run the Dockerfile:
```bash
docker build -t spypixel .
docker run -p 5000:5000 -v ./src:/app spypixel
```
