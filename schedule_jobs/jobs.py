import os
from decouple import config
from .models import RegisterJobs, RegisterTask


def register_task(func):
    
    try:
        import inspect
        from django.core.files.base import ContentFile

        func_source = inspect.getsource(func)

        obj = RegisterTask.objects.create(name=func.__name__)
        print(obj.name)
        obj.task_file.save(f"{func.__name__}.txt", ContentFile(func_source))
    except Exception as e:

        # Add logger
        print(e)


def add_job(registered_name, task_name, year, month, day, hour, min, periodic, **kwargs):

    import datetime

    TASK_HOLDER_PATH = config('TASK_HOLDER_PATH')
    CRON_TEMPLATE_BASH_PATH = config('CRON_TEMPLATE_BASH_PATH')
    # PROJECT_PATH = config('PROJECT_PATH')

    task_temp_obj = RegisterTask.objects.get(name=registered_name)
    job_obj = RegisterJobs(task_name=task_name, scheduled_hour=hour, scheduled_min=min,
                            scheduled_date=datetime.datetime(year, month, day), task_template=task_temp_obj, periodic=periodic)
    job_obj.save()

    with open(f"{TASK_HOLDER_PATH}/{job_obj.pk}.py", 'w') as f1, open(f"{task_temp_obj.task_file.path}", 'r') as f2:

        for line in f2:
            f1.write(line)
        
        extra_content = ''

        if not job_obj.periodic:
            extra_content = f"""
            
if __name__ == '__main__':
    import datetime

    if '{job_obj.scheduled_date.date()}' == datetime.date.today().strftime('%Y-%m-%d'):
        {registered_name}(**{kwargs})
            """
            
        else:
            extra_content = f"""

if __name__ == '__main__':

    {registered_name}(**{kwargs})
            """
        
        f1.write(extra_content)
        os.system(f'(crontab -l; echo "{min} {hour} * * * bash {CRON_TEMPLATE_BASH_PATH} {TASK_HOLDER_PATH}/{job_obj.pk}.py {job_obj.pk}") | crontab -')
    
    return job_obj.pk