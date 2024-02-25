from flask import current_app
from queue import Queue
from threading import Thread
from app.chat.callbacks.stream import StreamingHandler
class StreamableChain:

    def stream(self, input):
        queue = Queue()
        handler = StreamingHandler(queue)

        def task(app_context):
            app_context.push()
            self(input, callbacks=[handler])
        
        Thread(
            target=task,
            args=[current_app.app_context()]
            ).start() #for running the concurrent process

        while True: #keep running the loop
            token = queue.get() # get the token from the process
            if(token is None): #break the loop
                break
            yield token #add the token to the process
