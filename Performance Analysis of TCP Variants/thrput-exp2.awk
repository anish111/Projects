BEGIN {
fromNode=2; toNode1=3; toNode2=5;
lineCount = 0;totalBits = 0;
startTime1 = 100
startTime2 = 100
totalBits1 = 0
totalBits2 = 0
count1 = 0
count2 = 0
timeEnd1 = 0
timeEnd2 = 0
}
/^r/&&$3==fromNode&&($4==toNode1||$4==toNode2) {
	
	level = $4
	time = $2
	flow_id = $8
	if (flow_id == 1)
		totalBits1 += 8*$6;
	if (flow_id == 2)
		totalBits2 += 8*$6;
		
	 if (flow_id == 1 && count1 == 0) {
			startTime1 = time
			count1++
        }
	if (flow_id == 1)
			timeEnd1 = time
	
	totalBits += 8*$6;
	
	
	 if (flow_id == 2 && count2 == 0) {
		startTime2 = time
		count2++
        }
	
	if (flow_id == 2)
		timeEnd2 = time
	
};

END{

duration1 = timeEnd1-startTime1;
duration2 = timeEnd2-startTime2;
if (duration1 == 0) {
print "\nThroughput1 = " totalBits1 " kbps.";
}
if (duration2 == 0) {
print "\nThroughput2 = " totalBits2 " kbps.";
}
else {
print "\nThoughput1 = "  totalBits1/duration1/1e3 " kbps."; 
print "\nThoughput2 = "  totalBits2/duration2/1e3 " kbps."; 
};
};
