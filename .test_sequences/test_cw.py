from artiq import *
from artiq.language import *

class change_cw1(EnvExperiment):

    def build(self):
        self.setattr_device("core")
        self.setattr_device("scheduler")
        self.dds = self.get_device("866")
        self.cpld = self.get_device("urukul0_cpld")
        self.frequency = self.get_argument("frequency", NumberValue(80, unit="MHz"))
        self.amplitude = self.get_argument("amplitude", NumberValue(30, unit="dB"))
        self.state = self.get_argument("state", BooleanValue())

    @kernel
    def run(self):
        self.core.reset()
        self.cpld.init()
        self.dds.init()
        if self.state:
            self.dds.sw.on()
        else:
            self.dds.sw.off()
        self.dds.set(self.frequency)
        self.dds.set_att(self.amplitude)

    def analyze(self):
        print(self.frequency)
        print(self.frequency*MHz)
        print(self.amplitude)
        print(self.amplitude*dB)


