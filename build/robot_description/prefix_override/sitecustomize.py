import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/enryu/Desktop/Path-Following-Robot/install/robot_description'
