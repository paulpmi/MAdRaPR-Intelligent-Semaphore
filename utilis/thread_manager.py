import traceback
from threading import Thread

import sys


class ThreadManager:
    @staticmethod
    def run_thread_with_button(my_function, args, btn):
        thread = Thread(target=ThreadManager._button_function, args=[my_function, args, btn])
        thread.start()

    @staticmethod
    def run_thread_with_popup(my_function, popup):
        thread = Thread(target=ThreadManager._running_function, args=[my_function, popup])
        thread.start()

    @staticmethod
    def run_thread_with_popup_and_args(my_function, popup, location, logic):
        thread = Thread(target=ThreadManager._run_alg, args=[my_function, popup, location, logic])
        thread.start()

    @staticmethod
    def _run_alg(my_function, popup, location, logic):
        my_function(location, logic)
        popup.close()

    @staticmethod
    def _button_function(my_func, args, btn):
        try:
            my_func(args)
        except:
            print "Exception in user code:"
            print '-' * 60
            traceback.print_exc(file=sys.stdout)
            print '-' * 60
        btn.disabled = False

    @staticmethod
    def _running_function(my_function, popup):
        try:
            my_function()
        except:
            print "Exception in user code:"
            print '-' * 60
            traceback.print_exc(file=sys.stdout)
            print '-' * 60
        popup.close()
