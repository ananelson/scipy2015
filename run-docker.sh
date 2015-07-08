set -e

### "build"
export USERNAME=ananelson
export IMAGENAME=scipy2015
docker build -t $USERNAME/$IMAGENAME .

### "interactive"
docker run -t -i \
    -v `pwd`:/home/repro/work \
    $USERNAME/$IMAGENAME /bin/bash

### "hands-off"
#docker run \
#    -v `pwd`:/home/repro/work \
#    $USERNAME/$IMAGENAME
