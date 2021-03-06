# -*- coding: utf-8 -*-
import scipy as s
import unittest.main
import sys
from unittest import TestCase
import imp
tdm = imp.load_source('tdm_loader', 'C:\Users\Florian\PyCharmProjects\\tdm_loader\\tdm_loader\\tdm_loader.py')


class TestTDMLoader(TestCase):

    def __init__(self, *params):
        super(TestTDMLoader, self).__init__(*params)
        self.data = tdm.OpenFile("""../tdm_loader_test/test_files/test_sample0001.tdm""")

    def test_channel_accessibility(self):
        arg_arr = [(0, 0), (0, 1), (0, 2),
                   (1, 0), (1, 1)]
        try:
            for ch in arg_arr:
                self.data.channel(*ch)
            self.data.channel(0, 0, 0)
        except IndexError:
            self.fail("Not all channels are accessible.")

    def test_invalid_channel_raises_error(self):
        arg_arr = [(-1, -1), (-1, 0), (0, -1),
                   (3, 0), (0, 3), (1, 2),
                   (2, 1), (1, 2), (2, 0)]

        for ch in arg_arr:
            self.assertRaises(IndexError, self.data.channel, *ch)

    def test_get_channel_by_index(self):
        self.assertTrue((self.data.channel(0, 0) == s.array([1, 2, 3, 4])).all())
        self.assertTrue((self.data.channel(0, 1) == s.array([.1, .2, .3, .4, .5, .6])).all())
        self.assertTrue((self.data.channel(0, 2) == s.array([9, 10, 11, -50, sys.maxint, -sys.maxint-1])).all())
        self.assertTrue((self.data.channel(1, 0) == s.array([1.7976931348623157e+308, sys.maxint])).all())
        self.assertTrue((self.data.channel(1, 1) == s.array([0])).all())

    def test_get_channel_group_by_str(self):
        self.assertTrue((self.data.channel("channel2_test123$$?", 0) == s.array([1, 2, 3, 4])).all())
        self.assertTrue((self.data.channel("channel2_test123$$?", 2) == s.array([9, 10, 11, -50, sys.maxint, -sys.maxint-1])).all())
        self.assertTrue((self.data.channel("channel2", 1) == s.array([0])).all())

    def test_channel_invalid_type(self):
        self.assertRaises(TypeError, self.data.channel, (0.0, 1.0))
        self.assertRaises(TypeError, self.data.channel, (-1, 0))
        self.assertRaises(TypeError, self.data.channel, (0, -1))
        self.assertRaises(TypeError, self.data.channel, (-1, -1))
        self.assertRaises(TypeError, self.data.channel, (0, "lala"))
        self.assertRaises(TypeError, self.data.channel, (0, 0, 1))
        self.assertRaises(TypeError, self.data.channel, (0.0, 1, "lala"))
        self.assertRaises(TypeError, self.data.channel, (0.0, 1, 1.0))

    def test_channel_group_index(self):
        self.assertEqual(self.data.channel_group_index("channel2_test123$$?"), 0)
        self.assertEqual(self.data.channel_group_index("channel2", 0), 1)
        self.assertRaises(IndexError, self.data.channel_group_index, *("channel2", 1))
        self.assertRaises(TypeError, self.data.channel_group_index, 0)
        self.assertRaises(TypeError, self.data.channel_group_index, 0.)
        self.assertRaises(TypeError, self.data.channel_group_index, *("channel2", "lala"))
        self.assertRaises(ValueError, self.data.channel_group_index, "test")

    def test_channel_group_name(self):
        self.assertEqual(self.data.channel_group_name(0), "channel2_test123$$?")
        self.assertEqual(self.data.channel_group_name(1), "channel2")
        self.assertRaises(TypeError, self.data.channel_group_name, "lala")
        self.assertRaises(TypeError, self.data.channel_group_name, 0.0)

    def test_channel_group_search(self):
        self.assertTrue(
            self.data.channel_group_search("channel")
            == [("channel2_test123$$?", 0), ("channel2", 1), ("channel3", 2)], True)

        self.assertTrue(self.data.channel_group_search("test") == [("channel2_test123$$?", 0)])
        self.assertTrue(self.data.channel_group_search("helloworld") == [])
        self.assertTrue(self.data.channel_group_search("") == [('channel2_test123$$?', 0),
                                                               ('channel2', 1),
                                                               ('channel3', 2)])
        self.assertRaises(TypeError, self.data.channel_group_search, 0)
        self.assertRaises(TypeError, self.data.channel_group_search, -1)

    def test_channel_name(self):
        self.assertTrue(self.data.channel_name(0, 0) == "Float_4_Integers")
        self.assertTrue(self.data.channel_name(0, 1) == "Float as Float")
        self.assertTrue(self.data.channel_name(0, 2) == "Integer32_with_max_min")
        self.assertTrue(self.data.channel_name(1, 0) == "")
        self.assertTrue(self.data.channel_name(1, 1) == "")
        self.assertRaises(IndexError, self.data.channel_name, *(2, 0))
        self.assertRaises(IndexError, self.data.channel_name, *(0, 3))
        self.assertRaises(TypeError, self.data.channel_name, ("lala", 0))
        self.assertRaises(TypeError, self.data.channel_name, (0, "lala"))
        self.assertRaises(TypeError, self.data.channel_name, (0, 0.))
        self.assertRaises(TypeError, self.data.channel_name, (0., 0))

    def test_channel_search(self):
        self.assertEqual(self.data.channel_search("Integers"), [("Float_4_Integers", 0, 0)])
        self.assertEqual(self.data.channel_search("Float"), [("Float_4_Integers", 0, 0),
                                                             ("Float as Float", 0, 1)])
        print self.data.channel_search("")
        self.assertEqual(self.data.channel_search(""), [])

    def test_channel_unit(self):
        self.assertEqual(self.data.channel_unit(0, 0), "arb. units")
        self.assertEqual(self.data.channel_unit(0, 1), "eV")
        self.assertEqual(self.data.channel_unit(1, 0), "")

        self.assertRaises(TypeError, self.data.channel_unit, *(0.0, 0))
        self.assertRaises(TypeError, self.data.channel_unit, *("hello", 0))
        self.assertRaises(TypeError, self.data.channel_unit, *(0, 0.0))

    def test_no_of_channel_groups(self):
        self.assertEqual(self.data.no_channel_groups(), 2)

    def test_len(self):
        self.assertEqual(len(self.data), 5)

    def test_get_item(self):
        self.assertTrue((self.data[0] == s.array([1, 2, 3, 4])).all())
        self.assertTrue((self.data[-5] == s.array([1, 2, 3, 4])).all())
        self.assertTrue((self.data[1] == s.array([.1, .2, .3, .4, .5, .6])).all())
        self.assertTrue((self.data[2] == s.array([9, 10, 11, -50, sys.maxint, -sys.maxint - 1])).all())
        self.assertTrue((self.data[3] == s.array([1.7976931348623157e+308, sys.maxint])).all())
        self.assertTrue((self.data[4] == s.array([0])).all())
        self.assertTrue((self.data[-1] == s.array([0])).all())
        self.assertRaises(IndexError, lambda x: self.data[x], 5)
        self.assertRaises(IndexError, lambda x: self.data[x], -6)

    def test_col(self):
        self.assertTrue((self.data.col(0) == s.array([1, 2, 3, 4])).all())
        self.assertTrue((self.data.col(-5) == s.array([1, 2, 3, 4])).all())
        self.assertTrue((self.data.col(1) == s.array([.1, .2, .3, .4, .5, .6])).all())
        self.assertTrue((self.data.col(2) == s.array([9, 10, 11, -50, sys.maxint, -sys.maxint - 1])).all())
        self.assertTrue((self.data.col(3) == s.array([1.7976931348623157e+308, sys.maxint])).all())
        self.assertTrue((self.data.col(4) == s.array([0])).all())
        self.assertTrue((self.data.col(-1) == s.array([0])).all())
        self.assertRaises(IndexError, self.data.col, 5)
        self.assertRaises(IndexError, self.data.col, -6)

    def test_no_of_channels(self):
        self.assertEqual(self.data.no_channels(0), 3)
        self.assertEqual(self.data.no_channels(1), 2)
        self.assertEqual(self.data.no_channels(-1), 2)
        self.assertEqual(self.data.no_channels(-2), 3)
        self.assertRaises(IndexError, self.data.no_channels, -3)
        self.assertRaises(TypeError, self.data.no_channels, 1.0)
        self.assertRaises(IndexError, self.data.no_channels, 5)

if __name__ == "__main__":
    unittest.main()
