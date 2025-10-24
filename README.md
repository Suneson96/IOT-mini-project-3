# IOT-mini-project-3

## Dependencies

* Docker


## Running the project

### Starting
```Bash
docker compose up --build
```

### Stopping
```Bash
docker compose down
```

### Running DoS
Edit the `docker-compose.yml`file and uncomment the following section at the bottom:

```yaml
 client_dos:
    build: ./clients
    depends_on:
      fog:
        condition: service_healthy
    environment:
      - FOG_URL=http://fog:8000/upload
    command: [ "python", "client_dos.py" ]
```

Then start the project as usual.
