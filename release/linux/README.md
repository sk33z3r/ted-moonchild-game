# Ted Moonchild and the Roadies in Space

## Ways to play on Linux

### Docker

If you have `docker-compose` installed on your system:

```
$ ./run-game.sh
```

If you only want to use the `docker run` command:

```
$ ./run-game.sh docker
```

### Python

If you don't want to mess with Docker and already have a Python environment installed, first install the modules:

```
$ pip install colorama
```

Then you can run the game:

```
$ python main.py
```