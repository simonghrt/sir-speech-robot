#! /usr/bin/env python
# -*- coding: utf-8 -*-

import math
import rospy
import sys
from geometry_msgs.msg import Twist
import speech_process as sp
import pickle

def main(stdscr, persist):
    pub = rospy.Publisher('cmd_vel', Twist, queue_size=1)
    rospy.init_node('voice_teleop', anonymous=True)
    rate = rospy.Rate(10) 
    twist = Twist()
    voicecode = -1
    # load pickle file ici
    stdscr.addstr("Command\n")
    stdscr.addstr(" - EN AVANT    : control linear x  (+= or -=)\n")
    stdscr.addstr(" - A GAUCHE/A DROITE        : control angular z (+= or -=)\n")
    stdscr.addstr(" - STOP    : reset of the twist\n")
    stdscr.addstr(" - ESC        : reset twist and exit\n")
    # We set the "wait for a key press" period to 100 ms. 
    if(persist): stdscr.timeout(100)
    while (not rospy.is_shutdown()) and (keycode != 27): # 27 is escape
        keycode = stdscr.getch()         # Wait for a key press for at most 100ms
        if   voicecode == -1               : pass # No key has been pressed, we keep current twist.
        elif keycode == curses.KEY_UP    : twist.linear.x  = twist.linear.x  + .1
        elif keycode == curses.KEY_DOWN  : twist.linear.x  = twist.linear.x  - .1
        elif keycode == curses.KEY_LEFT  : twist.linear.y  = twist.linear.y  + .1
        elif keycode == curses.KEY_RIGHT : twist.linear.y  = twist.linear.y  - .1
        elif keycode == 101              : twist.angular.z = twist.angular.z + .2
        elif keycode == 114              : twist.angular.z = twist.angular.z - .2
        else                             : twist = Twist()
        pub.publish(twist)
        rate.sleep()

# Starts curses (terminal handling) and run our main function.
if __name__ == '__main__':
    persist = '--persist' in rospy.myargv(argv=sys.argv)
    # ajouter args pour choix fichier wav 
    try:
       #curses.wrapper(lambda w: main(w,persist))
	# ici définir les étapes du processing
    except rospy.ROSInterruptException:
        pass
