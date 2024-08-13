# processing user-uploaded files (e.g., images, documents) and performing operations like virus scanning, image resizing, and metadata extraction.

from celery import Celery, Task
from celery.utils.log import get_task_logger
from collections import defaultdict
import time


app = Celery('file_processing', broker='pyamqp://localhost//')

logger = get_task_logger(__name__)

class TaskRouter:
    """
    Class responsible for routing file processing tasks dynamically based on performance metrics.
    """
    
    def __init__(self):
        self.task_queues = defaultdict(list)
        self.performance_metrics = defaultdict(lambda: {'exec_time': 0, 'priority': 0})

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
        task_list = self.task_queues[task_name]
        if not task_list:
            logger.error(f"No tasks found for {task_name}")
            return None

         
        selected_task = min(task_list, key=lambda task: self.performance_metrics[task_name]['exec_time']) # Simple routing based on execution time

        start_time = time.time()
        result = selected_task(*args, **kwargs)
        exec_time = time.time() - start_time

        self.performance_metrics[task_name]['exec_time'] = exec_time

        logger.info(f"Executed {task_name} in {exec_time:.2f} seconds")

        return result

 
@app.task
def virus_scan(file_path):
    """
    Task to perform a virus scan on the uploaded file.
    
    :param file_path: Path to the uploaded file
    :return: Result of the virus scan
    """
    time.sleep(2) 
    return f"Virus scan completed for {file_path}"

@app.task
def resize_image(file_path, size=(800, 600)):
    """
    Task to resize an image to the specified dimensions.
    
    :param file_path: Path to the image file
    :param size: Desired size (width, height) as a tuple
    :return: Result of the resizing operation
    """
    time.sleep(1) 
    return f"Image {file_path} resized to {size[0]}x{size[1]}"

@app.task
def extract_metadata(file_path):
    """
    Task to extract metadata from the uploaded file.
    
    :param file_path: Path to the uploaded file
    :return: Extracted metadata
    """
    time.sleep(1.5)   
    return f"Metadata extracted from {file_path}"

 

router = TaskRouter()
router.add_task('virus_scan', virus_scan.delay)
router.add_task('resize_image', resize_image.delay)
router.add_task('extract_metadata', extract_metadata.delay)
 
file1_result = router.route_task('virus_scan', '/path/to/file1')
file2_result = router.route_task('resize_image', '/path/to/image2.jpg', size=(1024, 768))
file3_result = router.route_task('extract_metadata', '/path/to/file3.docx')

print(file1_result)
print(file2_result)
print(file3_result)
