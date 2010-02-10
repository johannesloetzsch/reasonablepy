# This file was created automatically by SWIG 1.3.28.
# Don't modify this file, modify the SWIG interface instead.
# This file is compatible with both classic and new-style classes.

import _xsb
import new
new_instancemethod = new.instancemethod
def _swig_setattr_nondynamic(self,class_type,name,value,static=1):
    if (name == "thisown"): return self.this.own(value)
    if (name == "this"):
        if type(value).__name__ == 'PySwigObject':
            self.__dict__[name] = value
            return
    method = class_type.__swig_setmethods__.get(name,None)
    if method: return method(self,value)
    if (not static) or hasattr(self,name):
        self.__dict__[name] = value
    else:
        raise AttributeError("You cannot add attributes to %s" % self)

def _swig_setattr(self,class_type,name,value):
    return _swig_setattr_nondynamic(self,class_type,name,value,0)

def _swig_getattr(self,class_type,name):
    if (name == "thisown"): return self.this.own()
    method = class_type.__swig_getmethods__.get(name,None)
    if method: return method(self)
    raise AttributeError,name

import types
try:
    _object = types.ObjectType
    _newclass = 1
except AttributeError:
    class _object : pass
    _newclass = 0
del types



create_string_array = _xsb.create_string_array

assign_string = _xsb.assign_string

print_string_array = _xsb.print_string_array

release_string_array = _xsb.release_string_array

pcharlist2string = _xsb.pcharlist2string

intpointer = _xsb.intpointer

ptoc_int = _xsb.ptoc_int

ptoc_float = _xsb.ptoc_float

ptoc_string = _xsb.ptoc_string

ptoc_longstring = _xsb.ptoc_longstring

ctop_int = _xsb.ctop_int

ctop_float = _xsb.ctop_float

ctop_string = _xsb.ctop_string

extern_ctop_string = _xsb.extern_ctop_string

string_find = _xsb.string_find

reg_term = _xsb.reg_term

c2p_int = _xsb.c2p_int

c2p_float = _xsb.c2p_float

c2p_string = _xsb.c2p_string

c2p_list = _xsb.c2p_list

c2p_nil = _xsb.c2p_nil

ensure_heap_space = _xsb.ensure_heap_space

c2p_functor = _xsb.c2p_functor

c2p_setfree = _xsb.c2p_setfree

c2p_chars = _xsb.c2p_chars

p2c_int = _xsb.p2c_int

p2c_float = _xsb.p2c_float

p2c_string = _xsb.p2c_string

p2c_functor = _xsb.p2c_functor

p2c_arity = _xsb.p2c_arity

p2c_chars = _xsb.p2c_chars

p2p_arg = _xsb.p2p_arg

p2p_car = _xsb.p2p_car

p2p_cdr = _xsb.p2p_cdr

p2p_new = _xsb.p2p_new

p2p_unify = _xsb.p2p_unify

p2p_deref = _xsb.p2p_deref

is_var = _xsb.is_var

is_int = _xsb.is_int

is_float = _xsb.is_float

is_string = _xsb.is_string

is_atom = _xsb.is_atom

is_list = _xsb.is_list

is_nil = _xsb.is_nil

is_functor = _xsb.is_functor

is_charlist = _xsb.is_charlist

is_attv = _xsb.is_attv

c2p_term = _xsb.c2p_term

p2c_term = _xsb.p2c_term

xsb_init = _xsb.xsb_init

xsb_init_string = _xsb.xsb_init_string

xsb_command = _xsb.xsb_command

xsb_command_string = _xsb.xsb_command_string

xsb_query = _xsb.xsb_query

xsb_query_string = _xsb.xsb_query_string

xsb_query_string_string = _xsb.xsb_query_string_string

xsb_query_string_string_b = _xsb.xsb_query_string_string_b

xsb_next = _xsb.xsb_next

xsb_next_string = _xsb.xsb_next_string

xsb_next_string_b = _xsb.xsb_next_string_b

xsb_get_last_answer_string = _xsb.xsb_get_last_answer_string

xsb_close_query = _xsb.xsb_close_query

xsb_close = _xsb.xsb_close

xsb_get_last_error_string = _xsb.xsb_get_last_error_string

print_pterm = _xsb.print_pterm

p_charlist_to_c_string = _xsb.p_charlist_to_c_string


