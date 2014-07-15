"""The *AttributeHelper* class provides tools that enable application configuration
and construction.

*AttributeHelper* provides the functionality as a mix-in class.

.. warning:: There is a reason the methods in the class are double underlined.

  Developers utilizing these methods should have a good understanding of the
  effects that use of these methods. Some of these methods have effects
  across class hierarchies.

AttributeHelper Class Utilization
+++++++++++++++++++++++++

The *AttributeHelper* class is designed to ba a mix-in class for the construction of
applications. It performs this functionality by providing methods that allow
a class hierarchy to drive application initialization.

* :meth:'~cognate.attribute_helper.AttributeHelper.__invoke_method_on_children__

*AttributeHelper* also provides some plain helper methods to ease typical
configuration scenarios.

* :meth:'~cognate.attribute_helper.AttributeHelper.__copy_property_values__
* :meth:'~cognate.attribute_helper.AttributeHelper.__create_property_bag__
* :meth:'!cognate.attribute_helper.AttributeHelper.__set_unassigned_attrs__

Be sure to visit each of the methods for further details on *AttributeHelper*
functionality.
"""


class AttributeHelper(object):
    """This is a min-in helper library class.

    *AttributeHelper* is used by deriving child classes, which inherit the *AttributeHelper*
    functionality. The functionality that crosses class hierarchy will only do
    so along the primary base class chain.

    By way of example, a class declaration to inherit *AttributeHelper* functionality::

      class SomeChild(AttributeHelper): ...

    and *AttributeHelper* will operate over *SomeChild* base class methods and
    attributes, *AttributeHelper* can also be utilized as a multi-inheritance
    declaration::

      class SomeChild(ParentClass, AttributeHelper): ...

    However, *AttributeHelper will only operate on the direct base class chain::

      class Parent(AttributeHelper): ...

      # SomeMixin is unrecognized in primary base class chain:
      class OtherChild(Parent, SomeMixin):


    In the instance above, *AttributeHelper* will only operate over *Parent* and
    *OtherChild*
    when it navigates bases with methods such as :meth:'~cognate.AttributeHelper
    .__invoke_method_on_children__.
    """

    def __invoke_method_on_children__(self, func_name=None, *args, **kwargs):
        """This helper method will walk the primary base class hierarchy to
        invoke a method if it exists for a given base class.

        :param func_name: The name of a function to search for invocation.
        :type func_name: str
        :param args: An argument list to pass to the target function.
        :type args: list
        :param kwargs: A dictionary of name/value pairs to pass to the target
        function as named arguments.
        :type kwargs: dict
        :return: None
        ":except:
          - **ValueError** - Thrown if no function name is provided.

        In an effort to explain, assume that a class hierarchy has been defined
        as the image below:

        .. image:: ../images/invoke_method_on_bases_class_hierarchy.png

        *AttributeHelper.__invoke_method_on_children__* will traverse the class hierarchy
        invoking target method *the_func* on each base class. This is different
        from normal python resolution, which will only inoke the first instance
        of the method defined in the class hierarchy, which would be Child3
        .the_func.

        .. image:: ../images/invoke_method_on_bases.png

        .. note:: Mind the flow of invocation on the class hierarchy.

          Invocation of target *func_name* is from the AttributeHelper class as the
          starting point, and the search continuing out toward the final
          ancestor class.

        ::Example Usage:

        To utilize this method, a function name must be provided.

        .. warning:: Beware mistyped method names.

          If a method name is supplied for a method that does not exist,
          the *__invoke_method_on_children__* will raise no exception.

        >>> foo = AttributeHelper()
        >>> foo.__invoke_method_on_children__()
        Traceback (most recent call last):
        ...
        ValueError: __invoke_method_on_children__:func_name parameter required
        >>> # Now correctly
        >>> foo.__invoke_method_on_children__(func_name='the_func')

        In actual usage, declare a AttributeHelper derived child class with a target
        function. It is possible to have more than one ancestor class with the
        target function defined. The *__invoke_method_on_children__* will
        execute
        the function on each of the child classes.

        >>> class Bar(AttributeHelper):
        ...   def the_func(self, a_key=None):
        ...     print 'a_key:', a_key
        >>> bar = Bar()

        With an instance of a *AttributeHelper* child class, we can invoke the method in
        two ways, as exampled below.

        >>> # Create a keyword argument dictionary or argument list
        >>> kwargs = {'a_key':'a_value'}
        >>> bar.__invoke_method_on_children__(func_name='the_func', **kwargs)
        a_key: a_value
        >>> # Simply pass the argument keyword and value
        >>> bar.__invoke_method_on_children__(
        ...     func_name='the_func', a_key='value')
        a_key: value
        """
        if func_name is None:
            raise ValueError(
                '__invoke_method_on_children__:func_name parameter required')

        class_stack = []
        base = self.__class__  # The root class in the hierarchy.
        while base is not None and base is not object:
            class_stack.append(base)
            base = base.__base__  # iterate to the next base class

        while len(class_stack) is not 0:
            base = class_stack.pop()
            if func_name in base.__dict__:  # check the func exist on class
                # instance
                func = getattr(base, func_name)
                func(self, *args,
                     **kwargs)  # This is the function getting invoked


def copy_property_values(source, target, property_names):
    """This method copies the property values in a given list from a given
    source object to a target source object.

    :title:copy_property_values Method

    :param src: The source object that is to be inspected for property
    values.
    :type src: Object that supports hasattr() method.
    :param target: The target object that will be modified with values found
    in src.
    :type target: Object that supports setattr() method.
    :param property_names: List of property names whose values are to be
    copied from source to object.
    :type property_names: List or set of string property names.

    The *copy_property_values* method will only copy the values from src
    when a property name is found in the src. In cases where a property
    value
    is not found in the src object, then no change to the target object is
    made.

    :Example Usage:

    >>> src = create_property_bag()
    >>> src.property1 = 1
    >>> src.property2 = 2
    >>> src.property3 = 3
    >>> target = create_property_bag()
    >>> property_list = ['property1', 'property2', 'exist_not_property']
    >>> copy_property_values(src, target, property_list)
    >>> assert hasattr(target, 'property1')
    >>> assert hasattr(target, 'property2')
    >>> assert not hasattr(target, 'property3')
    >>> assert not hasattr(target, 'exist_not_property')
    """
    if source is None:
        raise ValueError('"source" must be provided.')
    if target is None:
        raise ValueError('"target" must be provided.')
    if property_names is None:
        raise ValueError('"property_list" must be provided.')
    if not hasattr(property_names, '__iter__'):
        raise ValueError(
            '"property_names" must be a sequence type, such as list or set.')

    for property_name in property_names:
        if hasattr(source, property_name):
            setattr(target, property_name, getattr(source, property_name))


def create_property_bag():
    """This method will create a property bag that can be used to assign
    attributes.

    :return: An empty obect that supports assigning properties.

    It is not valid to create a python instance of *object* for use as a
    property bag. The underlying reason is that there is no __dict__
    property
    assigned to an instance of object - hence the inability for an object to
    hold an attribute assignment.

    :Example Usage:

    >>> property_bag = create_property_bag()
    >>> assert property_bag
    >>> property_bag.some_attr = 5
    >>> assert property_bag.some_attr == 5
    """

    return type('__property_bag', (object,), dict())


def set_attrs_from__dict(src_dict=None, target=None):
    """

    >>> src_dict = {'prop1': 'val1', 'prop2': 2}
    >>> target = create_property_bag()
    >>> assert not hasattr(target, 'prop1')
    >>> assert not hasattr(target, 'prop2')
    >>> set_attrs_from__dict(src_dict, target)
    >>> assert target.prop1 == 'val1'
    >>> assert target.prop2 == 2

    :param src_dict:
    :type src_dict: dict
    :param target:
    :type target: object
    """
    if src_dict is None:
        raise ValueError('"src_dict" must be provided.')
    if not isinstance(src_dict, dict):
        raise ValueError('"src_dict" must be of type dict.')
    if target is None:
        raise ValueError('"target" must be provided.')

    for name, value in src_dict.items():
        setattr(target, name, value)


def set_unassigned_attrs(target, attr_list):
    """This method takes a list of name/value tuple and assigns the property
    value to the given target, if the property does NOT exist.

    :param target: The target object that is to have name values applied.
    :type target: object, must support ``hasattr`` and ``setattr`` methods.
    :param attr_list: A list of name-value tuple.
    :type attr_list: [('name', some_value), ...]
    :return: None

    It should be kept in mind that if the target already has the named
    attribute assigned, the value supplied in the list is ignored.

    :Example Usage:

    >>> foo = AttributeHelper()
    >>> foo.ignore_attr = True
    >>> attr_list = [('some_attr', 'some_value'),('int_attr', 1),
    ...   ('ignore_attr', False)]
    >>> set_unassigned_attrs(foo, attr_list)
    >>> assert foo.some_attr == 'some_value'
    >>> assert foo.int_attr == 1
    >>> assert foo.ignore_attr == True # ignored value from attr_list
    """
    if target is None:
        raise ValueError('"target" must be provided.')
    if attr_list is None:
        raise ValueError('"attr_list" must be provided.')
    if not hasattr(attr_list, '__iter__'):
        raise ValueError(
            '"attr_list" must be a sequence type, such as list or set.')

    for (name, value) in attr_list:
        if not hasattr(target, name):
            setattr(target, name, value)
