import time
import inspect

def troubleshoot(function):
    def wrapper(*args, **kwargs):
        print('called: {}.{}'.format(function.__module__,function.__name__))
        arguments = inspect.signature(function).bind(*args, **kwargs).arguments
        arguments = ', '.join('{} = {!r}'.format(*item) for item in arguments.items())
        start = time.time()
        result = function(*args, **kwargs)
        end = time.time()
        try:
            print('arguments: {}'.format(arguments))
            print('results: {}'.format(result))
        except:
            print('something not printable')
        print('finished in {} secs'.format(round(end - start, 4)))
        return result
    return wrapper
