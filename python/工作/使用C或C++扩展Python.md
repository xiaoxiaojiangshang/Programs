# 使用C/C++扩展Python
	此文中所有内容在Windows/Python2.7/Visual studio 2010环境下正常运行
## 前言
### 为什么要使用C/C++扩展Python
1. 扩展Python现有模块
2. C/C++有远高于Python的性能
3. 可以使用现有的C/C++库
### 如何阅读本文

###### 本文主要包括以下几部分内容：
1. 前言
2. 一个简单的例子 
4. 如何使用C/C++扩展Python
5. 如何使用Distutil模块生成扩展文件
6. 如何使用C/C++扩展Numpy 
7. 例子
8. 参考文档
9. 代码示例

## 一个简单的例子
### C代码
这一部分包括了一个非常简单的例子，但是包含了使用C/C++扩展Python的绝大多数内容。  在这个例子中我们为Python添加了一个新的模块spam，此模块中仅仅包含一个函数system(str), 功能是在命令行中输入str中字符串对应的命令。


首先我们需要新建一个C语言文件spammodule.c。首先，为了扩展Python我们要向spammodule.c中加入最重要的头文件

	#include <Python.h> 
为了在编译过程中编译器能迅速的找到此头文件和对应的库文件，需要将相关的路径加入环境变量Path。

	提示： 由于 Python.h 中包含了一些可能会影响标准头文件的预处理指令，请将Python.h放在所有头文件的最前面。

 接下来我们为spammodule.c添加第一个函数：

``` C
static PyObject *
spam_system(PyObject *self, PyObject *args)
{
    const char *command;
    int sts;

    if (!PyArg_ParseTuple(args, "s", &command))
        return NULL;
    sts = system(command);
    return Py_BuildValue("i", sts);
}
```

对于任何一个可以从Python中调用的函数/方法，这个函数/方法总是有两个参数。一个是self，对于一个函数，self是一个空指针，对于方法self是指向这个方法对应的Python对象的指针。另一个参数是args，args是一个Python中的Tuple对象。Python中进行函数/方法调用时，参数总是以一个tuple的形式被传递。我们可以使用PyArg\_ParseTuple函数将Python中的Tuple转化为C中的数据类型，此函数的第一个参数为Python中的Tuple对象，第二个参数为参数的类型，其后各个参数是用于存放解析Tuple获得的结果的各个地址。这里的“s”即表明这个函数的参数只有一个字符串。system是stdilb中的函数。Python中的所有函数/方法都需要返回一个返回值，此处的spam.system函数如果成功执行命令, 返回0，执行失败返回非零值。Python中的任何数据都是一个对象，此处为了将C语言中的一个整数变成Python中的整数，我们需要使用函数Py\_BuildValue，这个函数的第一个参数与PyArg_ParseTuple相同,也是一个代表后续参数类型的字符串。后面就是字符串对应的数据类型的各个参数。

接下来，为了将写好的函数添加到此模块中，我们首先要添加一个方法列表
``` C
static PyMethodDef SpamMethods[] = {
    {"system",  spam_system, METH_VARARGS,
     "Execute a shell command."},
    {NULL, NULL, 0, NULL}        /* Sentinel */
};
```
方法列表中的每一项都是对模块中方法的描述。每一项中的第一个参数方法名称，就是Python中调用此函数的时候使用的名称，第二个参数是C语言中对于的函数的函数指针。第三个参数是参数Python中参数的使用形式，若为METH_VARARGS则在调用此函数的时候无法使用具名参数。第四个参数是对此函数的描述。

为了初始化此模块，我们需要一个名称为initspam的函数，此函数必须为非static类型。每个C扩展模块都必须有一个名为initname的函数对模块进行初始化，name是对应模块的名称。

``` C
PyMODINIT_FUNC
initspam(void)
{
    (void) Py_InitModule("spam", SpamMethods);
}
```

至此，使用C语言编写的扩展模块就已经编写完成。
### 编译成Python可以使用的扩展模块
我们使用Python中的Distutil模块将写好的C语言扩展模块编译成Python可用的模块。首先新建一个Python文件setup.py其中内容为：
``` python
from distutils.core import setup, Extension

module1 = Extension(name='spam',
                    version='1.0',
                    sources=['spammodule.c'])

setup (name = 'spam',
       version = '1.0',
       description = 'This is a demo package',
       ext_modules = [module1])

```
此处的name就是模块的名称，version是扩展模块的版本号，description是模块的描述。ext_modules指的是C/C++扩展模块(区别于Python扩展模块), sources是扩展模块对应的源文件。

在同一目录下执行python setup.py build会得到一个名为build的文件夹，其中又包含一个名为lib...的文件夹，此文件夹下包含一个后缀名为.pyd的文件，此文件就是编译好的扩展模块。

#### 可能出现的问题
在执行python setup.py build命令时，可能会出现 error: Unable to find vcvarsall.bat的问题，解决方法为：在..python安装路径…\Lib\distutils目录下有个msvc9compiler.py找到toolskey = “VS%0.f0COMNTOOLS” % version直接改为 toolskey = “VS你的版本COMNTOOLS”。 visual studio 10对应为 VS100COMNTOOLS，vs2013对于为 VS120COMNTOOLS 。

## 如何使用C/C++扩展Python

### 参数

Python的函数/方法有两种参数，一种是普通的参数，另一种是具名参数。

在Python中第一种参数是存在一个tuple中的。为了解析这种参数，我们需要使用PyArg_ParseTuple函数，其声明如下：

```C
int PyArg_ParseTuple(PyObject *arg, char *format, ...);
```

此函数的第二个参数format的详细说明可在Python官方文档 Python » Python 2.7.13 documentation » Python/C API Reference Manual » Utilities » Parsing arguments and building values 中查看。


对于具名参数，在编写C/C++扩展时有几处不同。首先是在定义扩展函数的时候带有具名参数的函数/方法有三个参数，形式如下：
```C
static PyObject* moudle_ext_func(PyObject* self, PyObject* arg, PyObject *kwdict)
```

其中前两个参数与普通扩展函数相同，第三个参数中储存了具名从参数的相关信息。在解析具名参数时，我们需要使用
```C
int PyArg_ParseTupleAndKeywords(PyObject *arg, PyObject *kwdict,
                                char *format, char *kwlist[], ...);
```
arg和kwdict分别对应moudle\_ext\_func中的arg和dict，format与PyArg\_ParseTuple函数作用相同。kwlist是表面命名参数名称的一个字符串数组，以NULL来标记结束。最后在方法列表中，带有具名参数传递扩展函数的第三个参数应写为  METH\_VARARGS | METH\_KEYWORDS，区别与普通函数的METH_VARARGS。下面是使用具名参数的一个例子。
```C
	static PyObject* moudle_sample(PyObject* self, PyObject* args, PyObject *keywds)
	{
		int size, i, n = 3;
		char* s;
		static char *kwlist[] = { "output", "n", NULL };
		if (!PyArg_ParseTupleAndKeywords(args, keywds, "s|i", 
			kwlist, &s, &n))
			return NULL;
		for(i = 0;i < n;i++)
			puts(s);
		Py_INCREF(Py_None);
		return Py_None;
	}
```
这个函数以一个字符串output和一个整数n为参数，将字符串在n行中每行输出一次，n的默认值为3。PyArg\_ParseTupleAndKeywords的format参数为"s|i"，其中的'|'意思为其后的参数是可选参数，如果将两个参数都改为必要参数可以写为“si”。将函数添加到方法列表的写法如下：
```c
	static PyMethodDef MoudleMethods[] = {
  	...
		 {"sample",  moudle_sample, METH_VARARGS|METH_KEYWORDS,
	     "Print a string for n times(default 3)."},
	...
	    {NULL, NULL, 0, NULL}        /* Sentinel */
	};
```
###tips
* 如何解析list、tuple等类型的参数

	将list、tuple参数作为对象传递，然后使用PyList_*、PyTuple_*、PySequence_*等函数对解析获得的对象进行操作。

###引用计数
Python中的对象通过引用计数的方式来进行垃圾回收，在C/C++中我们可以使用Py\_INCREF和Py\_DECREF函数来对PyObject增加/减少引用计数，当一个对象的引用计数减少为0时，这个对象占用的内存地址即被回收。为了防止内存泄漏和段错误，我们要小心的处理PyObject的引用计数。不过在很多情况下我们无需对此问题给予过多的关注，Python内存管理中有一种叫做borrow reference的机制。

###异常处理

异常处理在python是非常重要的一件事。当Python中函数调用失败时，我们通常要抛出异常，并给出相应提示。在错误处理中最常用的C函数是 PyErr_SetString，声明如下：
```c
	void PyErr_SetString(PyObject *type, const char *message) 
```
此函数的参数是一个异常对象和一个c string消息字符串，异常对象例如 PyExc_ZeroDivisionError、PyExc_RuntimeError， C string消息字符串会被转换为Python字符串作为异常的副值。除使用现有的异常类型，我们还可以为自己的模块添加新的异常类型。首先要在文件的起始位置定义一个全局变量：
```c
	static PyObject *SampleError;
```
此外，我们需要在初始化函数中初始化这个异常了类型：
```C
	PyMODINIT_FUNC
	initsample(void)
	{
    	PyObject *m;
	
    	m = Py_InitModule("sample", SampleMethods);
    	if (m == NULL)
    	    return;

    	SampleError = PyErr_NewException("Sample.error", NULL, NULL);
    	Py_INCREF(SampleError);//It‘s important to increase the references of SampleError
    	PyModule_AddObject(m, "error", SampleError);
	}
```
PyErr_NewException函数的后两个参数一般为NULL。详情可见Python官方文档 Python » Python 2.7.13 documentation » Python/C API Reference Manual » Exception Handling。

##使用distutil创建C/C++扩展

下面介绍如何使用Python distutil创建C/C++扩展。 先创建一个名为setup.py的文件。 在setup文件中，首先需要从 distutil.core模块中import setup函数和Extension模块。 首先我们使用Extension设置编译选项。Extension是一个对象，这个对象的初始化方法如下：
```python
	def __init__ (self, name, sources,
                  include_dirs=None,
                  define_macros=None,
                  undef_macros=None,
                  library_dirs=None,
                  libraries=None,
                  runtime_library_dirs=None,
                  extra_objects=None,
                  extra_compile_args=None,
                  extra_link_args=None,
                  export_symbols=None,
                  swig_opts = None,
                  depends=None,
                  language=None,
                  **kw                      # To catch unknown keywords
                 ):
```
我们在创建此模块的时候必须要指明模块名称，源文件列表。其他是可选编译选项。setup函数的使用较为简单，一般使用方法如下：
	setup (name = 'util',
       version = '1.0',
       description = 'utils for accelratrate computation',
       ext_modules = [ext_module])
其中name是模块名称，version是模块版本号，description是模块的描述，ext\_modules是Extension类型的对象的列表。

### 在C/C++中调用Python函数/方法
在C/C++中也能方便的调用Python中的函数/方法。Python将函数、lambda函数、方法都看作对象，这些对象都是可调用（callable）的。为了在C/C++中调用这些对象，我们首先要将这些对象的地址作为参数传递到C/C++模块中，然后在C/C++中使用PyObject_CallObject调用Python函数/方法。下面是一个例子，这个例子中我们重新实现了Python中的map函数。以下是完整的代码：

```c
#include <Python.h>
static PyObject *
sample_map(PyObject *dummy, PyObject *args)
{
	PyObject* func;
	PyObject* argsList;
	PyObject* result;
	Py_ssize_t size;
	int i;
	if (!PyArg_ParseTuple(args, "OO!", &func, &PyList_Type, &argsList)) {
		PyErr_SetString(PyExc_ValueError, "paramaters error in sample.map");
		goto fail;
	}
	if (!PyCallable_Check(&func)) {
		PyErr_SetString(PyExc_ValueError, "the frist parpmater should be callable");
		goto fail;
	}
	size = PyList_Size(argsList);
	result = PyList_New(size);
	for (i = 0; i < size; i++)
		PyList_SetItem(result, i, PyObject_CallObject(func, Py_BuildValue("(O)", PyList_GetItem(argsList, i))));
    return result;
fail:
	Py_INCREF(Py_None);
	return Py_None;
}

static PyMethodDef SampleMethods[] = {
    {"map",  sample_map, METH_VARARGS,
     "Rebuilt the wheel"},
    {NULL, NULL, 0, NULL}        /* Sentinel */
};
PyMODINIT_FUNC
initsample(void)
{
    (void) Py_InitModule("sample", SampleMethods);
}
```
## 如何使用C/C++扩展Numpy

Numpy模块是Python中执行科学计算常用的库，此处主要介绍对Numpy Array的操作。与Python中的list不同，Numpy Array更类似与C/C++中的数组，i.e, Numpy Array中的元素类型必须是相同的，对于多维数组，每一维都必须是对齐的。为了在C语言中操作Numpy Array，我们需要添加头文件：
```c
	#include <numpy/arrayobject.h>
```
下面给出一个非常简单的例子：
```c	
	static PyObject* util_reverse(PyObject* self, PyObject* args)
	{
		PyArrayObject *in_array;
		PyArrayIterObject *in_iter;
		double* a = NULL;
		npy_intp size;
		if (!PyArg_ParseTuple(args, "O!", &PyArray_Type, &in_array))
		return NULL;
		in_iter = (PyArrayIterObject*)PyArray_IterNew((PyObject*)in_array);
		a = (double*)in_iter->dataptr;
		size = in_iter->size;
		reverse(a, size);
		Py_INCREF(Py_None);
		return Py_None;
	}
```
我们需要把Numpy Array当作一个对象进行解析，PyArg\_ParseTuple(args, "O!", &PyArray_Type, &in_array)中的format字符串为“O!”，意思是将参数解析成一个指定类型(PyArray\_Type)的对象，如果不能解析成指定类型对象则返回值指示解析失败。Numpy Array中的元素在内存中是连续存放的。PyArrayIterObject是一个迭代器，其中保存了numpy array的起始位置、数据类型、数据个数等多种信息。我们使用函数PyArray\_IterNew创建一个新的迭代器，这个函数的参数是迭代器对应的numpy array。迭代器结构体中包含dataptr，size等成员，dataptr是指向array内存中起始位置的void*类型指针，size是npy\_intp类型的变量。这个npy\_intp类型对应64位或32位整数，为了避免在代码移植时出现错误，我们最好将其定义为npy_intp类型而不是int/long int类型。

### 如何新建一个Numpy Array对象
PyArray_New使用创建一个Numpy Array较为复杂，下为其声明:
```c
	PyObject* PyArray_New(PyTypeObject* subtype, int nd, npy_intp* dims, int type_num, npy_intp* strides, void* data, int itemsize, int flags, PyObject* obj)
```
为了简单起见，我们可以使用PyArray_SimpleNew来创建一个新的numpy array对象，其声明如下：
```c
	PyObject* PyArray_SimpleNew(int nd, npy_intp* dims, int typenum)
```
其中nd对应维数，一维数组nd=1，二维数组nd=2，以此类推。npy_intp是一个npy_intp类型的数组，数组长度应为nd，每个元素对应于numpy array的每一维的长度。typenum有NPY_BOOL、 NPY_SHORT、 NPY_INT、 NPY_LONGLONG、 NPY_FLOAT32、 NPY_FLOAT64等类型。

### 编译Numpy扩展

在编译Numpy扩展的时候，创建Extension对象时与之前略有差别，我们需要在构造函数中加入额外的参数，
```python
	include_dirs=[np.get_include()]
```
这是因为我们用到了numpy/arrayobject.h，却未指明其位置。我们可以使用np.get\_include()来获得numpy的各种头文件的路径。所有代码如下：
```python
	import numpy as np
	ext_module = Extension(name='npy_sample',
                    version='1.0',
                    sources=['npy_sample.c'],
					include_dirs=[np.get_include()])
```
##参考链接

* Python扩展
	
	Python官方文档

* Numpy扩展


	https://docs.scipy.org/doc/numpy/reference/c-api.html
## 代码示例

### Python扩展
* spammodule.c

```c
#include <Python.h>
static PyObject *
spam_system(PyObject *self, PyObject *args)
{
    const char *command;
    int sts;

    if (!PyArg_ParseTuple(args, "s", &command))
        return NULL;
    sts = system(command);
    return Py_BuildValue("i", sts);
}

static PyObject* spam_sample(PyObject* self, PyObject* args, PyObject *keywds)
{
	npy_intp size;
	int i, n = 3;
	char* s;
	static char *kwlist[] = { "output", "n", NULL };
	if (!PyArg_ParseTupleAndKeywords(args, keywds, "s|i", 
		kwlist, &s, &n))
		return NULL;
	for(i = 0;i < n;i++)
		puts(s);
	Py_INCREF(Py_None);
	return Py_None;
}

static PyMethodDef SpamMethods[] = {
    {"system",  spam_system, METH_VARARGS,
     "Execute a shell command."},
	 {"sample",  spam_sample, METH_VARARGS|METH_KEYWORDS,
     "Print a string for n times(default 3)."},
    {NULL, NULL, 0, NULL}        /* Sentinel */
};


PyMODINIT_FUNC
initspam(void)
{
    (void) Py_InitModule("spam", SpamMethods);
}
```


* setup.py

```python
from distutils.core import setup, Extension

module1 = Extension(name='spam',
                    version='1.0',
                    sources=['spammodule.c'])

setup (name = 'spam',
       version = '1.0',
       description = 'This is a demo package',
       ext_modules = [module1])
```

### Numpy扩展

* util.c

```c
#include < Python.h>
#include < numpy/arrayobject.h>
#include < stdio.h>
#include < math.h>
#include < assert.h>
//#define DEBUG 1

#define isnan(x) ((x) != (x))

static PyObject* util_type(PyObject* self, PyObject* args)
{
	PyArrayObject *in_array;
	if (!PyArg_ParseTuple(args, "O!", &PyArray_Type, &in_array))
		return NULL;
	printf("kind: %c\n", in_array->descr->kind);
	printf("type: %c\n", in_array->descr->type);
	printf("byte order: %c\n", in_array->descr->byteorder);
	printf("element size: %d\n", in_array->descr->elsize);
	Py_INCREF(Py_None);
	return Py_None;
}

void reverse(double *a, int len)
{
	int i;
	double tmp;
	for (i = 0; i < len / 2; i++) {
		tmp = a[len - 1 - i];
		a[len - 1 - i] = a[i];
		a[i] = tmp;
	}
}
static PyObject* util_reverse(PyObject* self, PyObject* args)
{
	PyArrayObject *in_array;
	PyArrayIterObject *in_iter;
	double* a = NULL;
	int size;
	if (!PyArg_ParseTuple(args, "O!", &PyArray_Type, &in_array))
		return NULL;
	in_iter = (PyArrayIterObject*)PyArray_IterNew((PyObject*)in_array);
	a = (double*)in_iter->dataptr;
	size = in_iter->size;
	reverse(a, size);
	Py_INCREF(Py_None);
	return Py_None;
}
static PyObject* util_print(PyObject* self, PyObject* args)
{
	PyArrayObject *in_array;
	PyArrayIterObject *in_iter;
	double* a = NULL;
	int size,i;
	if (!PyArg_ParseTuple(args, "O!", &PyArray_Type, &in_array))
		return NULL;
	in_iter = (PyArrayIterObject*)PyArray_IterNew((PyObject*)in_array);
	a = (double*)in_iter->dataptr;
	size = in_iter->size;
	printf("size = %d\n", size);
	while (in_iter->index < in_iter->size) {
		double* in_dataptr = (double *)in_iter->dataptr;
		printf("%dth: %f\n", in_iter->index, *in_dataptr);
		PyArray_ITER_NEXT(in_iter);
	}
	
	for (i = 0; i < size; i++) {
		printf("%f ",a[i]);
	}
	puts("");
	Py_INCREF(Py_None);
	return Py_None;
}
static PyObject* util_range(PyObject* self, PyObject* args)
{
	int size,i;
	double *a;
	PyArrayObject* res;
	PyArrayIterObject* iter;
	if (!PyArg_ParseTuple(args, "i", &size))
		goto fail;
	res = PyArray_SimpleNew(1, &size, NPY_DOUBLE);
	if (res == NULL)
		goto fail;
	iter = (PyArrayIterObject*)PyArray_IterNew((PyObject*)res);

	a = (double*)iter->dataptr;
	for (i = 0; i < size; i++)
		a[i] = (double)i;
	return (PyObject*)res;
fail:
	Py_INCREF(Py_None);
	return Py_None;
}

/*  define functions in module */
static PyMethodDef UtilMethods[] =
{
	{ "print_array", util_print, METH_VARARGS,
	"print a float64 numpy array" },
	{ "type", util_type, METH_VARARGS,
	"print a description of a numpy array" },
	{"reverse", util_reverse, METH_VARARGS,
	"reverse a float64 numpy array"},
	{"range", util_range, METH_VARARGS,
	"return a float64 numpy array of given length which contains 0 ~ size"},
	{ NULL, NULL, 0, NULL }
};

PyMODINIT_FUNC
initutil(void)
{
	(void)Py_InitModule("util", UtilMethods);
	import_array();
}
```

* setup.py
```python
from distutils.core import setup, Extension
import numpy as np
module1 = Extension(name='util',
                    version='1.0',
                    sources=['utils.c'],
					extra_compile_args=['-std=c99'],
					include_dirs=[np.get_include()])

setup (name = 'util',
       version = '1.0',
       description = 'utils for accelratrate computation',
       ext_modules = [module1])
```