# set up XHPy system, hook into UI libraries
from xhpy.init import register_xhpy_module
register_xhpy_module('cv.views')
register_xhpy_module('cv.ui')

# register signal handlers
import signal_handlers
