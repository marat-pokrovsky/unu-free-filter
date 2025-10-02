
#include <Python.h>

#define HASH_TABLE_SIZE 100

typedef struct Node {
    char* key;
    int value;
    struct Node* next;
} Node;

typedef struct {
    PyObject_HEAD
    Node* table[HASH_TABLE_SIZE];
} HashTable;

static unsigned int hash(const char* key) {
    unsigned int hash = 0;
    while (*key) {
        hash = (hash << 5) + *key++;
    }
    return hash % HASH_TABLE_SIZE;
}

static void HashTable_dealloc(HashTable* self) {
    for (int i = 0; i < HASH_TABLE_SIZE; i++) {
        Node* current = self->table[i];
        while (current != NULL) {
            Node* next = current->next;
            PyMem_Free(current->key);
            PyMem_Free(current);
            current = next;
        }
    }
    Py_TYPE(self)->tp_free((PyObject*)self);
}

static PyObject* HashTable_new(PyTypeObject* type, PyObject* args, PyObject* kwds) {
    HashTable* self;
    self = (HashTable*)type->tp_alloc(type, 0);
    if (self != NULL) {
        for (int i = 0; i < HASH_TABLE_SIZE; i++) {
            self->table[i] = NULL;
        }
    }
    return (PyObject*)self;
}

static int HashTable_init(HashTable* self, PyObject* args, PyObject* kwds) {
    return 0;
}

static PyObject* HashTable_set(HashTable* self, PyObject* args) {
    char* key;
    int value;
    if (!PyArg_ParseTuple(args, "si", &key, &value)) {
        return NULL;
    }

    unsigned int index = hash(key);
    Node* newNode = (Node*)PyMem_Malloc(sizeof(Node));
    if (newNode == NULL) {
        return PyErr_NoMemory();
    }
    newNode->key = PyMem_Malloc(strlen(key) + 1);
    if (newNode->key == NULL) {
        PyMem_Free(newNode);
        return PyErr_NoMemory();
    }
    strcpy(newNode->key, key);
    newNode->value = value;
    newNode->next = self->table[index];
    self->table[index] = newNode;

    Py_RETURN_NONE;
}

static PyObject* HashTable_get(HashTable* self, PyObject* args) {
    char* key;
    if (!PyArg_ParseTuple(args, "s", &key)) {
        return NULL;
    }

    unsigned int index = hash(key);
    Node* current = self->table[index];
    while (current != NULL) {
        if (strcmp(current->key, key) == 0) {
            return PyLong_FromLong(current->value);
        }
        current = current->next;
    }

    PyErr_SetString(PyExc_KeyError, key);
    return NULL;
}

static PyMethodDef HashTable_methods[] = {
    {"set", (PyCFunction)HashTable_set, METH_VARARGS, "Set a key-value pair in the hash table"},
    {"get", (PyCFunction)HashTable_get, METH_VARARGS, "Get a value from the hash table by key"},
    {NULL}  /* Sentinel */
};

static PyTypeObject HashTableType = {
    PyVarObject_HEAD_INIT(NULL, 0)
    .tp_name = "cpython.HashTable",
    .tp_doc = "Hash table object",
    .tp_basicsize = sizeof(HashTable),
    .tp_itemsize = 0,
    .tp_flags = Py_TPFLAGS_DEFAULT,
    .tp_new = HashTable_new,
    .tp_init = (initproc)HashTable_init,
    .tp_dealloc = (destructor)HashTable_dealloc,
    .tp_methods = HashTable_methods,
};

static PyModuleDef cpython_module = {
    PyModuleDef_HEAD_INIT,
    .m_name = "cpython",
    .m_doc = "CPython implementations of data structures and algorithms.",
    .m_size = -1,
};

PyMODINIT_FUNC PyInit_cpython(void) {
    PyObject* m;
    if (PyType_Ready(&HashTableType) < 0)
        return NULL;

    m = PyModule_Create(&cpython_module);
    if (m == NULL)
        return NULL;

    Py_INCREF(&HashTableType);
    if (PyModule_AddObject(m, "HashTable", (PyObject*)&HashTableType) < 0) {
        Py_DECREF(&HashTableType);
        Py_DECREF(m);
        return NULL;
    }

    return m;
}
