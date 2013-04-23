import sys
import os
import logging
import textwrap

#
class _LazyLogMethod( object ):
    """ LazyLogger is a lazy-wrapper of the Logger log methods """

    #
    def __init__( self, logger, level, args, kwargs ):
        self.logger = logger
        self.level = level
        self.args = args
        self.kwargs = kwargs

    #
    def log( self, msg ):
        if not self.logger.isEnabledFor( self.level ):
            return None

        # 
        msg = textwrap.dedent( msg ).strip().replace( "\n", " " )
        level = self.level
        args = self.args
        kwargs = self.kwargs
        extra = self.kwargs.get( "extra", None )
        exc_info = self.kwargs.get( "exc_info", None )

        # 
        fn, lno, func, f_locals = find_caller()

        if args and len( args ) == 1 and isinstance( args[ 0 ], dict ):
            # sole argument is a dictionary, add the locals to the dictionary
            f_locals.update( args[ 0 ] )
            args = [ f_locals ]
        elif not args:
            # no arguments delivered, default to the locals dictionary
            args = [ f_locals ]

        record = self.logger.makeRecord( self.logger.name, level, fn, lno, msg, 
            args, exc_info, func, extra )
        self.logger.handle( record )
        return record.getMessage()

    #
    def __rrshift__( self, other ):
        if isinstance( other, basestring ):
            self.log( other )
        else:
            super( LazyLogger, self ).__rrshift__( other )


##
class PrettyLogger( logging.Logger ):
    """ PrettyLogger is a dump Logger decorator that's used to invoke
    the logging methods lazily """

    def __init__( self, *args, **kwargs ):
        if args and 1 == len( args ) and isinstance( args[ 0 ], logging.Logger ):
            self._logger = args[ 0 ]
        else:
            super( PrettyLogger, self ).__init( self, *args, **kwargs )

    def log( self, level, *args, **kwargs ):
        return _LazyLogMethod( self._logger, level, args, kwargs )

    def debug( self, *args, **kwargs ):
        return self.log( logging.DEBUG, *args, **kwargs )
    
    def info( self, *args, **kwargs ):
        return self.log( logging.INFO, *args, **kwargs )

    def warning( self, *args, **kwargs ):
        return self.log( logging.WARNING, *args, **kwargs )

    warn = warning

    def error( self, *args, **kwargs ):
        return self.log( logging.ERROR, *args, **kwargs )

    def critical( self, *args, **kwargs ):
        return self.log( logging.CRITICAL, *args, **kwargs )

    fatal = critical


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