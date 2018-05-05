from threading import Thread


class ThreadManager:
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
    def _running_function(my_function, popup):
        my_function()
        popup.close()
