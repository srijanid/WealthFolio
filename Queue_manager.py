import threading
import time
from queue import Queue
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class RequestQueueManager:
    def __init__(self, max_size=100, process_interval=10):
        self.queue = Queue(maxsize=max_size)
        self.process_interval = process_interval
        self.user_requests = {}
        self.start_processing()

    def start_processing(self):
        thread = threading.Thread(target=self.process_queue)
        thread.daemon = True
        thread.start()
        logging.info("Queue processing thread started")

    def process_queue(self):
        while True:
            time.sleep(self.process_interval)
            while not self.queue.empty():
                try:
                    user_id, req_data = self.queue.get()
                    self.process_request(user_id, req_data)
                except Exception as e:
                    logging.error(f"Error processing request: {e}")

            self.user_requests.clear()

    def process_request(self, user_id, req_data):
        logging.info(f"Processing request for user {user_id}: {req_data}")

    def add_request(self, user_id, req_data):
        if self.queue.full():
            logging.warning("Request queue is full")
            return False, "Request queue is full, please try again later"
        
        self.user_requests[user_id] = req_data
        self.queue.put((user_id, req_data))
        logging.info(f"Request added to the queue for user {user_id}")
        return True, "Request added to the queue successfully"

# Create an instance of the RequestQueueManager
request_queue_manager = RequestQueueManager()
