from artiq.experiment import *
from pulse_sequence import get_729_dds


class SidebandCooling():
    line_selection="SidebandCooling.line_selection"
    selection_sideband="SidebandCooling.selection_sideband"
    order="SidebandCooling.order"
    stark_shift="SidebandCooling.order"
    channel_729="StatePreparation.channel_729"
    repump_additional="OpticalPumpingContinuous.optical_pumping_continuous_duration"
    amplitude_729="SidebandCooling.amplitude_729"
    att_729="SidebandCooling.att_729"
    duration="SidebandCoolingContinuous.sideband_cooling_continuous_duration"
    freq_729=220*MHz

    sequential_enable="SequentialSBCooling.enable"
    sequential_channel_729="SequentialSBCooling.channel_729"

    sequential1_enable="SequentialSBCooling1.enable"
    sequentia1l_channel_729="SequentialSBCooling1.channel_729"

    sequential2_enable="SequentialSBCooling2.enable"
    sequential2_channel_729="SequentialSBCooling2.channel_729"

    def subsequence(self):
        get_729_dds(self, SidebandCooling.channel_729)

        freq_729 = SidebandCooling.freq_729 + SidebandCooling.stark_shift
        self.dds_729.set(freq_729, amplitude=SidebandCooling.amplitude_729)
        self.dds_729.set_att(SidebandCooling.att_729)
        
        self.krun()
        
        if SidebandCooling.sequential_enable:
            get_729_dds(self, SidebandCooling.sequentia1_channel_729)
            self.krun()

        if SidebandCooling.sequential1_enable:
            get_729_dds(self, SidebandCooling.sequentia1l_channel_729)
            self.krun()

        if SidebandCooling.sequential2_enable:
            get_729_dds(self, SidebandCooling.sequentia12_channel_729)
            self.krun()
        
        
        
        delay(SidebandCooling.repump_additional)
        self.dds_854.sw.off()
        delay(SidebandCooling.repump_additional)
        self.dds_866.sw.off()

    @kernel
    def krun(self):
        with parallel:
            self.dds_729.sw.on()
            self.dds_729_SP.sw.on()
            self.dds_854.sw.on()
            self.dds_866.sw.on()
        delay(SidebandCooling.duration)
        with parallel:
            self.dds_729.sw.off()
            self.dds_729_SP.sw.off()
