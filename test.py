import logging
import prettylogs

logging.basicConfig( level = logging.DEBUG )
logger = logging.getLogger( "prettylogs-test" )

#
def test():

    something = "variables"

    """
    prettylogs is beautiful, eh?
    We can use %(something)s from the local scope, or add
    %(something_else)s.
    """.loginfo( logger, { "something_else": "a dictionary" })

if "__main__" == __name__:
    test()