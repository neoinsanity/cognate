"""The *AttributeHelper* class provides tools that enable application configuration
and construction.

*AttributeHelper* provides the functionality as a mix-in class.

.. warning:: There is a reason the methods in the class are double underlined.

  Developers utilizing these methods should have a good understanding of the
  effects that use of these methods. Some of these methods have effects
  across class hierarchies.

AttributeHelper Utilization
============================

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


def copy_attribute_values(source, target, property_names):
    """This method copies the property values in a given list from a given
    source object to a target source object.

    :title:copy_attribute_values Method

    :param src: The source object that is to be inspected for property
    values.
    :type src: Object that supports hasattr() method.
    :param target: The target object that will be modified with values found
    in src.
    :type target: Object that supports setattr() method.
    :param property_names: List of property names whose values are to be
    copied from source to object.
    :type property_names: List or set of string property names.

    The *copy_attribute_values* method will only copy the values from src
    when a property name is found in the src. In cases where a property
    value
    is not found in the src object, then no change to the target object is
    made.

    :Example Usage:

    >>> src = create_attr_bag()
    >>> src.property1 = 1
    >>> src.property2 = 2
    >>> src.property3 = 3
    >>> target = create_attr_bag()
    >>> property_list = ['property1', 'property2', 'exist_not_property']
    >>> copy_attribute_values(src, target, property_list)
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


def create_attr_bag():
    """This method will create a property bag that can be used to assign
    attributes.

    :return: An empty obect that supports assigning properties.
    :rtype: type

    It is not valid to create a python instance of *object* for use as a
    property bag. The underlying reason is that there is no __dict__
    property
    assigned to an instance of object - hence the inability for an object to
    hold an attribute assignment.

    :Example Usage:

    >>> attr_bag = create_attr_bag()
    >>> assert attr_bag
    >>> attr_bag.some_attr = 5
    >>> assert attr_bag.some_attr == 5
    """

    return type('__property_bag', (object,), dict())


def set_attrs_from__dict(src_dict=None, target=None):
    """

    >>> src_dict = {'prop1': 'val1', 'prop2': 2}
    >>> target = create_attr_bag()
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
    """Method takes a list of name/value tuple and assigns the property
    value to the given target, if the property does NOT exist.

    :param target: The target object that is to have name values applied.
    :type target: object, must support ``hasattr`` and ``setattr`` methods.
    :param attr_list: A list of name-value tuple.
    :type attr_list: [('name', some_value), ...]
    :return: None

    It should be kept in mind that if the target already has the named
    attribute assigned, the value supplied in the list is ignored.

    :Example Usage:

    >>> foo = create_attr_bag()
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
