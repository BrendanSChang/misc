# Express and MongoDB Setup with Docker Compose

This requires having node and docker installed.

To run the app: `docker-compose up`

To run the tests:

```
docker-compose -f docker-compose.yml -f docker-compose.test.yml \
    run --rm test
```

Note that the container has to be rebuilt (`docker-compose build`) each
time with the proper config.

- the config/ directory is currently not in use
- probably a good idea to have a .dockerignore containing any dotfiles,
  Dockerfiles, docker-compose files, node_modules, and other miscellaneous
  files that don't need to be copied over

