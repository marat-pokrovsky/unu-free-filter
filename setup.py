from distutils.core import setup, Extension

setup(
    name="cpython",
    version="1.0",
    ext_modules=[
        Extension(
            "cpython",
            [
                "data_structures/cpython/linked_list.c",
                "data_structures/cpython/doubly_linked_list.c",
                "data_structures/cpython/stack.c",
                "data_structures/cpython/queue.c",
                "data_structures/cpython/hash_table.c",
            ],
        )
    ],
)
