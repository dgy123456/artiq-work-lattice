from artiq import *
from artiq.language import *

class test_line_trigger(EnvExperiment):

    def build(self):
        self.setattr_device("core")
        self.setattr_device("LTriggerIN")

    def prepare(self):
        self.set_dataset("pmt_counts", [], broadcast=True)

    @kernel
    def run(self):
        while True:
            if self.LTriggerIN.watch_stay_on():
                self.LTriggerIN.watch_done()
            self.append_to_dataset("pmt_counts", 1)
            #self.LTriggerIN.watch_done()
