#Create a simulator object
set ns [new Simulator]

#Open the NAM trace file

set tcpf [open tcp.txt w]
set udpf [open udp.txt w]
set tcl_precision 4

#Define a 'finish' procedure
proc finish {} {
        global tcpf udpf
        #$ns flush-trace
        #Close the NAM trace file
        close $tcpf
		close $udpf
        #Execute NAM on the trace file
        #exec nam out.tr &
        exit 0
}

proc getinterval {} {
        global sink0 udpsink tcpf udpf
        #Get an instance of the simulator
        set ns [Simulator instance]
        #Set the time after which the procedure should be called again
        set time 5
        #How many bytes have been received by the traffic sinks?
        set bw0 [$sink0 set bytes_]
        set bw1 [$udpsink set bytes_]
        #Get the current time
        set now [$ns now]
        #Calculate the bandwidth (in MBit/s) and write it to the files
        puts $tcpf "$now [expr $bw0/$time*8/1000]"
        puts $udpf "$now [expr $bw1/$time*8/1000]"
        #Reset the bytes_ values on the traffic sinks
        $sink0 set bytes_ 0
        $udpsink set bytes_ 0
        #Re-schedule the procedure
        $ns at [expr $now+$time] "getinterval"
}

set N1 [$ns node]
set N2 [$ns node]
set N3 [$ns node]
set N4 [$ns node]
set N5 [$ns node]
set N6 [$ns node]

$ns duplex-link $N1 $N2 10Mb 10ms [lindex $argv 1]
$ns duplex-link $N5 $N2 10Mb 10ms [lindex $argv 1]
$ns duplex-link $N2 $N3 10Mb 10ms [lindex $argv 1]
$ns duplex-link $N3 $N4 10Mb 10ms [lindex $argv 1]
$ns duplex-link $N3 $N6 10Mb 10ms [lindex $argv 1]

#Node position (for NAM)
$ns duplex-link-op $N5 $N2 orient right-up
$ns duplex-link-op $N1 $N2 orient right-down
$ns duplex-link-op $N2 $N3 orient right
$ns duplex-link-op $N3 $N4 orient right-up
$ns duplex-link-op $N3 $N6 orient right-down

#set type [lindex $argv 0]
#set tahoe "Tahoe"
#Setup a TCP connection
if {[lindex $argv 0] == "Tahoe"} {
set tcp [new Agent/TCP]
} else {
set tcp [new Agent/TCP/[lindex $argv 0]]
}
$tcp set class_ 1
$ns attach-agent $N1 $tcp
if {[lindex $argv 0] == "Sack1"} {
set sink0 [new Agent/TCPSink/Sack1]
} else {
set sink0 [new Agent/TCPSink]
}
$ns attach-agent $N4 $sink0
$ns connect $tcp $sink0
$tcp set fid_ 1
$tcp set window_ 10000

#Setup a FTP over TCP connection
set ftp [new Application/FTP]
$ftp attach-agent $tcp
$ftp set type_ FTP


#Setup a UDP connection
set udp [new Agent/UDP]
$ns attach-agent $N5 $udp
set udpsink [new Agent/LossMonitor]
$ns attach-agent $N6 $udpsink
$ns connect $udp $udpsink
$udp set fid_ 2

#Setup a CBR over UDP connection
set cbr [new Application/Traffic/CBR]
$cbr attach-agent $udp
$cbr set type_ CBR
$cbr set packet_size_ 1000
$cbr set rate_ 6mb
$cbr set random_ false

#Schedule events for the CBR and FTP agents
$ns at 0.1 "$ftp start"
$ns at 40.0 "$cbr start"
$ns at 100.0 "$ftp stop"
$ns at 100.5 "$cbr stop"

#Detach tcp and sink agents (not really necessary)
#$ns at 4.5 "$ns detach-agent $N1 $tcp ; $ns detach-agent $N4 $sink"

#Call the finish procedure after 5 seconds of simulation time
$ns at 0 "getinterval"
$ns at 100.0 "finish"

#Print CBR packet size and interval
#puts "CBR packet size = [$cbr set packet_size_]"
#puts "CBR interval = [$cbr set interval_]"

#Run the simulation
$ns run