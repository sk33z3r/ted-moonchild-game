# TMATRIS Releases

Currently, this process doesn't do much except package a lighter version of the game for use in Docker or Python `venv` on Unix systems.

## Usage

The script automates everything needed to package a release for each platform. Simply change to the release folder, and run the script. It will save the package into the `./build` directory.

Example Linux output:

```bash
$ cd ./release
$ ./release.sh [platform]
.. build output ..
```

## Linux

Example release run for Linux:

```bash
$ cd ./release
$ ./release.sh linux
Building Linux Release...
Cleaning up old builds...
art.py
battle.py
database.py
docker-compose.yml
Dockerfile
engine.old.py
engine.py
json/
json/enemies.json
json/locations_winnibego.json
json/locations_melvin.json
json/items.json
json/planets.json
json/locations_space.json
json/locations_jorlene.json
json/README.md
json/challenge_ratings.json
json/player.json
json/abilities.json
json/levels.json
main.py
README.md
requirements.txt
run-game.sh
world.py
Cleaning up files...
md5checksum: 5aca356d856317aeda771b6ed0cfe6b1
Build complete!
```

## Windows

Coming soon.

## macOS

Coming soon.
