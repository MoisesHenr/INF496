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
    @display("bgb=900,600");
    submodules:
        configurator: Ipv4NetworkConfigurator {
            @display("p=50,50");
        }
        radioMedium: Ieee80211ScalarRadioMedium {
            @display("p=50,150");
        }
        visualizer: IntegratedVisualizer {
            @display("p=50,250");
        }
        host1: WirelessHost {
            @display("p=450,50");
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
                @display("p=450,200;r=,,#707070");
            gates:
                ethg[1];
        }
        AP2: AccessPoint {
            parameters:
                @display("p=625,400;r=,,#707070");
            gates:
                ethg[1];
        }
        AP1: AccessPoint {
            parameters:
                @display("p=275,400;r=,,#707070");
            gates:
                ethg[1];
        }
        etherSwitch: EtherSwitch {
            parameters:
                @display("p=450,400");
            gates:
                ethg[6];
        }
        standardHost: StandardHost {
            parameters:
                @display("p=450,500");
            gates:
                ethg[1];
        }
        AP4: AccessPoint {
            parameters:
                @display("p=100,200;r=,,#707070");
            gates:
                ethg[1];
        }
        AP5: AccessPoint {
            parameters:
                @display("p=800,200;r=,,#707070");
            gates:
                ethg[1];
        }
    connections:
        etherSwitch.ethg[0] <--> Eth100M <--> AP3.ethg[0];
        etherSwitch.ethg[1] <--> Eth100M <--> AP1.ethg[0];
        etherSwitch.ethg[2] <--> Eth100M <--> AP2.ethg[0];
        etherSwitch.ethg[3] <--> Eth100M <--> AP4.ethg[0];
        etherSwitch.ethg[4] <--> Eth100M <--> AP5.ethg[0];
        standardHost.ethg[0] <--> Eth100M <--> etherSwitch.ethg[5];
}