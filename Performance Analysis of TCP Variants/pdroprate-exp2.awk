BEGIN {
        recvdSize1 = 0
		p_total1 = 1
		p_drop1 = 0
		recvdSize2 = 0
		p_total2 = 1
		p_drop2 = 0
   }
    
{
event = $1
time = $2
node_id = $3
pkt_size = $6
flow_id = $8
level = $4
p_id = $12

if (event == "d" && flow_id == "1") {
p_drop1 += 1
}

if (event == "d" && flow_id == "2") {
p_drop2 += 1
}

if (event == "+" && node_id == "0") {
p_total1 += 1
}

if (event == "+" && node_id == "4") {
p_total2 += 1
}
}
    
END {

	printf("\nPacket drop rate 1 = %f\t\t",p_drop1/p_total1)
	printf("\nPacket drop rate 2 = %f\t\t",p_drop2/p_total2)
}
