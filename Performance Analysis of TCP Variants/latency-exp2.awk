BEGIN {
	ind1 = 0
	ind2 = 0
	total_latency = 0
	highest_pid = 0
}
    
{
	event = $1
	time = $2
	node_id = $3
	pkt_size = $6
	level = $4
	flow_id = $8
	p_id = $11
	
	if (event == "r" && level == "0")
	{
		total_latency1 += time - p_stime1[p_id]
		ind1++
	}
	# Store start time
	if (event == "+" && node_id == "0") {
		p_stime1[p_id] = time
		
	}
		
	if (event == "r" && level == "4")
	{
		total_latency2 += time - p_stime2[p_id]
		ind2++
	}
	# Store start time
	if (event == "+" && node_id == "4") {
		p_stime2[p_id] = time
		
	}
	if(p_id > highest_pid)
		highest_pid = p_id
}
    
END {

	printf("\nAverage Latency1[kbps] = %f\t\t",total_latency1/ind1)
	printf("\nAverage Latency2[kbps] = %f\t\t",total_latency2/ind2)
}
