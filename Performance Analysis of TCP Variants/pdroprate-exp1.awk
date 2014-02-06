BEGIN {
        recvdSize = 0
        startTime = 2
        stopTime = 0
		p_total = 0
		p_drop = 0
		total_latency = 0
   }
    
   {
              event = $1
              time = $2
              node_id = $3
              pkt_size = $6
			  flow_id = $8
              level = $4
			  p_id = $12
			  
				if (event == "d" && flow_id == "1")
				{
					p_drop += 1
				}
			  
   if (event == "+" && node_id == 0) {
     p_total += 1
        }
    
   }
    
   END {
		printf("\nPacket drop rate = %f\t\t",p_drop/p_total)
   }
