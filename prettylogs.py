import sys
import os
import logging

import monkeypatch

##
def log( msg, logger, *args, **kwargs ):
    level = kwargs.get( "level", None )
    if not logger.isEnabledFor( level ):
        return None 

    msg = msg.strip()
    extra = kwargs.get( "extra", None )
    exc_info = kwargs.get( "exc_info", None )
    fn, lno, func = find_caller()
    record = logger.makeRecord( logger.name, level, fn, lno, msg, args, exc_info, 
        func, extra )
    logger.handle( record )
    return record.getMessage()


# burrowed from python's logging module
# unfortunately, python's logging module isn't robust or modular enough to 
# be easily extended in a prettier way.
def find_caller():
    """ Find the invoking code location of the log method, by looking up the 
    stack until there's a location outside of the prettylogs package """

    frame = sys._getframe() if hasattr( sys, "_getframe" ) else None
    if frame is None:
        try:
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
            frame = frame.f_back
            continue

        rv = ( frame.f_code.co_filename, frame.f_lineno, 
               frame.f_code.co_name )

    if rv is None:
        rv = ( None, None, None )

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

#
def test():
    logging.basicConfig( level = logging.DEBUG )
    logger = logging.getLogger( "prettylogs-test" )

    """
    prettylogs is beautiful, eh?
    """.loginfo( logger )

#
if "__main__" == __name__:
    test()