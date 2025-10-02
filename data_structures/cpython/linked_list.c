
#include <Python.h>

typedef struct Node {
    int data;
    struct Node* next;
} Node;

typedef struct {
    PyObject_HEAD
    Node* head;
} LinkedList;

static void LinkedList_dealloc(LinkedList* self) {
    Node* current = self->head;
    while (current != NULL) {
        Node* next = current->next;
        PyMem_Free(current);
        current = next;
    }
    Py_TYPE(self)->tp_free((PyObject*)self);
}

static PyObject* LinkedList_new(PyTypeObject* type, PyObject* args, PyObject* kwds) {
    LinkedList* self;
    self = (LinkedList*)type->tp_alloc(type, 0);
    if (self != NULL) {
        self->head = NULL;
    }
    return (PyObject*)self;
}

static int LinkedList_init(LinkedList* self, PyObject* args, PyObject* kwds) {
    return 0;
}

static PyObject* LinkedList_append(LinkedList* self, PyObject* args) {
    int data;
    if (!PyArg_ParseTuple(args, "i", &data)) {
        return NULL;
    }

    Node* newNode = (Node*)PyMem_Malloc(sizeof(Node));
    if (newNode == NULL) {
        return PyErr_NoMemory();
    }
    newNode->data = data;
    newNode->next = NULL;

    if (self->head == NULL) {
        self->head = newNode;
    } else {
        Node* last = self->head;
        while (last->next != NULL) {
            last = last->next;
        }
        last->next = newNode;
    }

    Py_RETURN_NONE;
}

static PyObject* LinkedList_print(LinkedList* self, PyObject* Py_UNUSED(ignored)) {
    Node* current = self->head;
    while (current != NULL) {
        printf("%d ", current->data);
        current = current->next;
    }
    printf("\n");
    Py_RETURN_NONE;
}

static PyMethodDef LinkedList_methods[] = {
    {"append", (PyCFunction)LinkedList_append, METH_VARARGS, "Append an item to the linked list"},
    {"print", (PyCFunction)LinkedList_print, METH_NOARGS, "Print the linked list"},
    {NULL}  /* Sentinel */
};

static PyTypeObject LinkedListType = {
    PyVarObject_HEAD_INIT(NULL, 0)
    .tp_name = "cpython.LinkedList",
    .tp_doc = "Linked list object",
    .tp_basicsize = sizeof(LinkedList),
    .tp_itemsize = 0,
    .tp_flags = Py_TPFLAGS_DEFAULT,
    .tp_new = LinkedList_new,
    .tp_init = (initproc)LinkedList_init,
    .tp_dealloc = (destructor)LinkedList_dealloc,
    .tp_methods = LinkedList_methods,
};

static PyModuleDef cpython_module = {
    PyModuleDef_HEAD_INIT,
    .m_name = "cpython",
    .m_doc = "CPython implementations of data structures and algorithms.",
    .m_size = -1,
};

PyMODINIT_FUNC PyInit_cpython(void) {
    PyObject* m;
    if (PyType_Ready(&LinkedListType) < 0)
        return NULL;

    m = PyModule_Create(&cpython_module);
    if (m == NULL)
        return NULL;

    Py_INCREF(&LinkedListType);
    if (PyModule_AddObject(m, "LinkedList", (PyObject*)&LinkedListType) < 0) {
        Py_DECREF(&LinkedListType);
        Py_DECREF(m);
        return NULL;
    }

    return m;
}
