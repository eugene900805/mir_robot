#!/usr/bin/env python3
import rospy
from moveit_msgs.msg import MoveGroupActionGoal
import socket

# Socket setings
HOST = "192.168.0.102" # replace by the IP address of the UR robot
PORT = 63352 # PORT used by robotiq gripper

def callback(msg):
    # 從 goal_constraints 中找出目標 joint 的資料
    for constraint in msg.goal.request.goal_constraints:
        for joint_constraint in constraint.joint_constraints:
            if joint_constraint.joint_name == "ur5_robotiq_85_left_knuckle_joint":
                # rospy.loginfo("Joint position: %f", joint_constraint.position)
                # rospy.loginfo("Tolerance above: %f", joint_constraint.tolerance_above)
                # rospy.loginfo("Tolerance below: %f", joint_constraint.tolerance_below)

                # Socket communication
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.connect((HOST, PORT))
                    target = round(joint_constraint.position / (45/180*3.1415926) * 224 + 3)
                    s.sendall(bytes(f'SET POS {target}\n', encoding='utf-8'))

def listener():
    rospy.init_node('joint_value_listener', anonymous=True)
    rospy.Subscriber("/move_group/goal", MoveGroupActionGoal, callback)
    rospy.spin()

if __name__ == '__main__':
    listener()