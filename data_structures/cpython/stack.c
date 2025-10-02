
#include <Python.h>

typedef struct Node {
    int data;
    struct Node* next;
} Node;

typedef struct {
    PyObject_HEAD
    Node* top;
} Stack;

static void Stack_dealloc(Stack* self) {
    Node* current = self->top;
    while (current != NULL) {
        Node* next = current->next;
        PyMem_Free(current);
        current = next;
    }
    Py_TYPE(self)->tp_free((PyObject*)self);
}

static PyObject* Stack_new(PyTypeObject* type, PyObject* args, PyObject* kwds) {
    Stack* self;
    self = (Stack*)type->tp_alloc(type, 0);
    if (self != NULL) {
        self->top = NULL;
    }
    return (PyObject*)self;
}

static int Stack_init(Stack* self, PyObject* args, PyObject* kwds) {
    return 0;
}

static PyObject* Stack_push(Stack* self, PyObject* args) {
    int data;
    if (!PyArg_ParseTuple(args, "i", &data)) {
        return NULL;
    }

    Node* newNode = (Node*)PyMem_Malloc(sizeof(Node));
    if (newNode == NULL) {
        return PyErr_NoMemory();
    }
    newNode->data = data;
    newNode->next = self->top;
    self->top = newNode;

    Py_RETURN_NONE;
}

static PyObject* Stack_pop(Stack* self, PyObject* Py_UNUSED(ignored)) {
    if (self->top == NULL) {
        PyErr_SetString(PyExc_IndexError, "pop from empty stack");
        return NULL;
    }

    Node* oldTop = self->top;
    int data = oldTop->data;
    self->top = oldTop->next;
    PyMem_Free(oldTop);

    return PyLong_FromLong(data);
}

static PyMethodDef Stack_methods[] = {
    {"push", (PyCFunction)Stack_push, METH_VARARGS, "Push an item onto the stack"},
    {"pop", (PyCFunction)Stack_pop, METH_NOARGS, "Pop an item from the stack"},
    {NULL}  /* Sentinel */
};

static PyTypeObject StackType = {
    PyVarObject_HEAD_INIT(NULL, 0)
    .tp_name = "cpython.Stack",
    .tp_doc = "Stack object",
    .tp_basicsize = sizeof(Stack),
    .tp_itemsize = 0,
    .tp_flags = Py_TPFLAGS_DEFAULT,
    .tp_new = Stack_new,
    .tp_init = (initproc)Stack_init,
    .tp_dealloc = (destructor)Stack_dealloc,
    .tp_methods = Stack_methods,
};

static PyModuleDef cpython_module = {
    PyModuleDef_HEAD_INIT,
    .m_name = "cpython",
    .m_doc = "CPython implementations of data structures and algorithms.",
    .m_size = -1,
};

PyMODINIT_FUNC PyInit_cpython(void) {
    PyObject* m;
    if (PyType_Ready(&StackType) < 0)
        return NULL;

    m = PyModule_Create(&cpython_module);
    if (m == NULL)
        return NULL;

    Py_INCREF(&StackType);
    if (PyModule_AddObject(m, "Stack", (PyObject*)&StackType) < 0) {
        Py_DECREF(&StackType);
        Py_DECREF(m);
        return NULL;
    }

    return m;
}
