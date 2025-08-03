![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Vue](https://img.shields.io/badge/vuejs-35495E?style=for-the-badge&logo=vue.js&logoColor=4FC08D)
![TailwindCSS](https://img.shields.io/badge/tailwindcss-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white)
![Pinia](https://img.shields.io/badge/pinia-FFD859?style=for-the-badge&logo=pinia&logoColor=white)
![DjangoREST](https://img.shields.io/badge/DJANGO-REST-ff1709?style=for-the-badge&logo=django&logoColor=white&color=ff1709&labelColor=gray)
![Django](https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white)
![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)


# IMDB Clone - Django and Vue

I tried creating a clone of IMDB with some basic features like creating playlist, viewing details of movies and some more cool stuff. For getting the data it uses rapid-API.

# Screenshots

To be added later since there are changes to be done in the ui.

## Features

- Search for movies, get treding movies in countries.
- Create playlist, write reviews of movies you watched.
- Markdown support
- Basic Search Filtering
- Pagination

## Database

Postgres is used for the database configured in settings.py file insdie the Django app. Though it was not required, for the time being it still uses a Custom User model
since it is considered one of the best practices of starting out with Django.

## Docker deployment

Only build images without starting the services

```
docker-compose build
```

Run services in detached mode

```
docker-compose up -d
```

Start services without re-building the image

```
docker-compose up
```

To build images and start all the services

```
docker-compose up --build
```

After making changes to Nginx.conf file we can skip re-building the image

```
docker-compose down
docker-compose up -d
```

## Authors

* **Amit Prafulla (APFirebolt)** - [My Website](https://apgiiit.com)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details



