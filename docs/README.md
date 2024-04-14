# Spypixel

Spy pixel server based on a Dockerized simple flask app on python3.

# .env
First create a .env file in the `src/` directory with the following:
```bash
SECRET_KEY=your_secret_key
DATABASE_URL=sqlite:///site.db
ADMIN_PASSWORD=your_admin_password
```
Then run the Dockerfile:
```bash
docker build -t spypixel .
docker run -p 5000:5000 -v .:/app spypixel
```
