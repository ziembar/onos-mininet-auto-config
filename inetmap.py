from mininet.topo import Topo
from mininet.node import OVSKernelSwitch
import mininet


class Project( Topo ):
    def __init__( self ):
        # Initialize topology
        Topo.__init__( self )
        # Add hosts
        h1 = self.addHost('Londyn')
        h2 = self.addHost('Paryz')
        h3 = self.addHost('Madryt')
        h4 = self.addHost('Zurych')
        h5 = self.addHost('Rzym')
        h6 = self.addHost('Zagrzeb')
        h7 = self.addHost('Ateny')
        h8 = self.addHost('Berlin')
        h9 = self.addHost('Praga')
        h10 = self.addHost('Warszawa')

        s1 = self.addSwitch('s1')
        s2 = self.addSwitch('s2')
        s3 = self.addSwitch('s3')
        s4 = self.addSwitch('s4')
        s5 = self.addSwitch('s5')
        s6 = self.addSwitch('s6')
        s7 = self.addSwitch('s7')
        s8 = self.addSwitch('s8')
        s9 = self.addSwitch('s9')
        s10 = self.addSwitch('s10')

        self.addLink(h1,s1)
        self.addLink(h2,s2)
        self.addLink(h3,s3)
        self.addLink(h4,s4)
        self.addLink(h5,s5)
        self.addLink(h6,s6)
        self.addLink(h7,s7)
        self.addLink(h8,s8)
        self.addLink(h9,s9)
        self.addLink(h10,s10)

        self.addLink(s1,s2,delay='2ms', bw=80)
        self.addLink(s3,s2,delay='7ms', bw=80)
        self.addLink(s4,s2,delay='3ms', bw=80)
        self.addLink(s8,s2,delay='6ms', bw=80)
        self.addLink(s4,s5,delay='5ms', bw=20)
        self.addLink(s4,s6,delay='4ms', bw=80)
        self.addLink(s6,s7,delay='8ms', bw=10)
        self.addLink(s8,s9,delay='2ms', bw=80)
        self.addLink(s8,s10,delay='4ms', bw=80)


#       cyclic links also
        self.addLink(s4,s9,delay='3ms', bw=80)
        self.addLink(s9,s10,delay='4ms', bw=80)
        self.addLink(s6,s9,delay='3ms', bw=80)
        self.addLink(s3,s4,delay='9ms', bw=80)
        self.addLink(s5,s7,delay='8ms', bw=80)
        self.addLink(s3,s5,delay='9ms', bw=80)



topos = { 'inetmap': ( lambda: Project() )}