from unittest import TestCase

from cognate import attribute_helper


class AttributeHelperTestCase(TestCase):
    def test_copy_attribute_values(self):
        """Ensure copy_attribute_value functionality and error handling."""
        src_property_bag = attribute_helper.create_attr_bag()
        src_property_bag.prop1 = 'value 1'
        src_property_bag.prop2 = 'value 2'
        src_property_bag.prop3 = 'value 3'
        src_property_bag.prop4 = 'value 4'
        trgt_property_bag = attribute_helper.create_attr_bag()
        trgt_property_bag.prop2 = 'another 2'
        trgt_property_bag.prop3 = 'another 3'
        property_names = {'prop1', 'prop3'}

        self.assertRaisesRegexp(
            ValueError,
            '"source" must be provided.',
            attribute_helper.copy_attribute_values,
            None, trgt_property_bag, property_names)

        self.assertRaisesRegexp(
            ValueError,
            '"target" must be provided.',
            attribute_helper.copy_attribute_values,
            src_property_bag, None, property_names)

        self.assertRaisesRegexp(
            ValueError,
            '"property_list" must be provided.',
            attribute_helper.copy_attribute_values,
            src_property_bag, trgt_property_bag, None)

        self.assertRaisesRegexp(
            ValueError,
            '"property_names" must be a sequence type, such as list or set.',
            attribute_helper.copy_attribute_values,
            src_property_bag, trgt_property_bag, 'Not a sequence')

        self.assertFalse(hasattr(trgt_property_bag, 'prop1'))
        self.assertEqual(trgt_property_bag.prop2, 'another 2')
        self.assertEqual(trgt_property_bag.prop3, 'another 3')
        self.assertFalse(hasattr(trgt_property_bag, 'prop4'))
        attribute_helper.copy_attribute_values(
            src_property_bag, trgt_property_bag, property_names)
        self.assertEqual(trgt_property_bag.prop1, 'value 1')
        self.assertEqual(trgt_property_bag.prop2, 'another 2')
        self.assertEqual(trgt_property_bag.prop3, 'value 3')
        self.assertFalse(hasattr(trgt_property_bag, 'prop4'))

    def test_set_attrs_from_dict(self):
        """Ensure set_attrs_from_dict features and error handling."""
        a_property_bag = attribute_helper.create_attr_bag()

        self.assertRaisesRegexp(
            ValueError,
            '"src_dict" must be provided.',
            attribute_helper.set_attrs_from__dict, None, a_property_bag)

        self.assertRaisesRegexp(
            ValueError,
            '"src_dict" must be of type dict.',
            attribute_helper.set_attrs_from__dict, 'not dict', a_property_bag)

        self.assertRaisesRegexp(
            ValueError,
            '"target" must be provided.',
            attribute_helper.set_attrs_from__dict, {'prop': 'val'}, None)

        self.assertFalse(hasattr(a_property_bag, 'prop'))
        attribute_helper.set_attrs_from__dict({'prop': 'val'}, a_property_bag)
        self.assertEqual(a_property_bag.prop, 'val')

    def test_set_unassigned_attrs(self):
        """Ensure set_unassigned features and error handling."""
        self.assertRaisesRegexp(
            ValueError,
            '"target" must be provided.',
            attribute_helper.set_unassigned_attrs, None, ['prop', 'value'])

        a_property_bag = attribute_helper.create_attr_bag()

        self.assertRaisesRegexp(
            ValueError,
            '"attr_list" must be provided.',
            attribute_helper.set_unassigned_attrs, a_property_bag, None)

        self.assertRaisesRegexp(
            ValueError,
            '"attr_list" must be a sequence type, such as list or set.',
            attribute_helper.set_unassigned_attrs, a_property_bag, 'not list')

        self.assertFalse(hasattr(a_property_bag, 'prop'))
        attribute_helper.set_unassigned_attrs(a_property_bag, [('prop', 'val')])
        self.assertEqual(a_property_bag.prop, 'val')
