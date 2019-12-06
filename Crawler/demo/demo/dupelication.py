
class RepeatFilter(object):
    def __init__(self):
        self.visited_fd = set()

    @classmethod
    def from_settings(cls, settings):
        print("....")
        return cls()

    def request_seen(self, request):
        if request.url in self.visited_fd:
            return True
        self.visited_fd.add(request.url)
        return False

    def open(self):  # can return deferred
        print('开始')


    def close(self, reason):  # can return a deferred
        print('结束')


    def log(self, request, spider):  # log that a request has been filtered
        pass