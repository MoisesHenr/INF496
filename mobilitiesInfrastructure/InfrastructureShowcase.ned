package inet.showcases.wireless.mobilitiesInfrastructure;

import inet.networklayer.configurator.ipv4.Ipv4NetworkConfigurator;
import inet.node.ethernet.Eth100M;
import inet.node.ethernet.EtherSwitch;
import inet.node.inet.StandardHost;
import inet.node.inet.WirelessHost;
import inet.node.wireless.AccessPoint;
import inet.physicallayer.ieee80211.packetlevel.Ieee80211ScalarRadioMedium;
import inet.visualizer.integrated.IntegratedVisualizer;


network InfrastructureShowcaseBase
{
    @display("bgb=640,420");
    submodules:
        configurator: Ipv4NetworkConfigurator {
            @display("p=52,45");
        }
        radioMedium: Ieee80211ScalarRadioMedium {
            @display("p=51,112");
        }
        visualizer: IntegratedVisualizer {
            @display("p=52,164");
        }
        host1: WirelessHost {
            @display("");
        }
}

network InfrastructureShowcaseA extends InfrastructureShowcaseBase
{
    parameters:
        @figure[title](type=label; text="Infrastructure mode"; pos=525,25; anchor=sw; color=darkblue);
    types:
        channel Unnamed
        {
        }

    submodules:
        AP3: AccessPoint {
            parameters:
                @display("p=300,100;r=,,#707070");
            gates:
                ethg[1];
        }
        AP2: AccessPoint {
            parameters:
                @display("p=500,300;r=,,#707070");
            gates:
                ethg[1];
        }
        AP1: AccessPoint {
            parameters:
                @display("p=100,300;r=,,#707070");
            gates:
                ethg[1];
        }
        etherSwitch: EtherSwitch {
            parameters:
                @display("p=298,242");
            gates:
                ethg[4];
        }
        standardHost: StandardHost {
            parameters:
                @display("p=616,23");
            gates:
                ethg[1];
        }
    connections:
        etherSwitch.ethg[0] <--> Eth100M <--> AP3.ethg[0];
        etherSwitch.ethg[1] <--> Eth100M <--> AP1.ethg[0];
        etherSwitch.ethg[2] <--> Eth100M <--> AP2.ethg[0];
        standardHost.ethg[0] <--> Eth100M <--> etherSwitch.ethg[3];
}
