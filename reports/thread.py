import threading
import time


def notification(name):
    time.sleep(2)
    print(f"Notification: New pothole report submitted by {name}")


def start_notification(name):
    thread = threading.Thread(target=notification, args=(name,))
    thread.start()