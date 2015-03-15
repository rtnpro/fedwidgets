import fedmsg
from collection import defaultdict
import json


# Dispatcher
class Dispatcher(object):

    def __init__(self):
        self._observers = defaultdict(list)

    def run(self):
        for name, endpoint, topic, msg in fedmsg.tail_messages():
            for observer in self._observers.get(topic, []):
                observer(name, endpoint, topic, msg)

    def attach_observer(self, topic, observer):
        if observer not in self._observers.get(topic, []):
            self._observers[topic].append(observer)

dispatcher = Dispatcher()


# Base Widget
class BaseWidget(object):
    LISTENER = ""

    def _observe(self, name, endpoint, topic, msg):
        self.update(name, endpoint, topic, msg)

    def update(self, name, endpoint, topic, msg):
        """
        Invoked from the observer to save data.
        """
        data = self.clean(name, endpoint, topic, msg)
        self.save(data)
        self.post_save(name, endpoint, topic, msg, data)

    def get(self, id=None, params={}):
        """
        Called from a generic view to handle widget endpoints.

        Returns a JSON.
        """
        raise NotImplementedError

    def clean(self, name, endpoint, topic, msg):
        """
        Clean raw data and generate data to be saved.
        """
        return msg

    def save(self, data):
        """
        Save data to datastore.
        """
        raise NotImplementedError

    def post_save(self, name, endpoint, topic, msg, data):
        """Run post save hooks."""
        return


# Test Widget
class TestWidget(BaseWidget):
    LISTENER = "testing"

    def get(self, *args, **kwargs):
        return json.dumps({})

    def save(self, data):
        # Code to save data to db
        pass

test_widget = TestWidget()


def initialize_widgets():
    # This code will crawl through widgets dir and initialize
    # all the widgets
    widgets = [test_widget] # get_all_widgets()
    for widget in widgets:
        dispatcher.attach_observer(widget.LISTENER, widget._observe)

initialize_widgets()
dispatcher.run()
