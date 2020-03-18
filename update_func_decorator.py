# coding:utf-8

import unittest
import types

def both_instance_of_type(item1,item2,type):
    return isinstance(item1,type) and isinstance(item2,type)

def update_func(old_func,new_func):
    if not both_instance_of_type(old_func,new_func,types.FunctionType):
        return
    if len(old_func.__code__.co_freevars)!=len(new_func.__code__.co_freevars):#参数数量不同返回
        return
    old_func.__doc__=new_func.__doc__
    old_func.__dict__=new_func.__dict__
    old_func.__defaults__=new_func.__defaults__
    old_func.__code__=new_func.__code__
    if not old_func.__closure__ or not new_func.__closure__:#closure属性为空的时候，说明没形成闭包
        return
    for old_cell,new_cell in zip(old_func.__closure__,new_func.__closure__):#将运行环境中的func进行替换
        if not both_instance_of_type(old_cell.cell_contents,new_cell.cell_contents,types.FunctionType):
            continue
        update_func(old_cell.cell_contents,new_cell.cell_contents)

def decorator(func):
    def wrapper(*args,**kwargs):
        return func(*args,**kwargs)
    return wrapper


def old_foo():
    return "old_foo"

def new_foo():
    return "new_foo"

@decorator
def old_foo_withdec():
    return "old_foo"

@decorator
def new_foo_withdec():
    return "new_foo"

class ReloadTest(unittest.TestCase):

    def test_update_func_withdec1(self):
        self.assertEqual("old_foo",old_foo_withdec())
        update_func(old_foo_withdec,new_foo_withdec)
        self.assertEqual("new_foo",old_foo_withdec())

    def test_update_func_withdec2(self):
        self.assertEqual("old_foo",old_foo())
        update_func(old_foo,new_foo_withdec)
        self.assertEqual("new_foo",old_foo())

