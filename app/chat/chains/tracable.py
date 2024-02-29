from typing import Any
from langfuse.model import CreateTrace
from app.chat.tracing.langfuse import langfuse


class TracableChain():
    def __call__(self, *args: Any, **kwds: Any) -> Any:
        
        chat_args = self.metadata
        trace = langfuse.trace(
            CreateTrace(
                id=chat_args["conversation_id"],
                metadata=chat_args
            )
        )

        callbacks = kwds.get('callbacks', [])
        callbacks.append(trace.getNewHandler())
        kwds["callbacks"] = callbacks
        return super().__call__(*args, **kwds)