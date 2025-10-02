from fastapi import APIRouter
from ..logic import (
    bubble_sort_logic,
    heap_sort_logic,
    insertion_sort_logic,
    merge_sort_logic,
    quick_sort_logic,
    selection_sort_logic,
)

router = APIRouter()

@router.post("/bubble-sort")
def bubble_sort_endpoint(data: list):
    """Endpoint to sort a list using bubble sort."""
    return bubble_sort_logic(data)

@router.post("/heap-sort")
def heap_sort_endpoint(data: list):
    """Endpoint to sort a list using heap sort."""
    return heap_sort_logic(data)

@router.post("/insertion-sort")
def insertion_sort_endpoint(data: list):
    """Endpoint to sort a list using insertion sort."""
    return insertion_sort_logic(data)

@router.post("/merge-sort")
def merge_sort_endpoint(data: list):
    """Endpoint to sort a list using merge sort."""
    return merge_sort_logic(data)

@router.post("/quick-sort")
def quick_sort_endpoint(data: list):
    """Endpoint to sort a list using quick sort."""
    return quick_sort_logic(data)

@router.post("/selection-sort")
def selection_sort_endpoint(data: list):
    """Endpoint to sort a list using selection sort."""
    return selection_sort_logic(data)
