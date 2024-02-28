from functools import partial
from .sql_memory import build_memory, build_window_memory

memory_map = {
    "sql_buffer_memory": partial(build_memory),
    "sql_window_memory": build_window_memory
}