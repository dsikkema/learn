To spin up container:

```
docker run --name dvd_rentals_pg -e POSTGRES_PASSWORD=davinci -d -p 5432:5432 postgres
```

then to start:
`docker start dvd_rentals_pg`

The script `reset_load_db.sh` will either reset the db (drop and re-restore it from zipped archive) or create it fresh.

Script requires env vars set for db name and connection details, I use direnv to store this, in `.envrc`

DB comes from https://neon.tech/postgresql/postgresql-getting-started/load-postgresql-sample-database

