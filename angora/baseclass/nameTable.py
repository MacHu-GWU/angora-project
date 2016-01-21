#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**中文文档**

nameTable 是一种数据容器类。 以名字为namespace来访问对应的object, 同时提供了以object的属性的方式
来访问对应的object的简洁方法。

例如你有一个 ``花名册``, 里面记录了许多 ``人``, 每个 ``人`` 有id, name等属性。
你可以以 ``花名册.人名`` 的形式来访问人的对象, 也可以通过 ``花名词.id__人的id`` 或 
``花名册.name__人名`` 的形式来达到同样的目的。
"""

import inspect

class Base(object):
    """nameTable base class.

    restriction:

    - class attributes's namespace cannot start with "__" and end with "__"
    - class attributes's value has to be an object

    Example::

        >>> class Person(namespace.Base):
        ...     def __init__(self, id, name):
        ...         self.id = id
        ...         self.name = name
        ...
        ...     def __repr__():
        ...         return "Person(id=%r, name=%r)" % (self.id, self.name)

        >>> class PersonNamespace_(Base):
        ...     Jack = Person(id=1, name="Jack")
        ...     Tom = Person(id=2, name="Tom")

        >>> PersonNamespace = PersonNamespace_()
        >>> PersonNamespace.Jack
        Person(id=1, name='Jack')

        >>> PersonNamespace.id_1
        Person(id=1, name='Jack')

        >>> PersonNamespace.name_Jack
        Person(id=1, name='Jack')
    """
    def __init__(self, **kwargs):
        for attr, value in kwargs.items():
            object.__setattr__(self, attr, value)

        class_attributes = self.__class_attributes__()

        for class_attr in class_attributes:
            instance = object.__getattribute__(self, class_attr)
            for attr in instance.__dict__:
                object.__setattr__(self, "__%s_instance__" % attr, dict())
            break

        for class_attr in class_attributes:
            instance = object.__getattribute__(self, class_attr)
            for attr, value in instance.__dict__.items():
                object.__getattribute__(self, "__%s_instance__" % attr)[str(value)] = class_attr

    def __class_attributes__(self):
        """Return all class attributes.
        """
        class_attributes = list()
        for key, value in inspect.getmembers(self):
            if not (key.startswith("__") or key.endswith("__")):
                if not inspect.ismethod(value):
                    class_attributes.append(key)
        return class_attributes

    def keys(self):
        """Return all class attributes.
        """
        return self.__class_attributes__()

    def values(self):
        """Return all value of class attributes.
        """
        return [object.__getattribute__(self, class_attribute)
                for class_attribute in self.__class_attributes__()]

    def items(self):
        """Return all class attributes and value pairs.
        """
        items = list()
        for class_attribute in self.__class_attributes__():
            items.append(
                (class_attribute, object.__getattribute__(self, class_attribute)))
        return items

    def __getattr__(self, attr):
        """Smart get attribute method.

        - self.attr: return class attribute's value
        - self.attr__value: return the instance that its attr's value is #value
        """
        chunks = attr.split("__")
        l = len(chunks)

        if l == 2:
            return object.__getattribute__(
                self,
                object.__getattribute__(
                    self,
                    "__%s_instance__" % chunks[0],
                )[chunks[1]]
            )
        else:
            return object.__getattribute__(self, attr)

    def __repr__(self):
        kwargs = list()
        for attr, value in self.items():
            kwargs.append("%s=%r" % (attr, value))
        return "%s(%s)" % (self.__class__.__name__, ", ".join(kwargs))

    def to_dict(self):
        """return data in dict view.
        """
        d = dict()
        for class_attribute in self.__class_attributes__():
            d[class_attribute] = dict()
            for attr, value in self.__getattr__(class_attribute).__dict__.items():
                d[class_attribute][attr] = value
        return d

if __name__ == "__main__":
    import unittest

    from angora.baseclass import namespace

    class Person(namespace.Base):
        def __init__(self, id, name):
            self.id = id
            self.name = name

        def __eq__(self, other):
            return self.__dict__ == other.__dict__

    class PersonNamespace_(Base):
        Jack = Person(id=1, name="Jack")
        Tom = Person(id=2, name="Tom")

    class Unittest(unittest.TestCase):
        def test_all(self):
            for person_namespace in [
                        PersonNamespace_(),
                        PersonNamespace_(
                            Jack=Person(id=1, name="Jack"),
                            Tom=Person(id=2, name="Tom")
                        ),
                    ]:
                self.assertListEqual(person_namespace.__class_attributes__(),
                                     ["Jack", "Tom"])
                self.assertEqual(person_namespace.Jack, Person(id=1, name="Jack"))
                self.assertEqual(person_namespace.id__1, Person(id=1, name="Jack"))
                self.assertEqual(person_namespace.name__Jack, Person(id=1, name="Jack"))

                self.assertListEqual(
                    person_namespace.keys(),
                    ["Jack", "Tom"],
                )
                self.assertListEqual(
                    person_namespace.values(),
                    [Person(id=1, name="Jack"), Person(id=2, name="Tom")],
                )
                self.assertListEqual(
                    person_namespace.items(),
                    [("Jack", Person(id=1, name="Jack")), ("Tom", Person(id=2, name="Tom"))],
                )

                self.assertDictEqual(
                    person_namespace.to_dict(),
                    {"Jack": {"id": 1, "name": "Jack"}, "Tom": {"id": 2, "name": "Tom"}},
                )

        def test_str(self):
            print(PersonNamespace_())

    unittest.main()