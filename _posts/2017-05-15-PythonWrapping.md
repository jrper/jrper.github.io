---
title: Ways to wrap C code for python - Part I
tag: python
---

Lets say you have some C code like the following


{% highlight c %}

/* example.h */

#ifndef _EXAMPLE_H
#define _EXAMPLE_H 1

void hello_name(char* );

#endif /* _EXAMPLE_H */

{% endhighlight %}

{% highlight c %}

/* example.c */

#include "example.h"
#include "stdio.h"

void hello_name(char *name){
  printf("Hello %s!\n",name);
}

{% endhighlight %}

You would like to be able to use this code in python. Option one is to do it manually. We need to write up a module wrapping the function

{% highlight C %}

/* example_wrap.c */

#include "example.h"
#include "Python.h"

static PyObject *example_hello_name(PyObject *self, PyObject *args) {
  char* name;
  if (!PyArg_ParseTuple(args, "s", &name)) {
      return NULL;
  }
  hello_name(name);
  Py_RETURN_NONE; 
}

static PyMethodDef exampleMethods[] = {
	{ (char *)"hello_name", (PyCFunction) example_hello_name, METH_VARARGS, "Print hello with a name"},
	{ NULL, NULL, 0, NULL }
};

PyMODINIT_FUNC initexample() {
  Py_InitModule3("example", exampleMethods, "Print world");
}

{% endhighlight %}

We can also throw together an installation script:

{% highlight python %}

% setup.py

from distutils.core import setup, Extension
setup(name='example', version='1.0',  \
      ext_modules=[Extension('example', ['example.c','example_wrap.c'])])

{% endhighlight %}


Now we can run `python setup install` and generate a file `example.so` which can be imported, containing a wrapped version of our function.
