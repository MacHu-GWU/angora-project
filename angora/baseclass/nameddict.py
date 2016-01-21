#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**中文文档**

和 ``collections.namedtuple`` 类似, ``nameddict`` 是一种数据容器类。提供了方便的方法
对属性, 值的遍历, 以及与dict之间的交互。
"""

class Base(object):
    """nameddict base class.
    
    if you really care about performance, use collections.namedtuple.
    """
    def __init__(self, **kwargs):
        for attr, value in kwargs.items():
            object.__setattr__(self, attr, value)
     
    def __repr__(self):
        kwargs = list()
        for attr, value in self.__dict__.items():
            kwargs.append("%s=%r" % (attr, value))
        return "%s(%s)" % (self.__class__.__name__, ", ".join(kwargs))
    
    @classmethod
    def _make(cls, d):
        return cls(**d)
    
    def keys(self):
        return self.__dict__.keys()
    
    def values(self):
        return self.__dict__.values()
    
    def items(self):
        return self.__dict__.items()
    
    def to_dict(self):
        return self.__dict__
     
if __name__ == "__main__":
    import unittest
    
    class Person(Base):
        def __init__(self, name):
            self.name = name
    
    class Unittest(unittest.TestCase):
        def test_all(self):
            person = Person(name="Jack")
            self.assertEqual(str(person), "Person(name='Jack')")
            self.assertDictEqual(person.to_dict(), {"name": "Jack"})

            person = Person._make({"name": "Jack"})
            self.assertEqual(str(person), "Person(name='Jack')")
            self.assertDictEqual(person.to_dict(), {"name": "Jack"})
            
    unittest.main()