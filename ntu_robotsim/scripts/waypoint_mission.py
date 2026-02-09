#!/usr/bin/env python3
"""
Waypoint mission navigator using Nav2 Simple Commander API.
"""

import rclpy
from nav2_simple_commander.robot_navigator import BasicNavigator, TaskResult
from geometry_msgs.msg import PoseStamped
import time


def create_pose(x, y, theta):
    """Create a PoseStamped message."""
    pose = PoseStamped()
    pose.header.frame_id = 'map'
    pose.header.stamp = rclpy.time.Time().to_msg()
    pose.pose.position.x = x
    pose.pose.position.y = y
    pose.pose.position.z = 0.0

    # Convert theta (yaw) to quaternion
    # Simple 2D rotation: qz = sin(theta/2), qw = cos(theta/2)
    import math
    pose.pose.orientation.x = 0.0
    pose.pose.orientation.y = 0.0
    pose.pose.orientation.z = math.sin(theta / 2.0)
    pose.pose.orientation.w = math.cos(theta / 2.0)

    return pose


def main():
    rclpy.init()
    navigator = BasicNavigator()

    # Wait for Nav2 to be ready
    navigator.waitUntilNav2Active()

    # TODO: Define your waypoints here (x, y, theta)
    # Replace these coordinates with positions in your maze
    waypoints = [
        create_pose(1.0, 0.3, 0.0),      # Waypoint 1
        create_pose(2.0, 2.0, 1.57),     # Waypoint 2
        create_pose(-1.0, 2.0, 3.14),    # Waypoint 3
        create_pose(-1.0, -1.0, -1.57),  # Waypoint 4
        create_pose(0.0, 0.0, 0.0),      # Return to start
    ]

    print(f"Starting waypoint mission with {len(waypoints)} waypoints...")

    # Record start time
    mission_start = time.time()

    # Navigate through waypoints
    for i, waypoint in enumerate(waypoints, 1):
        print(f"\nNavigating to waypoint {i}/{len(waypoints)}")
        print(f"  Position: ({waypoint.pose.position.x:.2f}, "
              f"{waypoint.pose.position.y:.2f})")

        waypoint_start = time.time()

        # Send navigation goal
        navigator.goToPose(waypoint)

        # Wait for completion
        while not navigator.isTaskComplete():
            feedback = navigator.getFeedback()
            # TODO: You can print feedback here if desired
            time.sleep(0.1)

        waypoint_time = time.time() - waypoint_start

        # Check result
        result = navigator.getResult()
        if result == TaskResult.SUCCEEDED:
            print(f"  ✓ Reached waypoint {i} in {waypoint_time:.1f} seconds")
        elif result == TaskResult.CANCELED:
            print(f"  ✗ Waypoint {i} was canceled")
            print(f"    Aborting mission.")
            break
        elif result == TaskResult.FAILED:
            print(f"  ✗ Failed to reach waypoint {i}")
            print(f"    Aborting mission.")
            break

        # Brief pause before next waypoint
        time.sleep(1.0)

    mission_time = time.time() - mission_start
    print(f"\nMission completed in {mission_time:.1f} seconds")

    rclpy.shutdown()


if __name__ == '__main__':
    main()
