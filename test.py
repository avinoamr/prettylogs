import logging
import prettylogs

logging.basicConfig( level = logging.DEBUG )
logger = logging.getLogger( "prettylogs-test" )
logger = prettylogs.PrettyLogger( logger )


#
def test():

    something = "variables"

    """
    prettylogs is beautiful, eh?
    We can use %(something)s from the local scope, or add
    %(something_else)s.
    """ >> logger.info({ "something_else": "arguments" })

if "__main__" == __name__:
    test()