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

- ros2_ws/src/panda_ros2 : (forked) `https://github.com/eric-mjk/_forked_panda_ros2.git`

- thinkgrasp/Thinkgrasp : (forked) `https://github.com/eric-mjk/_forked_ThinkGrasp.git`

- ros2_ws/src/pymoveit2 : `https://github.com/AndrejOrsula/pymoveit2.git`


docker images

`https://hub.docker.com/repository/docker/ericmjk/panda_ws/general`

`https://hub.docker.com/repository/docker/ericmjk/panda_thinkgrasp/general`
