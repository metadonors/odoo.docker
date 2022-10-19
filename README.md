# Odoo base Docker image

Clone this repository

```
$ git clone git@github.com:metadonors/odoo.docker.git
```

Enter project folder

```
$ cd odoo.docker
```

Initialize Odoo database

```
$ docker compose run odoo upgrade base
```

Run Odoo 

```
$ docker compose up
```

Open http://localhost/web with your browser and login with username **admin** and password **admin**
