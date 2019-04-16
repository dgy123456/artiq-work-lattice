import labrad
from threading import Thread
from artiq import *
from artiq.language import *
from artiq.language.core import TerminationRequested

class pmt_collect_pulsed(EnvExperiment):

    def build(self):
        cxn = labrad.connect()
        p = cxn.parametervault
        self.duration = p.get_parameter(["PmtReadout", "duration"])["ms"]
        self.setattr_device("core")
        self.setattr_device("scheduler")
        self.pmt = self.get_device("pmt")
        self.cpld = self.get_device("urukul0_cpld")
        self.dds_866 = self.get_device("866")
        # self.dds_397 = self.get_device("397")

    def run(self):
        self.core.reset()
        self.set_dataset("pmt_counts", [], broadcast=True)
        self.set_dataset("collection_duration", [self.duration])
        self.set_dataset("pmt_counts_866_off", [], broadcast=True)
        self.set_dataset("diff_counts", [], broadcast=True)
        self.set_dataset("pulsed", [True], broadcast=True)
        while True:
            try:
                self.run_pmt()
                self.core.comm.close()
                self.scheduler.pause()
                self.core.comm.open()
            except TerminationRequested:
                break

    @kernel
    def run_pmt(self):
        self.core.break_realtime()
        self.cpld.init()
        self.dds_866.init()
        # self.dds_397.init()
        # self.dds_866.set(80*MHz)
        # self.dds_397.set(75*MHz)
        # self.dds_866.set_att(22*dB)
        # self.dds_397.set_att(22*dB)
        self.dds_866.sw.on()
        # self.dds_397.sw.on()
        while not self.scheduler.check_pause():
            self.core.break_realtime()
            t_count = self.pmt.gate_rising(self.duration*ms)
            pmt_counts = self.pmt.count(t_count)
            self.core.break_realtime()
            self.dds_866.sw.off()
            self.record_data("pmt_counts", pmt_counts)
            t_count = self.pmt.gate_rising(self.duration*ms)
            self.dds_866.sw.on()
            pmt_counts_866_off = self.pmt.count(t_count)
            t1 = Thread(target=self.record_data, 
                        args=("pmt_counts_866_off", pmt_counts_866_off))
            t2 = Thread(target=self.record_data, 
                        args=("diff_counts", pmt_counts - pmt_counts_866_off))
            t1.start()
            t2.start()
            # self.record_data("pmt_counts_866_off", pmt_counts_866_off)
            # self.record_data("diff_counts", pmt_counts - pmt_counts_866_off)

    @rpc(flags={"async"})
    def record_data(self, dataset, x):
        self.append_to_dataset(dataset, x)