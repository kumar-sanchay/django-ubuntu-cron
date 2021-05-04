from django.test import TestCase
from .jobs import register_task, add_job



def my_task(a, b):
    return a+b

class TestResgisterTask(TestCase):

    # def test_creating_task(self):
    #     register_task(my_task)
    
    def setUp(self):
        register_task(my_task)

    def test_add_job(self):
        print(add_job("my_task", "my_task", 2021, 5, 5, 1, 50, True, a=1, b=2))