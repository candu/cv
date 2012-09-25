# set up XHPy system, hook into UI libraries
from xhpy.init import register_xhpy_module
register_xhpy_module('cv.views')
register_xhpy_module('cv.ui')

# register signal handlers
# TODO: re-enable these. for now, we just want to find out how the
# through association looks so that we can use it in the correct manner...
#import signal_handlers
