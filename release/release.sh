#!/usr/bin/env bash

mkdir -p ./build
commit=$(git rev-parse --short HEAD)

case $1 in
    linux)
        echo "Building Linux Release..."
        echo "Cleaning up old builds..."
        if [ -f ./build/ted-moonchild-linux* ]; then rm ./build/ted-moonchild-linux*; fi
        cp ../*.py linux/
        cp -r ../json linux/
        cp ../dockerfiles/requirements.txt linux/
        cd linux
        tar zcvf ../build/ted-moonchild-linux_$commit.tar.gz *
        echo "Cleaning up files..."
        rm -r *.py json/
        cd ..
        echo "md5checksum: $(md5sum ./build/ted-moonchild-linux_$commit.tar.gz | awk '{print $1}')"
        echo "Build complete!"
    ;;
    windows)
        echo "Windows not implemented yet"
    ;;
    macos)
        echo "macOS not implemented yet"
    ;;
    *)
        echo "Invalid argument, expecting linux, windows or macos"
        exit 1
    ;;
esac