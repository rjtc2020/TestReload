# coding:utf-8

import unittest

def update_func(old_func,new_func):
    old_func.__doc__=new_func.__doc__
    old_func.__dict__=new_func.__dict__
    old_func.__defaults__=new_func.__defaults__
    old_func.__code__=new_func.__code__

    # print "查看函数"
    # print old_func.__doc__
    # print old_func.__dict__
    # print old_func.__defaults__
    # print old_func.__code__

def old_foo():
    return "old_foo"

def new_foo():
    return "new_foo"

class ReloadTest(unittest.TestCase):

    def test_update_func(self):
        self.assertEqual('old_foo',old_foo())
        update_func(old_foo,new_foo)
        self.assertEqual('new_foo',old_foo())