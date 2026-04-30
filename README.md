# Panda_ws

running the container
```
docker run -it -d --net=host --ipc=host \
  -e ROS_DOMAIN_ID=0 \
  -e RMW_IMPLEMENTATION=rmw_fastrtps_cpp \
  -e FASTDDS_BUILTIN_TRANSPORTS=UDPv4 \
  -e DISPLAY=$DISPLAY \
  -e QT_X11_NO_MITSHM=1 \
  -v /tmp/.X11-unix:/tmp/.X11-unix:rw \
  --gpus all\
  --privileged\
  --name eric_panda\
  -v ~/Eric/panda_ws:/workspace \
  ericmjk/panda_thinkgrasp:sim
```

git clone 

- ros2_ws/src/panda_ros2 : (forked) `https://github.com/eric-mjk/_forked_panda_ros2.git`

- thinkgrasp/Thinkgrasp : (forked) `https://github.com/eric-mjk/_forked_ThinkGrasp.git`

- ros2_ws/src/pymoveit2 : `https://github.com/AndrejOrsula/pymoveit2.git`


docker images

`https://hub.docker.com/repository/docker/ericmjk/panda_ws/general`

`https://hub.docker.com/repository/docker/ericmjk/panda_thinkgrasp/general`
