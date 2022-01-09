#!/usr/bin/env bash

case $1 in
    linux)
        echo "Building Linux Release..."
        echo "Cleaning up old builds..."
        if [ -f ../ted-moonchild-linux* ]; then rm ../ted-moonchild-linux*; fi
        cp ../*.py linux/
        cd linux
        tar zcvf ../../ted-moonchild-linux_$(git rev-parse --short HEAD).tar.gz *
        echo "Cleaning up files..."
        rm *.py
        cd ..
        echo "md5checksum: $(md5sum ../ted-moonchild-linux* | awk '{print $1}')"
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