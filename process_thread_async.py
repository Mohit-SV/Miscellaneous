import requests
import time
from multiprocessing import Pool
from threading import Thread
import asyncio
import csv
import urllib
from itertools import islice
import numpy

cores = 4
threads_to_use = 20 # number of threads to be ran on each core
async_batch = 30
iteration_limit = 1500 # number of tasks to be given to the cores at once
file = r'***'

def divide_by_size(l, size):
    """returns splits the given list into chunks of given size"""
    def divide(l, size):
        for i in range(0, len(l), size):
            yield l[i:i + size]
    return list(divide(l, size))


def divide_by_number(l, number):
    """returns splits the given list into given number of chunks"""
    ll = numpy.array_split(numpy.array(l), number)
    lll = []
    for l in ll:
        lll.append(l.tolist())
    return lll


# function that sets up tasks in async
def responses_async(async_tasks):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    results = loop.run_until_complete(main_function(async_tasks, loop))
    print(results)
    return results


# main function ran for each async task
async def main_function(data_chunk, loop):
    results = []
    future = {}
    for inputs in data_chunk:
        # each api call
        url_encoded_text = urllib.parse.urlencode({'text': inputs[1]})
        url = """***{param1}***{param2}""".format(param1=int(inputs[0]), param2=url_encoded_text)
        future[inputs[0]] = loop.run_in_executor(None, requests.get, url)
        print("called: ", inputs[0])
    for inputs in data_chunk:
        response = await future[inputs[0]]
        f = open('tests_log.txt', 'a')
        f.write(response)
        f.close()
        results[inputs[0]] = response
    return results


def thread_run(data_to_the_core):
    """run tasks in multiple threads"""

    thread_tasks_list = divide_by_number(data_to_the_core, threads_to_use) # list of lists of tasks to each thread

    def run_each_thread(thread_tasks_list, thread_results, index):
        """run tasks in async"""
        for async_tasks in divide_by_size(thread_tasks_list, async_batch):
            try:
                thread_results[index] = responses_async(async_tasks)
            except:
                didnt_run[index] = thread_tasks_list
            time.sleep(1)

    threads = [None] * threads_to_use
    thread_results = [None] * threads_to_use
    didnt_run = [None] * threads_to_use

    for i in range(threads_to_use):
        threads[i] = Thread(target=run_each_thread, args=(thread_tasks_list[i], thread_results, i))
        threads[i].start()

    for i in range(threads_to_use):
        threads[i].join()
    
    print(didnt_run) # prints tasks that have failed run on threads
    
    return thread_results


if __name__ == '__main__':
    start_time = time.time()

    with open(file, mode='r', encoding='ISO-8859-1') as infile:
        reader = csv.reader(infile) # file containing inputs (2 columns) of api calls (multiple rows)
        primary_data = []
        for rows in reader:
            primary_data.append([rows[0], rows[1]])
        del primary_data[0] # if there is any header
        print("Total number of api calls: ", len(primary_data))
        
        # run pool of tasks
        
        for iteration_data in divide_by_size(primary_data, iteration_limit):
            core_tasks_list = divide_by_number(iteration_data, cores) # list of lists of tasks to each core
            pool = Pool(processes=cores)
            compiled_responses = pool.map(thread_run, core_tasks_list) 
            pool.close()    
            pool.join()

        print(compiled_responses)

    end_time = time.time()
    print("Process Time: ", end_time - start_time)
