
#include <Python.h>

typedef struct Node {
    int data;
    struct Node* next;
} Node;

typedef struct {
    PyObject_HEAD
    Node* front;
    Node* rear;
} Queue;

static void Queue_dealloc(Queue* self) {
    Node* current = self->front;
    while (current != NULL) {
        Node* next = current->next;
        PyMem_Free(current);
        current = next;
    }
    Py_TYPE(self)->tp_free((PyObject*)self);
}

static PyObject* Queue_new(PyTypeObject* type, PyObject* args, PyObject* kwds) {
    Queue* self;
    self = (Queue*)type->tp_alloc(type, 0);
    if (self != NULL) {
        self->front = self->rear = NULL;
    }
    return (PyObject*)self;
}

static int Queue_init(Queue* self, PyObject* args, PyObject* kwds) {
    return 0;
}

static PyObject* Queue_enqueue(Queue* self, PyObject* args) {
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

    if (self->rear == NULL) {
        self->front = self->rear = newNode;
    } else {
        self->rear->next = newNode;
        self->rear = newNode;
    }

    Py_RETURN_NONE;
}

static PyObject* Queue_dequeue(Queue* self, PyObject* Py_UNUSED(ignored)) {
    if (self->front == NULL) {
        PyErr_SetString(PyExc_IndexError, "dequeue from empty queue");
        return NULL;
    }

    Node* oldFront = self->front;
    int data = oldFront->data;
    self->front = oldFront->next;

    if (self->front == NULL) {
        self->rear = NULL;
    }

    PyMem_Free(oldFront);

    return PyLong_FromLong(data);
}

static PyMethodDef Queue_methods[] = {
    {"enqueue", (PyCFunction)Queue_enqueue, METH_VARARGS, "Enqueue an item to the queue"},
    {"dequeue", (PyCFunction)Queue_dequeue, METH_NOARGS, "Dequeue an item from the queue"},
    {NULL}  /* Sentinel */
};

static PyTypeObject QueueType = {
    PyVarObject_HEAD_INIT(NULL, 0)
    .tp_name = "cpython.Queue",
    .tp_doc = "Queue object",
    .tp_basicsize = sizeof(Queue),
    .tp_itemsize = 0,
    .tp_flags = Py_TPFLAGS_DEFAULT,
    .tp_new = Queue_new,
    .tp_init = (initproc)Queue_init,
    .tp_dealloc = (destructor)Queue_dealloc,
    .tp_methods = Queue_methods,
};

static PyModuleDef cpython_module = {
    PyModuleDef_HEAD_INIT,
    .m_name = "cpython",
    .m_doc = "CPython implementations of data structures and algorithms.",
    .m_size = -1,
};

PyMODINIT_FUNC PyInit_cpython(void) {
    PyObject* m;
    if (PyType_Ready(&QueueType) < 0)
        return NULL;

    m = PyModule_Create(&cpython_module);
    if (m == NULL)
        return NULL;

    Py_INCREF(&QueueType);
    if (PyModule_AddObject(m, "Queue", (PyObject*)&QueueType) < 0) {
        Py_DECREF(&QueueType);
        Py_DECREF(m);
        return NULL;
    }

    return m;
}
