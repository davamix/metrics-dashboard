## Metrics dashboard (WIP)

Build:
```
docker-compose build
```

Run:
```
docker-compose up
```

GET 
```
curl http://127.0.0.1:5000/board
```

POST
```
curl -d '{"value":5}' -H "Content-Type: application/json" -X POST http://127.0.0.1:5000/board
```