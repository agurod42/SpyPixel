# Spypixel

Spypixel is a lightweight spy pixel server crafted using Flask and SQLite, designed to provide simple yet effective tracking capabilities.

## How to run the server

### .env

Create a .env file in the src/ directory with the following variables:

```bash
SECRET_KEY=your_secret_key
DATABASE_URL=sqlite:///site.db
ADMIN_PASSWORD=your_admin_password
DOMAIN_NAME=yoyur_domain_name
```
### Dockerfile

Build and run the Docker container using the provided Dockerfile:

```bash
docker build -t spypixel .
docker run -p 5000:5000 -v .:/app spypixel
```

## Screenshots

#### Login

![login](login.png)

#### Create a pixel

![create a pixel](create_pixel.png)

#### View pixels

![view pixels](view_pixels.png)

#### View logs

![logs](logs.png)

---
Enhance your tracking capabilities effortlessly with Spypixel!