def run_batch_job(data):
    """
    Run a batch job with a sequence of tasks, ensuring correct execution order, data integrity, and handling failures.
    
    :param data: Initial data to be processed
    :return: Final result of the job execution
    """
    job_manager = JobManager()
    partial_result_manager = PartialResultManager()

    #we are adding our tasks to the job pipeline
    job_manager.add_task(task_a, data)
    job_manager.add_task(task_b)
    job_manager.add_task(task_c)

    # now execute the job
    try:
        result = job_manager.execute()
        logger.info(f"Job completed successfully: {result.get()}")
    except Exception as exc:
        job_manager.handle_failure(task_c)
        partial_result_manager.handle_error(task_c, exc)
        result = partial_result_manager.get_partial_result(task_c.name)
        if result:
            logger.info(f"Continuing with partial results: {result}")
        else:
            logger.error("Job failed and no partial results are available.")
    return result


if __name__ == '__main__':
    initial_data = 10  
    final_result = run_batch_job(initial_data)
    print(f"Final result of the batch job: {final_result}")
