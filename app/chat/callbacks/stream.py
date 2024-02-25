from typing import Any, Dict, List
from uuid import UUID
from langchain.callbacks.base import BaseCallbackHandler
from langchain_core.messages import BaseMessage

class StreamingHandler(BaseCallbackHandler):
    def __init__(self, queue) -> None:
        self.queue = queue
        self.streaming_chat_ids = set()
    
    def on_chat_model_start(self, serialized: Dict[str, Any], messages: List[List[BaseMessage]], *, run_id: UUID, parent_run_id: UUID | None = None, tags: List[str] | None = None, metadata: Dict[str, Any] | None = None, **kwargs: Any) -> Any:
        if serialized["kwargs"]["streaming"] is True:
            self.streaming_chat_ids.add(run_id)
            print("Streaming chain Id, ", run_id)
        

    def on_llm_new_token(self, token, **kwargs):
        self.queue.put(token)

    def on_llm_end(self, response, run_id, **kwargs):
        if run_id in self.streaming_chat_ids:
            self.queue.put(None)
            self.streaming_chat_ids.remove(run_id)

    def on_llm_error(self, error):
        self.queue.put(None)
