import sys
import os
import logging

import monkeypatch

class LazyLogger( object ):
    def __init__( self, logger, level, args, kwargs ):
        self.logger = logger
        self.level = level
        self.args = args
        self.kwargs = kwargs

    def __rrshift__( self, other ):
        if isinstance( other, basestring ):
            other.log( self.logger, *self.args, level = self.level, **self.kwargs )
        else:
            super( LazyLogger, self ).__rrshift__( other )


##
class PrettyLogger( logging.Logger ):

    def __init__( self, *args, **kwargs ):
        if args and 1 == len( args ) and isinstance( args[ 0 ], logging.Logger ):
            self._logger = args[ 0 ]
        else:
            super( PrettyLogger, self ).__init( self, *args, **kwargs )

    def debug( self, *args, **kwargs ):
        return LazyLogger( self._logger, logging.DEBUG, args, kwargs )
    
    def info( self, *args, **kwargs ):
        return LazyLogger( self._logger, logging.INFO, args, kwargs )

    def warning( self, *args, **kwargs ):
        return LazyLogger( self._logger, logging.WARNING, args, kwargs )

    warn = warning

    def error( self, *args, **kwargs ):
        return LazyLogger( self._logger, logging.ERROR, args, kwargs )

    def critical( self, *args, **kwargs ):
        return LazyLogger( self._logger, logging.CRITICAL, args, kwargs )

    fatal = critical


#
def log( msg, logger, *args, **kwargs ):

    # explicit level, or from defaults
    level = kwargs[ "level" ]
    if not logger.isEnabledFor( level ):
        return None 

    msg = msg.strip()
    extra = kwargs.get( "extra", None )
    exc_info = kwargs.get( "exc_info", None )
    fn, lno, func, f_locals = find_caller()

    if args and len( args ) == 1 and isinstance( args[ 0 ], dict ) and args[ 0 ]:
        # sole argument is a dictionary, add the locals to the dictionary
        f_locals.update( args[ 0 ] )
        args = [ f_locals ]
    elif not args:
        # no arguments delivered, default to the locals dictionary
        args = [ f_locals ]

    record = logger.makeRecord( logger.name, level, fn, lno, msg, args, exc_info, 
        func, extra )
    logger.handle( record )
    return record.getMessage()


# borrowed from python's logging module
# unfortunately, python's logging module isn't robust or modular enough to 
# be easily extended in a prettier way.
def find_caller():
    """ Find the invoking code location of the log method, by looking up the 
    stack until there's a location outside of the prettylogs package """

    frame = sys._getframe() if hasattr( sys, "_getframe" ) else None
    if frame is None:
        try:
            # little trick for getting this frame from the exception traceback
            raise Exception 
        except:
            frame = sys.exc_info()[ 2 ].tb_frame

    src_file = os.path.normcase( frame.f_code.co_filename )
    filename = src_file
    rv = None
    while rv is None:
        if not hasattr( frame, "f_code" ):
            break # running out of frames

        filename = os.path.normcase( frame.f_code.co_filename )
        if filename == src_file:
            # keep climbing up the stack until a frame outside of this file
            # is found - this has to be the invoker
            frame = frame.f_back
            continue

        rv = ( frame.f_code.co_filename, frame.f_lineno, 
               frame.f_code.co_name, frame.f_locals )

    if rv is None:
        rv = ( "unknown", "unknown", "unknown", {} )

    return rv

#
def log_with_level( level ):
    return lambda *args, **kwargs: log( *args, level = level, **kwargs )

# monkey patch the basestring to expose the logging methods
dstr = monkeypatch.get_class_dict( basestring )
logmethods = {
    "logdebug": logging.DEBUG,
    "loginfo": logging.INFO,
    "logwarning": logging.WARNING,
    "logwarn": logging.WARNING,
    "logerror": logging.ERROR,
    "logcritical": logging.CRITICAL,
    "logfatal": logging.CRITICAL
}
dstr[ "log" ] = log
for fname, level in logmethods.items():
    dstr[ fname ] = log_with_level( level )