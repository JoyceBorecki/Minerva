import psutil

def get_memory_usage_mb():
    processo = psutil.Process()
    return processo.memory_info().rss / (1024 * 1024)
