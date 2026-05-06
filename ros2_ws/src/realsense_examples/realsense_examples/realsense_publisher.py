"""Publishes RealSense color and depth streams as ROS 2 topics."""

import numpy as np
import pyrealsense2 as rs
import rclpy
from cv_bridge import CvBridge
from rclpy.node import Node
from sensor_msgs.msg import CameraInfo, Image


class RealSensePublisher(Node):
    def __init__(self):
        super().__init__('realsense_publisher')

        self.declare_parameter('serial_no', '')       # empty = first device found
        self.declare_parameter('color_width', 1920)
        self.declare_parameter('color_height', 1080)
        self.declare_parameter('color_fps', 30)
        self.declare_parameter('depth_width', 640) # 640
        self.declare_parameter('depth_height', 480) # 480
        self.declare_parameter('depth_fps', 30)
        self.declare_parameter('enable_color', True)
        self.declare_parameter('enable_depth', True)
        self.declare_parameter('enable_aligned_depth', True)

        serial = self.get_parameter('serial_no').value
        color_w = self.get_parameter('color_width').value
        color_h = self.get_parameter('color_height').value
        color_fps = self.get_parameter('color_fps').value
        depth_w = self.get_parameter('depth_width').value
        depth_h = self.get_parameter('depth_height').value
        depth_fps = self.get_parameter('depth_fps').value
        self._enable_color = self.get_parameter('enable_color').value
        self._enable_depth = self.get_parameter('enable_depth').value
        self._enable_aligned = self.get_parameter('enable_aligned_depth').value

        # Aligned depth requires both streams.
        if self._enable_aligned and not (self._enable_color and self._enable_depth):
            self.get_logger().warn('enable_aligned_depth requires both color and depth — disabling')
            self._enable_aligned = False

        self._bridge = CvBridge()

        if self._enable_color:
            self._color_pub = self.create_publisher(Image, 'camera/color/image_raw', 10)
            self._info_pub = self.create_publisher(CameraInfo, 'camera/color/camera_info', 10)
        if self._enable_depth:
            self._depth_pub = self.create_publisher(Image, 'camera/depth/image_raw', 10)
        if self._enable_aligned:
            self._aligned_pub = self.create_publisher(Image, 'camera/aligned_depth_to_color/image_raw', 10)

        self._pipeline = rs.pipeline()
        config = rs.config()

        if serial:
            config.enable_device(serial)

        if self._enable_color:
            config.enable_stream(rs.stream.color, color_w, color_h, rs.format.bgr8, color_fps)
        if self._enable_depth:
            config.enable_stream(rs.stream.depth, depth_w, depth_h, rs.format.z16, depth_fps)

        profile = self._pipeline.start(config)

        device = profile.get_device()
        self.get_logger().info(f'Connected to: {device.get_info(rs.camera_info.name)} '
                               f'(s/n {device.get_info(rs.camera_info.serial_number)})')

        if self._enable_color:
            color_profile = profile.get_stream(rs.stream.color).as_video_stream_profile()
            self._camera_info = self._build_camera_info(color_profile.get_intrinsics())

        if self._enable_aligned:
            self._align = rs.align(rs.stream.color)

        # Drain a few frames so the camera is streaming before the timer fires.
        self.get_logger().info('Waiting for camera to stabilize...')
        for _ in range(5):
            self._pipeline.wait_for_frames(timeout_ms=5000)
        self.get_logger().info('Camera ready')

        timer_period = 1.0 / max(color_fps, depth_fps)
        self.create_timer(timer_period, self._timer_callback)

    def _timer_callback(self):
        try:
            frames = self._pipeline.wait_for_frames(timeout_ms=2000)
        except RuntimeError:
            self.get_logger().warn('Frame timeout — skipping', throttle_duration_sec=2.0)
            return

        now = self.get_clock().now().to_msg()

        if self._enable_color:
            color_frame = frames.get_color_frame()
            if color_frame:
                color_img = np.asanyarray(color_frame.get_data()).copy()
                # self.get_logger().info(f'Publishing color frame {color_img.shape} at {now.sec}.{now.nanosec:09d}')
                color_msg = self._bridge.cv2_to_imgmsg(color_img, encoding='bgr8')
                color_msg.header.stamp = now
                color_msg.header.frame_id = 'camera_color_optical_frame'
                self._camera_info.header.stamp = now
                self._color_pub.publish(color_msg)
                self._info_pub.publish(self._camera_info)

        if self._enable_depth:
            depth_frame = frames.get_depth_frame()
            if depth_frame:
                depth_img = np.asanyarray(depth_frame.get_data()).copy()
                # self.get_logger().info(f'Publishing depth frame {depth_img.shape} at {now.sec}.{now.nanosec:09d}')
                depth_msg = self._bridge.cv2_to_imgmsg(depth_img, encoding='16UC1')
                depth_msg.header.stamp = now
                depth_msg.header.frame_id = 'camera_depth_optical_frame'
                self._depth_pub.publish(depth_msg)

        if self._enable_aligned:
            aligned_frames = self._align.process(frames)
            aligned_depth = aligned_frames.get_depth_frame()
            if aligned_depth:
                aligned_img = np.asanyarray(aligned_depth.get_data()).copy()
                aligned_msg = self._bridge.cv2_to_imgmsg(aligned_img, encoding='16UC1')
                aligned_msg.header.stamp = now
                aligned_msg.header.frame_id = 'camera_color_optical_frame'
                self._aligned_pub.publish(aligned_msg)

    def _build_camera_info(self, intrinsics) -> CameraInfo:
        msg = CameraInfo()
        msg.header.frame_id = 'camera_color_optical_frame'
        msg.width = intrinsics.width
        msg.height = intrinsics.height
        msg.distortion_model = 'plumb_bob'
        msg.d = list(intrinsics.coeffs)
        fx, fy = intrinsics.fx, intrinsics.fy
        cx, cy = intrinsics.ppx, intrinsics.ppy
        msg.k = [fx, 0.0, cx, 0.0, fy, cy, 0.0, 0.0, 1.0]
        msg.r = [1.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 1.0]
        msg.p = [fx, 0.0, cx, 0.0, 0.0, fy, cy, 0.0, 0.0, 0.0, 1.0, 0.0]
        return msg

    def destroy_node(self):
        self._pipeline.stop()
        super().destroy_node()


def main(args=None):
    rclpy.init(args=args)
    node = RealSensePublisher()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
