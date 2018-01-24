#! /usr/bin/env python
# -*- coding: utf-8 -*-

import math
import rospy
import sys
from geometry_msgs.msg import Twist
import speech_process as sp
import pickle

def main():
    pub = rospy.Publisher('cmd_vel', Twist, queue_size=1)
    rospy.init_node('voice_teleop', anonymous=True)
    rate = rospy.Rate(10) 
    twist = Twist()
    data_folder = "/usr/users/promo2018/juge_rem/sir-speech-robot/data/" 
    ref_set = pickle.load(open(data_folder+'ref_set.pkl', 'rb'))
    voicecode = "undefined"
   # stdscr.addstr("Command\n")
   # stdscr.addstr(" - EN AVANT    : control linear x  (+= or -=)\n")
   # stdscr.addstr(" - A GAUCHE/A DROITE        : control angular z (+= or -=)\n")
   # stdscr.addstr(" - STOP    : reset of the twist\n")
   # stdscr.addstr(" - ESC        : reset twist and exit\n")
    # We set the "wait for a key press" period to 100 ms. 
   # if(persist): stdscr.timeout(100)
    f_wav = ""
    while (not rospy.is_shutdown()) and (f_wav != "exit"): # 27 is escape
	try:
	    f_wav = raw_input("Entrez un nom de fichier (sans l'extension, exit pour stopper): ")
	    data = [{"filename":f_wav + ".wav", "class":"unknown"}]
            processed_file = sp.compute_set(data_folder, data)
            voicecode = sp.predict(test_set=processed_file, reference_set=ref_set, verbose=True)
	except:
	    voicecode = None
	if   voicecode == -1              : pass # No key has been pressed, we keep current twist.
        elif voicecode == "forward"        : twist = Twist(); twist.linear.x  = twist.linear.x  + .1
        elif voicecode == "stop"           : twist = Twist()
        elif voicecode == "left"           : twist = Twist(); twist.angular.z = 0.2 
        elif voicecode == "right"          : twist = Twist(); twist.angular.z = -0.2
        else                               : twist = Twist()
        pub.publish(twist)
        rate.sleep()

# Starts curses (terminal handling) and run our main function.
if __name__ == '__main__':
   
    # f_wav = sys.argv[1]
    # persist = '--persist' in rospy.myargv(argv=sys.argv) 
    
    try:
        main()
    except rospy.ROSInterruptException:
        pass
