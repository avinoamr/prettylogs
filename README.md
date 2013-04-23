prettylogs
==========
A Python logging utility for easily creating simple, beautiful and minimalistic 
log lines in your code.

Introduction
------------
Logs are ugly. They add massive amounts of fluff to the code, making it bloated 
and defocusing, turning your beautiful materpiece into a messy clutter of logic 
and log lines. In fact, the more complex a system is, the more likely it is to 
require extensive logging, which - due to the reduced readability - makes the 
system even more complex. It's a paradoxical kinda thing. Apsect-oriented 
programming presents its own ultimate solution for it, with the price of some 
design challenges.

This library doesn't solve the problem. Instead, it attempts to reduce the 
boilerplate of logging by making it minimalistic and concise.

> Note: `prettylogs` uses the unholy magic of monkey patching the 
`logging.Logger` class. If you're disgusted by it, now will be a good time to
leave.

Getting Started
---------------
After downloading and installing the library, you'll need to wrap your Logger 
instance with the `prettylogs.PrettyLogger` class:
```python
import logging
import prettylogs
logger = logging.getLogger( "sesame" )
logger = prettylogs.PrettyLogger( logger )
```

Alternatively, you can just configure the logging facility to use this class as 
its default Logger class:
```python
logging.setLoggerClass( prettylogs.PrettyLogger )
logger = logging.getLogger( "sesame" )
```

Content first
-------------
The first key goal of prettylogs is to put the actual content of the log line 
first. It makes the code read more fluently, and helps explain what the code 
does. To some extent, it can replace or extend existing comments (similar to how
docstrings work):

```python
"""
This is a lengthy message
with multiple lines that
describes the state and 
logic of the code
""" >> logger.info()
```

String formatting
-----------------
The right-shift notation uses the same API as Python's `Logger` class, except 
that the message argument isn't passed directly. The rest of the arguments are 
passed to the logging module for the default string formatting behavior:

```python
"""
%s stole the %s
""" >> logger.info( "monster", "cookie jar" )

"""
Give me a big hug, %(you)s
""" >> logger.info({ "you": "Big Bird" })
```

Another little trick is that the local scope is also available in string 
formatting (unless overridden):

```python
howmany = "SEVEN"
"""
%(howmany)s BANANAS!
""" >> logger.info()
```

This usually eliminates, or reduces, the redudent variable passing thus allowing
the log lines to remain concise and simply describe the state of the current 
scope with little boilerplate.
