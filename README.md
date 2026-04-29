# Panda_ws

running the container
```
docker run -it\
  -d \
  --gpus all \
  --ipc host \
  --net host \
  --privileged \
  -v /dev:/dev \
  -v /dev/bus/usb:/dev/bus/usb \
  --name panda \
  -e DISPLAY=$DISPLAY \
  -v /tmp/.X11-unix:/tmp/.X11-unix:rw \
  -v ~/Eric/panda_ws:/workspace \
  ericmjk/panda_ws:vanilla
```

git clone 

`https://github.com/tenfoldpaper/panda_ros2.git`

docker images

`https://hub.docker.com/repository/docker/ericmjk/panda_ws/general`

`https://hub.docker.com/repository/docker/ericmjk/panda_thinkgrasp/general`
