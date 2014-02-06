
#===================================
#     Simulation parameters setup
#===================================
# set val(stop)   10.0                         ;# time of simulation end

#===================================
#        Initialization        
#===================================
#Create a ns simulator
set ns [new Simulator]

#Open the NS trace file
set tf [open out.tr w]
$ns trace-all $tf

#Open the NAM trace file
#set namfile [open out.nam w]
#$ns namtrace-all $namfile

#===================================
#        Nodes Definition        
#===================================
#Create 6 nodes
set n1 [$ns node]
set n2 [$ns node]
set n3 [$ns node]
set n4 [$ns node]
set n5 [$ns node]
set n6 [$ns node]

#===================================
#        Links Definition        
#===================================
#Createlinks between nodes
$ns duplex-link $n1 $n2 10Mb 10ms DropTail
#$ns queue-limit $n1 $n2 50
$ns duplex-link $n2 $n3 10Mb 10ms DropTail
#$ns queue-limit $n2 $n3 50
$ns duplex-link $n4 $n3 10Mb 10ms DropTail
#$ns queue-limit $n4 $n3 50
$ns duplex-link $n3 $n6 10Mb 10ms DropTail
#$ns queue-limit $n3 $n6 50
$ns duplex-link $n5 $n2 10Mb 10ms DropTail
#$ns queue-limit $n5 $n2 50

#Give node position (for NAM)
$ns duplex-link-op $n1 $n2 orient right-down
$ns duplex-link-op $n2 $n3 orient right
$ns duplex-link-op $n4 $n3 orient left-down
$ns duplex-link-op $n3 $n6 orient right-down
$ns duplex-link-op $n5 $n2 orient right-up

#===========Agents Defintion=============


#Setup a TCP connection
set tcp1 [new Agent/TCP/[lindex $argv 0]]
$ns attach-agent $n1 $tcp1
set sink1 [new Agent/TCPSink]
$ns attach-agent $n4 $sink1
$ns connect $tcp1 $sink1
$tcp1 set fid_ 1
$tcp1 set window_ 10000

#Setup a TCP connection
set tcp2 [new Agent/TCP/[lindex $argv 1]]
$ns attach-agent $n5 $tcp2
set sink2 [new Agent/TCPSink]
$ns attach-agent $n6 $sink2
$ns connect $tcp2 $sink2
$tcp2 set fid_ 2
$tcp2 set window_ 10000


#Setup a UDP connection
set udp [new Agent/UDP]
$ns attach-agent $n2 $udp
set udpsink [new Agent/Null]
$ns attach-agent $n3 $udpsink
$ns connect $udp $udpsink
$udp set fid_ 3


#=======Applications Definition=============        

#Setup a FTP Application over TCP connection
set ftp1 [new Application/FTP]
$ftp1 attach-agent $tcp1
$ftp1 set type_ FTP


#Setup a FTP Application over TCP connection
set ftp2 [new Application/FTP]
$ftp2 attach-agent $tcp2
$ftp2 set type_ FTP


#Setup a CBR over UDP connection
set cbr [new Application/Traffic/CBR]
$cbr attach-agent $udp
$cbr set type_ CBR
$cbr set packet_size_ 1000
$cbr set rate_ [lindex $argv 2]mb
$cbr set random_ false


#===================================
#        Termination        
#===================================
#Define a 'finish' procedure
proc finish {} {
    global ns tf
    $ns flush-trace
    close $tf
    #exec nam out.nam &
    exit 0
}
#$ns at $val(stop) "$ns nam-end-wireless $val(stop)"
#$ns at $val(stop) "finish"
#$ns at $val(stop) "puts \"done\" ; $ns halt"
#Schedule events for the CBR and FTP agents
$ns at 0.1 "$cbr start"
$ns at 0.5 "$ftp1 start"
$ns at 0.5 "$ftp2 start"
$ns at 100.0 "$ftp1 stop"
$ns at 100.0 "$ftp2 stop"
$ns at 100.5 "$cbr stop"

#Detach tcp and sink agents (not really necessary)
#$ns at 4.5 "$ns detach-agent $N1 $tcp ; $ns detach-agent $N4 $sink"

#Call the finish procedure after 5 seconds of simulation time

$ns at 100.0 "finish"

$ns run
