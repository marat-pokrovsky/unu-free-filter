from fastapi import APIRouter
from ..logic import (
    doubly_linked_list_logic,
    hash_table_logic,
    linked_list_logic,
    stack_logic,
    queue_logic
)

router = APIRouter()

@router.post("/doubly-linked-list")
def doubly_linked_list_endpoint(data: list):
    """Endpoint to create a doubly linked list from a list of elements."""
    return doubly_linked_list_logic(data)

@router.post("/hash-table")
def hash_table_endpoint(data: list):
    """Endpoint to create a hash table from a list of elements."""
    return hash_table_logic(data)

@router.post("/linked-list")
def linked_list_endpoint(data: list):
    """Endpoint to create a linked list from a list of elements."""
    return linked_list_logic(data)

@router.post("/stack")
def stack_endpoint(data: list):
    """Endpoint to create a stack from a list of elements."""
    return stack_logic(data)

@router.post("/queue")
def queue_endpoint(data: list):
    """Endpoint to create a queue from a list of elements."""
    return queue_logic(data)
