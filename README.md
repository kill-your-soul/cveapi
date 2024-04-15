# CVE API

### Prerequisites 
1. Docker
2. python

### Run
1. Run server and api 
```commandline
docker compose up --build -d core db redis celery-worker
```

3. Run migrations
```commandline
docker compose exec core alembic upgrade head
```

4. Run init script, it tooks alot of time(up to 80 minutes, meybe more)
```commandline
docker compose up init
```

5. Run celery beat for update 
```commandline
docker compose up celery-beat -d
```