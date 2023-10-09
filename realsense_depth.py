import pyrealsense2 as rs
import numpy as np

class DepthCamera:
    def __init__(self):
        self.W = 640
        self.H = 480
        self.FPS = 30

        # Configure depth and color streams
        config = rs.config()

        config.enable_stream(rs.stream.depth, self.W, self.H, rs.format.z16, self.FPS)
        config.enable_stream(rs.stream.color, self.W, self.H, rs.format.bgr8, self.FPS)

        # Start streaming
        print("[INFO][Realsense] Start streaming...")
        self.pipeline = rs.pipeline()
        self.profile = self.pipeline.start(config)

        self.aligned_stream = rs.align(rs.stream.color) # alignment between color and depth
        self.point_cloud = rs.pointcloud()
    
    def get_camera_intrinsics(self):
        # get camera intrinsics
        return self.profile.get_stream(rs.stream.color).as_video_stream_profile().get_intrinsics()

    def get_frame(self):
        frames = self.pipeline.wait_for_frames()
        frames = self.aligned_stream.process(frames)
        depth_frame = frames.get_depth_frame()
        color_frame = frames.get_color_frame()

        points = self.point_cloud.calculate(depth_frame)
        
        if not depth_frame or not color_frame:
            return None, None, None
        return points, depth_frame, color_frame

    def release(self):
        print("[INFO][Realsense] Stop streaming.")
        self.pipeline.stop()