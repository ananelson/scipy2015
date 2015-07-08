set -e
export USERNAME=ananelson
export IMAGENAME=scipy2015
docker build -t $USERNAME/$IMAGENAME .
docker run -t -i \
    -v `pwd`:/home/repro/work \
    $USERNAME/$IMAGENAME /bin/bash
