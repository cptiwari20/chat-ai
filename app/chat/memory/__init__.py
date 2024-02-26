from functools import partial
from .sql_memory import build_memory

memory_map = {
    "sql_buffer_memory": partial(build_memory)
}