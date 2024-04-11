# CVE API

### Prerequisites 
1. Docker
2. python

### Run
1. Run server and api 
```commandline
docker compose up core db redis celery-worker --build -d
```

3. Run migrations
```commandline
docker compose exec core alembic upgrade head
```

4. Run init script, it tooks alot of time(up to 30 minutes, meybe more)
```commandline
docker compose up init
```

5. Run celery beat for update 
```commandline
docker compose up celery-beat -d
```