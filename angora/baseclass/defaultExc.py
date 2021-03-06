#!/usr/bin/env python
# -*- coding: utf-8 -*-

def declare_base(erroName=True):
    """Create a Exception with default message.
    
    :param errorName: boolean, True if you want the Exception name in the 
      error message body.
    """
    if erroName:
        class Base(Exception):
            def __str__(self):
                if len(self.args):
                    return "%s: %s" % (self.__class__.__name__, self.args[0])
                else:
                    return "%s: %s" % (self.__class__.__name__, self.default)
    else:
        class Base(Exception):
            def __str__(self):
                if len(self.args):
                    return "%s" % self.args[0]
                else:
                    return "%s" % self.default
    return Base

if __name__ == "__main__":
    class DataError(declare_base(erroName=False)):
        default = "This is DEFAULT message"
        
    try:
        raise DataError
    except Exception as e:
        print(e)
        
    try:
        raise DataError("This is CUSTOMIZE message")
    except Exception as e:
        print(e)