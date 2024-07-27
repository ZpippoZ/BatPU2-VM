import threading
import time

start = time.perf_counter()


def gui():
    ...


def vm():
    ...


gui_thread = threading.Thread(target=gui)
vm_thread = threading.Thread(target=vm)

gui_thread.start()
vm_thread.start()

finish = time.perf_counter()

print(round(finish - start, 5))
