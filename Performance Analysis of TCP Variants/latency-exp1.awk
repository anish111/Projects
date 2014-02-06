BEGIN {
	recvdSize = 0
	startTime = 2
	stopTime = 0
	ind = 0
	total_latency = 0
	highest_pid = 0
}
    
{
	event = $1
	time = $2
	node_id = $3
	pkt_size = $6
	level = $4
	p_id = $11
	if (event == "r" && level == 0)
	{
		ind++
		total_latency += time - p_stime[p_id]
	}
	# Store start time
	if (event == "+" && node_id == 0) {
		p_stime[p_id] = time

	}

}
    
END {
	printf("\nAverage Latency[kbps] = %f\t\t",total_latency/ind)
}
