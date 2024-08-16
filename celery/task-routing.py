from celery import Celery, Task
from celery.utils.log import get_task_logger
from collections import defaultdict, deque
import time
import random

app = Celery('file_processing', broker='pyamqp://localhost//')

logger = get_task_logger(__name__)

class TaskRouter:
    """
    Class responsible for routing file processing tasks dynamically based on performance metrics.
    """
    
    def __init__(self, max_concurrency=5):
        self.task_queues = defaultdict(list)
        self.performance_metrics = defaultdict(lambda: {'exec_time': 0, 'errors': 0, 'priority': 1})
        self.task_history = defaultdict(deque)  # Keep track of the last N executions
        self.max_concurrency = max_concurrency
        self.current_concurrency = 0

    def add_task(self, task_name, task_func):
        """
        Add a task to the routing system.
        
        :param task_name: Name of the task
        :param task_func: Function representing the task
        """
        self.task_queues[task_name].append(task_func)
    
    def route_task(self, task_name, *args, **kwargs):
        """
        Route a task based on its performance metrics and priority.
        
        :param task_name: Name of the task to route
        :return: Result of the task execution
        """
        task_list = self.task_queues.get(task_name, [])
        
        if not task_list:
            logger.error(f"No tasks found for {task_name}")
            return None

        if self.current_concurrency >= self.max_concurrency:
            logger.warning(f"Max concurrency reached. Task {task_name} is waiting.")
            time.sleep(1)  # Simple delay mechanism; can be replaced with a more sophisticated queue system
        
        # Select task based on a weighted metric (execution time, error count, and priority)
        selected_task = min(task_list, key=lambda task: 
            (self.performance_metrics[task_name]['exec_time'] * self.performance_metrics[task_name]['priority']) + 
            (self.performance_metrics[task_name]['errors'] * 2)  # Higher weight for errors
        )

        start_time = time.time()
        try:
            self.current_concurrency += 1
            result = selected_task(*args, **kwargs)
            exec_time = time.time() - start_time

            self.performance_metrics[task_name]['exec_time'] = exec_time
            self.task_history[task_name].append((result, exec_time))
            if len(self.task_history[task_name]) > 10:  # Keep history of the last 10 executions
                self.task_history[task_name].popleft()

            logger.info(f"Executed {task_name} in {exec_time:.2f} seconds")
        except Exception as e:
            self.performance_metrics[task_name]['errors'] += 1
            logger.error(f"Task {task_name} failed with error: {e}")
            result = None
        finally:
            self.current_concurrency -= 1
        
        return result
    
    def get_task_history(self, task_name):
        """
        Get the history of a task's execution.
        
        :param task_name: Name of the task
        :return: List of past executions
        """
        return list(self.task_history[task_name])

 
@app.task(bind=True, max_retries=3)
def virus_scan(self, file_path):
    """
    Task to perform a virus scan on the uploaded file.
    
    :param file_path: Path to the uploaded file
    :return: Result of the virus scan
    """
    try:
        # Simulating a potential intermittent failure
        if random.choice([True, False]):
            raise ValueError("Simulated scan failure")
        
        time.sleep(2) 
        return f"Virus scan completed for {file_path}"
    except Exception as exc:
        logger.error(f"Error in virus_scan for {file_path}: {exc}")
        self.retry(exc=exc, countdown=5)

@app.task(bind=True, max_retries=3)
def resize_image(self, file_path, size=(800, 600)):
    """
    Task to resize an image to the specified dimensions.
    
    :param file_path: Path to the image file
    :param size: Desired size (width, height) as a tuple
    :return: Result of the resizing operation
    """
    try:
        # Simulating a potential intermittent failure
        if random.choice([True, False]):
            raise ValueError("Simulated resize failure")
        
        time.sleep(1)
        return f"Image {file_path} resized to {size[0]}x{size[1]}"
    except Exception as exc:
        logger.error(f"Error in resize_image for {file_path}: {exc}")
        self.retry(exc=exc, countdown=5)

@app.task(bind=True, max_retries=3)
def extract_metadata(self, file_path):
    """
    Task to extract metadata from the uploaded file.
    
    :param file_path: Path to the uploaded file
    :return: Extracted metadata
    """
    try:
        # Simulating a potential intermittent failure
        if random.choice([True, False]):
            raise ValueError("Simulated metadata extraction failure")
        
        time.sleep(1.5)
        return f"Metadata extracted from {file_path}"
    except Exception as exc:
        logger.error(f"Error in extract_metadata for {file_path}: {exc}")
        self.retry(exc=exc, countdown=5)



router = TaskRouter(max_concurrency=3)
router.add_task('virus_scan', virus_scan.delay)
router.add_task('resize_image', resize_image.delay)
router.add_task('extract_metadata', extract_metadata.delay)

 
file1_result = router.route_task('virus_scan', '/path/to/file1')
file2_result = router.route_task('resize_image', '/path/to/image2.jpg', size=(1024, 768))
file3_result = router.route_task('extract_metadata', '/path/to/file3.docx')

print(file1_result)
print(file2_result)
print(file3_result)
 
print("Virus Scan Task History:", router.get_task_history('virus_scan'))
