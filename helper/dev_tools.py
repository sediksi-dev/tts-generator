import concurrent.futures
import time


def measure_execution_time(func, *args, **kwargs):
    start_time = time.time()  # Waktu sebelum fungsi dijalankan
    result = func(*args, **kwargs)  # Menjalankan fungsi
    end_time = time.time()  # Waktu setelah fungsi selesai dijalankan
    duration = end_time - start_time  # Menghitung durasi eksekusi
    return duration, result


def parallel_process(func, args_list, max_workers=10):
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(func, *args) for args in args_list]
        results = []
        for future in concurrent.futures.as_completed(futures):
            results.extend(future.result())
    return results
