prettylogs
==========

A Python logging utility for easily creating simple, beautiful and minimalistic log lines in your code.

Introduction
------------
Logs are ugly. They add massive amounts of fluff to the code, making it bloated and defocusing, turning your beautiful materpiece into a messy clutter of logic and log lines. In fact, the more complex a system is, the more likely it is to require extensive logging, which - due to the reduced readability - makes the system even more complex. It's a paradoxical kinda thing. Apsect-oriented programming presents its own ultimate solution for it, with the price of some design challenges.

This library doesn't solve this problem. Instead, it attempts to reduce the boilerplate of logging by making it minimalistic and concise.

> Note: `prettylogs` uses the unholy magic of monkey patching the built-in `basestring` type. If you are disgusted by it, now will be a good time to leave.

Content first
-------------
The first key goal of prettylogs is to put the actual content of the log line first. It makes the code read more fluently, and helps explain what the code does. To some extent, it can replace or extend existing comments (similar to how docstrings work):

```python
"This is a short log message".loginfo( logger )

"""
This is a lengthy message
with multiple lines
""".loginfo( logger )
```

This is done by extending Python's built-in `basestring` class (parent class of `str` and `unicode`) with the normal logging shortcuts of the logging module. Alternatively, you can just use `.log( logger, level = 60 )` for more robust control on the log level.

String formatting
-----------------
You can notice that the first argument is always the logger instance to be used. The rest of the arguments are passed as-is to the logger. This maintains the normal behavior of the logging methods for string formatting:

```python
"""
%s stole the %s
""".loginfo( logger, "monster", "cookie jar" )

"""
Give me a big hug, %(you)s
""".loginfo( logger, { "you": "Big Bird" } )
```

Another little trick is that the local scope is also available in string formatting (unless overridden explicitly):

```python
howmany = "SEVEN"
"""
%(howmany)s BANANAS!
""".loginfo( logger )
```

This usually eliminates, or reduces, the redudent variable passing thus allowing the log lines to remain concise and simply describe the state of the current scope with little boilerplate.


