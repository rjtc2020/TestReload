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

def update_class(old_class, new_class):
    for name, new_attr in new_class.__dict__.items():
        if name not in old_class.__dict__:
            setattr(old_class, name, new_attr)
        else:
            old_attr = old_class.__dict__[name]
            if both_instance_of_type(old_attr, new_attr, types.FunctionType):
                update_func(old_attr, new_attr)
            elif both_instance_of_type(old_attr, new_attr, staticmethod):
                update_func(old_attr.__func__, new_attr.__func__)
            elif both_instance_of_type(old_attr, new_attr, classmethod):
                update_func(old_attr.__func__, new_attr.__func__)
            elif both_instance_of_type(old_attr, new_attr, property):
                update_func(old_attr.fdel, new_attr.fdel)
                update_func(old_attr.fget, new_attr.fget)
                update_func(old_attr.fset, new_attr.fset)
            elif both_instance_of_type(old_attr, new_attr, (type, types.ClassType)):
                update_class(old_attr, new_attr)