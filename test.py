import threading
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import socket
import queue


# Define your TCP socket thread function
def tcp_socket_thread():
    # Your TCP socket logic here
    HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
    PORT = 65432  # Port to listen on (non-privileged ports are > 1023)

    print("Start tcp server ")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        conn, addr = s.accept()
        with conn:
            print("Connected by", addr)
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                print(data)


# Define a class to handle file system events
class MyFileSystemEventHandler(FileSystemEventHandler):
    def __init__(self, thread_queue):
        super().__init__()
        self.thread_queue = thread_queue

    def on_created(self, event):
        if event.is_directory:
            return
        print(f"File created: {event.src_path}")
        thread = threading.Thread(target=self.handle_file, args=(event.src_path,))
        self.thread_queue.put(thread)

    def handle_file(self, file_path):
        # Your logic to handle the newly created file
        pass


# Define a function to watch a folder
def watch_folder_thread(thread_queue):
    print("Watch folder thread started")
    observer = Observer()
    observer.schedule(
        MyFileSystemEventHandler(thread_queue),
        "/home/shaarang/Desktop/workspace/watch",
        recursive=True,
    )
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


# Define a function to process threads from the queue
def process_thread_queue(thread_queue):
    while True:
        thread = thread_queue.get()
        thread.start()
        thread.join()


# Create a queue for threads
thread_queue = queue.Queue()

# Create and start your TCP socket thread
tcp_thread = threading.Thread(target=tcp_socket_thread)
tcp_thread.start()

# Create and start your folder watching thread
watch_folder_thread = threading.Thread(target=watch_folder_thread, args=(thread_queue,))
watch_folder_thread.start()

# Create and start a thread to process threads from the queue
process_thread_queue_thread = threading.Thread(
    target=process_thread_queue, args=(thread_queue,)
)
process_thread_queue_thread.start()
