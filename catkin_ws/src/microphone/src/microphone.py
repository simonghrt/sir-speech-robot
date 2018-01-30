#!/usr/bin/env python
# license removed for brevity
import rospy
from std_msgs.msg import String

def talker():
    pub = rospy.Publisher('voice_message', String, queue_size=10)
    rospy.init_node('microphone', anonymous=True)
    rate = rospy.Rate(10) # 10hz
    while not rospy.is_shutdown():
        s = raw_input("Entrez un nom de fichier (sans l'extension, exit pour stopper): ")
        rospy.loginfo(s)
        pub.publish(s)
        rate.sleep()

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
