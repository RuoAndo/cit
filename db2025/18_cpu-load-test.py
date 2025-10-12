# cpu_load_controller.py
# CPU Load Generator: 50% usage for 10 seconds with progress display

import multiprocessing
import time

def burn(load, duration):
    period = 0.1
    busy = period * load
    idle = period * (1 - load)
    end_time = time.time() + duration
    last_report = time.time()

    while time.time() < end_time:
        start = time.time()
        while (time.time() - start) < busy:
            pass  # Busy loop
        time.sleep(idle)
        if time.time() - last_report >= 1:
            elapsed = duration - (end_time - time.time())
            print(f"Elapsed: {elapsed:.1f}s")
            last_report = time.time()

if __name__ == "__main__":
    load = 0.5
    duration = 10
    print(f"Starting CPU load test: {load*100:.0f}% for {duration}s")

    cores = multiprocessing.cpu_count()
    processes = [multiprocessing.Process(target=burn, args=(load, duration)) for _ in range(cores)]
    for p in processes: p.start()
    for p in processes: p.join()

    print("CPU load test complete.")
