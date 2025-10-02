
#include <Python.h>

typedef struct Node {
    int data;
    struct Node* next;
    struct Node* prev;
} Node;

typedef struct {
    PyObject_HEAD
    Node* head;
} DoublyLinkedList;

static void DoublyLinkedList_dealloc(DoublyLinkedList* self) {
    Node* current = self->head;
    while (current != NULL) {
        Node* next = current->next;
        PyMem_Free(current);
        current = next;
    }
    Py_TYPE(self)->tp_free((PyObject*)self);
}

static PyObject* DoublyLinkedList_new(PyTypeObject* type, PyObject* args, PyObject* kwds) {
    DoublyLinkedList* self;
    self = (DoublyLinkedList*)type->tp_alloc(type, 0);
    if (self != NULL) {
        self->head = NULL;
    }
    return (PyObject*)self;
}

static int DoublyLinkedList_init(DoublyLinkedList* self, PyObject* args, PyObject* kwds) {
    return 0;
}

static PyObject* DoublyLinkedList_append(DoublyLinkedList* self, PyObject* args) {
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
        newNode->prev = NULL;
        self->head = newNode;
    } else {
        Node* last = self->head;
        while (last->next != NULL) {
            last = last->next;
        }
        last->next = newNode;
        newNode->prev = last;
    }

    Py_RETURN_NONE;
}

static PyObject* DoublyLinkedList_print(DoublyLinkedList* self, PyObject* Py_UNUSED(ignored)) {
    Node* current = self->head;
    while (current != NULL) {
        printf("%d ", current->data);
        current = current->next;
    }
    printf("\n");
    Py_RETURN_NONE;
}

static PyMethodDef DoublyLinkedList_methods[] = {
    {"append", (PyCFunction)DoublyLinkedList_append, METH_VARARGS, "Append an item to the doubly linked list"},
    {"print", (PyCFunction)DoublyLinkedList_print, METH_NOARGS, "Print the doubly linked list"},
    {NULL}  /* Sentinel */
};

static PyTypeObject DoublyLinkedListType = {
    PyVarObject_HEAD_INIT(NULL, 0)
    .tp_name = "cpython.DoublyLinkedList",
    .tp_doc = "Doubly linked list object",
    .tp_basicsize = sizeof(DoublyLinkedList),
    .tp_itemsize = 0,
    .tp_flags = Py_TPFLAGS_DEFAULT,
    .tp_new = DoublyLinkedList_new,
    .tp_init = (initproc)DoublyLinkedList_init,
    .tp_dealloc = (destructor)DoublyLinkedList_dealloc,
    .tp_methods = DoublyLinkedList_methods,
};

static PyModuleDef cpython_module = {
    PyModuleDef_HEAD_INIT,
    .m_name = "cpython",
    .m_doc = "CPython implementations of data structures and algorithms.",
    .m_size = -1,
};

PyMODINIT_FUNC PyInit_cpython(void) {
    PyObject* m;
    if (PyType_Ready(&DoublyLinkedListType) < 0)
        return NULL;

    m = PyModule_Create(&cpython_module);
    if (m == NULL)
        return NULL;

    Py_INCREF(&DoublyLinkedListType);
    if (PyModule_AddObject(m, "DoublyLinkedList", (PyObject*)&DoublyLinkedListType) < 0) {
        Py_DECREF(&DoublyLinkedListType);
        Py_DECREF(m);
        return NULL;
    }

    return m;
}
