prettylogs
==========

A Python logging utility for easily creating simple, beautiful and minimalistic log lines in your code.

Introduction
------------
Logs are ugly. They add massive amounts of fluff to the code, making it bloated and defocusing, turning your beautiful materpiece into a messy clutter of logic and log lines. In fact, the more complex a system is, the more likely it is to require extensive logging, which - due to the reduced readability - makes the system even more complex. It's a paradoxical kinda thing. Apsect-oriented programming presents its own ultimate solution for it, with the price of some design challenges.

This library doesn't solve this problem. Instead, it attempts to reduce the boilerplate of logging by making it minimalistic and concise.

> Note: `prettylogs` uses the unholy magic of monkey patching the built-in `basestring` type. If you are disgusted by it, now will be a good time to leave.
