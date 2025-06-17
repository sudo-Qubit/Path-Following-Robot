import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/mazino/Path-Following-Robot/install/teleop_twist_keyboard'
