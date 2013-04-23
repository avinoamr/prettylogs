import logging
import prettylogs

logging.basicConfig( level = logging.DEBUG )
logger = logging.getLogger( "prettylogs-test" )
logger = logger.pretty()


#
def test():

    something = "variables"

    """
    prettylogs is beautiful, eh? 
    We can use %(something)s from the local scope, or add 
    %(something_else)s.
    """ >> logger.info({ "something_else": "arguments" })

    logger.info( "Hello World" )

if "__main__" == __name__:
    test()