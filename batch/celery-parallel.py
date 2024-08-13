class JobManager:
    """
    Class responsible for managing and executing jobs in sequence.
    """

    def __init__(self):
        self.tasks = []

    def add_task(self, task, *args, **kwargs):
        """
        Add a task to the job pipeline.
        
        :param task: Celery task to be added to the job
        :param args: Arguments for the task
        :param kwargs: Keyword arguments for the task
        """
        self.tasks.append(task.s(*args, **kwargs))

    def execute(self):
        """
        Execute the job tasks in sequence.
        
        :return: Result of the chained task execution
        """
        job_chain = chain(*self.tasks)
        result = job_chain.apply_async()
        return result

    def handle_failure(self, task):
        """
        Handle task failures with custom logic.
        
        :param task: The task that failed
        """
        logger.error(f"Task {task.name} failed. Executing rollback.")
        self.rollback()

    def rollback(self):
        """
        Implement rollback mechanism to revert changes in case of failure.
        """
        logger.info("Rolling back changes...")
        # TODO: we can add rollback logic here (e.g., reverting database changes, deleting files)

class PartialResultManager:
    """
    Class responsible for managing partial results and handling errors.
    """

    def __init__(self):
        self.partial_results = {}

    def store_partial_result(self, task_name, result):
        """
        Store the partial result of a completed task.
        
        :param task_name: Name of the task
        :param result: Result of the task
        """
        self.partial_results[task_name] = result
        logger.info(f"Stored partial result for {task_name}")

    def get_partial_result(self, task_name):
        """
        Retrieve the partial result of a task.
        
        :param task_name: Name of the task
        :return: Partial result of the task
        """
        return self.partial_results.get(task_name, None)

    def handle_error(self, task, exc):
        """
        Handle errors by logging and continuing with partial results.
        
        :param task: The task that failed
        :param exc: The exception that caused the failure
        """
        logger.error(f"Task {task.name} failed with error: {exc}. Continuing with partial results.")
        

@app.task(bind=True)
def task_a(self, data):
    """
    First task in the chain: Data preprocessing.
    
    :param data: Input data
    :return: Processed data
    """
    try:
        logger.info("Task A: Preprocessing data")
 
        processed_data = data * 2
        return processed_data
    except Exception as exc:
        self.retry(exc=exc)

@app.task(bind=True)
def task_b(self, data):
    """
    Second task in the chain: Data analysis.
    
    :param data: Output from task_a
    :return: Analyzed data
    """
    try:
        logger.info("Task B: Analyzing data")
        
        analyzed_data = data + 3
        return analyzed_data
    except Exception as exc:
        self.retry(exc=exc)

@app.task(bind=True)
def task_c(self, data):
    """
    Final task in the chain: Data storage.
    
    :param data: Output from task_b
    :return: Confirmation of data storage
    """
    try:
        logger.info("Task C: Storing data")
        
        return f"Data stored: {data}"
    except Exception as exc:
        self.retry(exc=exc)

