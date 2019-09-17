#!/usr/bin/env python
import rospy
from std_msgs.msg import String,Bool
import os
import time

class Logger:
    def __init__(self, experimentWaitDuration=0):
        self.hz = 40
        self.experimentWaitDuration = experimentWaitDuration

        self.log = {'nest':rospy.Subscriber('/nest/log',String,self.callback_log,queue_size=5),
                'robot1':rospy.Subscriber('/robot1/log',String,self.callback_log,queue_size=5)}
        
        self.ROStimeStep = 0#rospy.Time.now()
        
        self.pkg_path = '/home/turtlebot/catkin_ws/src/my_data_logger'
        self.experimentFolder = time.strftime('%Y-%m-%d/%H-%M-%S')
        self.resultLogPath = self.pkg_path + '/results/' + self.experimentFolder
        try:
            os.makedirs(self.resultLogPath)
        except FileExistsError:
            print self.resultLogPath + ' already exists!'

    def callback_log(self,data):
        robotID,logData = data.data.split(':')

        with open(self.resultLogPath + '/' + robotID + '.csv','a') as f:
            f.write('{:.4f}'.format(self.ROStimeStep) + ',' + logData+'\n')
    
    def loopLogger(self):
        rate = rospy.Rate(self.hz)
        pub_experimentStart = rospy.Publisher('/experimentStart',Bool,queue_size=1)
        time.sleep(self.experimentWaitDuration)

        t = rospy.Time.now().to_sec()
        while not rospy.is_shutdown():
            self.ROStimeStep = rospy.Time.now().to_sec() - t
            print self.ROStimeStep
            pub_experimentStart.publish(True)
            rate.sleep()

if __name__ == '__main__':
    experimentWaitDuration = 0
    node = rospy.init_node('my_data_logger',anonymous=True)
    logger = Logger(experimentWaitDuration=experimentWaitDuration)
    
    try:
        logger.loopLogger()
    except rospy.ROSInterruptException:
        pass
