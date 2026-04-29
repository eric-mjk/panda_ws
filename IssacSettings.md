# Isaac Sim ↔ ROS 2 Topic Flow

```
Isaac Sim                    topic_based_ros2_control         ros2_control stack
─────────────────────────────────────────────────────────────────────────────────

PublishJointState ──────► /isaac_joint_states ──────► read()  ──► JointStateBroadcaster ──► /joint_states
                                                                                                    │
                                                                                          robot_state_publisher
                                                                                          move_group (planning scene)

SubscribeJointState ◄───── /isaac_joint_commands ◄──── write() ◄── JointTrajectoryController ◄── move_group (execution)
```

## Key topic roles

| Topic | Direction | Who publishes | Who subscribes |
|---|---|---|---|
| `/isaac_joint_states` | Isaac → ROS | Isaac Sim (OmniGraph) | `topic_based_ros2_control` |
| `/isaac_joint_commands` | ROS → Isaac | `topic_based_ros2_control` | Isaac Sim (OmniGraph) |
| `/joint_states` | internal ROS | `joint_state_broadcaster` | `robot_state_publisher`, RViz, `move_group` |
| `/panda_arm_controller/follow_joint_trajectory` | internal ROS | `move_group` | `panda_arm_controller` |

## What each layer does

- **Isaac Sim OmniGraph**: physics simulation; exposes joint states and accepts position commands via the two `isaac_*` topics
- **`topic_based_ros2_control`**: thin bridge; maps those topics into the ros2_control hardware interface (`read()`/`write()` calls)
- **`JointTrajectoryController`**: interpolates trajectories; reads from move_group action server, writes position commands
- **`JointStateBroadcaster`**: re-publishes hardware state as standard `/joint_states` for the rest of ROS to consume
