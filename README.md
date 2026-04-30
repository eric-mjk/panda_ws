# Panda_ws

1. Clone this repo
ex) to Eric/panda_ws

2. running the container
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

3. After cloning panda_ws (inside container)
```
git submodule update --init --recursive

sudo apt update
sudo apt install ros-humble-ros-testing
```

4. Colcon build inside ros2_ws

5. Run

- fake hardware
```
ros2 launch franka_moveit_config moveit.launch.py use_fake_hardware:=true load_gripper:=true
```

- isaac sim
```
ros2 launch franka_moveit_config moveit.launch.py use_isaac_sim:=true load_gripper:=false
```

```
ros2 launch franka_moveit_config moveit.launch.py use_isaac_sim:=true load_gripper:=true
```

<- for isaac sim run the sim.usda file first (this file is not on github)



(for reference)
docker images

`https://hub.docker.com/repository/docker/ericmjk/panda_ws/general`

`https://hub.docker.com/repository/docker/ericmjk/panda_thinkgrasp/general`
