BEGIN {
fromNode=2; toNode=3;
lineCount = 0;totalBits = 0;
}
/^r/&&$3==fromNode&&$4==toNode {
    totalBits += 8*$6;
	level = $4
	time = $2
	if(lineCount == 0) {
	startTime = 0; lineCount++;
	}
	timeEnd = time;
};
END{
duration = timeEnd-startTime;
if (duration == 0) {}
else {
print "\nThoughput = "  totalBits/duration/1e3 " kbps."; 
};
};