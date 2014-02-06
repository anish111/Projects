'''
    Making raw sockets over ethernet, tcp and ip. Feeling awesome! :)
       
'''
# importing required packages
import socket, sys
import urlparse
from struct import *
import random
import time
import subprocess
import fcntl
import struct
from parse import parse
from uuid import getnode as get_mac_address

global gatewaymac
global ethernet_header
global filenameurl

f = subprocess.Popen(["route","-n"],stdout=subprocess.PIPE)

trace = f.communicate()#.split('\n')
lines = trace[0].split('\n')

count = len(lines)

def getHwAddr(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    info = fcntl.ioctl(s.fileno(), 0x8927,  struct.pack('256s', ifname[:15]))
    return ''.join(['%02x:' % ord(char) for char in info[18:24]])[:-1]
 
for x in range(0, count):
  if "UG" in lines[x]:
    gatewayip = (' '.join(lines[x].split())).split(' ')[1]
    macline = subprocess.Popen(["arp",str(gatewayip)],stdout=subprocess.PIPE).communicate()[0].split('\n')[1]
    gatewaymac = (' '.join(macline.split())).split(' ')[2]
    prototype = 2048
    mymac = getHwAddr("eth0")
    ethernet_header = pack('!6s6sH',gatewaymac.replace(':', '').decode('hex'), mymac.replace(':', '').decode('hex'), prototype)



def getNetworkIp():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('8.8.8.8', 0))
    return s.getsockname()[0] 

filenameurl = sys.argv[1]
url = urlparse.urlparse(str(sys.argv[1]))
host = str(url.netloc) 
path = str(url.path)
 
if not path:
 path = '/'
 filenameurl += path
pl_sequence = 0
pl_acl = 0
data = ''
data_length = 0
recv_flag = 0
source_ip = getNetworkIp()
dest_ip =  socket.gethostbyname(host)  #'129.10.113.83' # or socket.gethostbyname
tcp_source = random.randrange(1025,65535)   # source port
acknowledgement = 0
sequence = 0
d_addr = getNetworkIp()
dest_port = 0
collectdata = ''
contentlength = 0
initseq = 0

def checksum(data):
  pos = len(data)
  if (pos & 1):  # checking for odd data length
    pos -= 1
    sum = ord(data[pos])  # this is used to create a proper sum.
  else:
    sum = 0
 
  # This calculates the actual checksum.
  while pos > 0:
    pos -= 2
    sum += (ord(data[pos + 1]) << 8) + ord(data[pos])
 
  sum = (sum >> 16) + (sum & 0xffff)
  sum += (sum >> 16)
 
  result = (~ sum) & 0xffff #Keeping the lower 16 bits
  return result

 
#create a raw socket

try:
    s = socket.socket(socket.AF_PACKET, socket.SOCK_RAW)
    s.bind(('eth0',0))
except socket.error , msg:
    print 'Socket could not be created. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
    sys.exit()
 

# starting to  construct the packet
packet = ''
hostname = ''
if len(sys.argv[1]) > 0:
  hostname = sys.argv[1]
else:
  print 'No host name given'
  sys.exit()
    
def write_data(collectdata,location):
  f = open(location,'a')
  f.write(collectdata)
  f.close()

def send_pack(flags,seq,ack,data):
  # ip header field
  ip_ihl = 5
  ip_ver = 4
  ip_tos = 0
  ip_tot_len = 0  
  ip_id = 54321   
  ip_frag_off = 0
  ip_ttl = 255
  ip_proto = socket.IPPROTO_TCP
  ip_check = 0 
  ip_saddr = socket.inet_aton ( source_ip ) 
  ip_daddr = socket.inet_aton ( dest_ip )
  
  ip_ihl_ver = (ip_ver << 4) + ip_ihl
  
  
  ip_header = pack('!BBHHHBBH4s4s' , ip_ihl_ver, ip_tos, ip_tot_len, ip_id, ip_frag_off, ip_ttl, ip_proto, ip_check, ip_saddr, ip_daddr)

  #fields of tcp headers
  tcp_dest = 80   # destination port
  tcp_seq = seq
  tcp_ack_seq = ack
  tcp_doff = 5   
  #tcp flags
  if flags == 1:		#syn packet
    tcp_syn = 1
    tcp_ack = 0
    tcp_psh = 0
    tcp_fin = 0
  elif flags == 2:		#ack packet
    tcp_syn = 0
    tcp_ack = 1
    tcp_psh = 0
    tcp_fin = 0
  elif flags == 3:		#data packet
    tcp_syn = 0
    tcp_ack = 1
    tcp_psh = 1
    tcp_fin = 0
  elif flags == 4:		#fin packet
    tcp_syn = 0
    tcp_ack = 1
    tcp_psh = 0
    tcp_fin = 1
  tcp_rst = 0
  tcp_urg = 0
  tcp_window = socket.htons (1000)    #   maximum allowed window size
  tcp_check = 0
  tcp_urg_ptr = 0
  
  tcp_offset_res = (tcp_doff << 4) + 0
  tcp_flags = tcp_fin + (tcp_syn << 1) + (tcp_rst << 2) + (tcp_psh <<3) + (tcp_ack << 4) + (tcp_urg << 5)
  tcp_header = pack('!HHLLBBHHH' , tcp_source, tcp_dest, tcp_seq, tcp_ack_seq, tcp_offset_res,        tcp_flags,  tcp_window, tcp_check, tcp_urg_ptr)
  
  user_data = data 
  global pl_ack

  
  pl_ack = tcp_ack_seq
  
  source_address = socket.inet_aton( source_ip )
  dest_address = socket.inet_aton(dest_ip)
  placeholder = 0
  protocol = socket.IPPROTO_TCP
  tcp_length = len(tcp_header) + len(user_data)
  
  psh = pack('!4s4sBBH' , source_address , dest_address , placeholder , protocol , tcp_length);
  psh = psh + tcp_header + user_data;
  
  tcp_check = checksum(psh)
  
  #making the tcp header again with new checksum
  tcp_header = pack('!HHLLBBH' , tcp_source, tcp_dest, tcp_seq, tcp_ack_seq, tcp_offset_res, tcp_flags,  tcp_window) + pack('H' , tcp_check) + pack('!H' , tcp_urg_ptr)
  
  
  ip_tot_len = 20  + len(tcp_header) + len(user_data)
  ip_header = pack('!BBHHHBBH4s4s' , ip_ihl_ver, ip_tos, ip_tot_len, ip_id, ip_frag_off, ip_ttl, ip_proto, ip_check, ip_saddr, ip_daddr)
  ip_check = socket.htons(checksum(ip_header))
  ip_header = pack('!BBHHHBBH4s4s' , ip_ihl_ver, ip_tos, ip_tot_len, ip_id, ip_frag_off, ip_ttl, ip_proto, ip_check, ip_saddr, ip_daddr)
  
  packet = ethernet_header + ip_header + tcp_header + user_data
  s.send(packet)
  
global collectdata
global remembered_data
global flag
global tcp_map
global tcp_data
global contentlength
f1 = 0
initial_seq_no = 754

send_pack(1,initial_seq_no,0,'')

start_syn = time.clock()

sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
recvdata = ''
def recv(msg):
  global contentlength
  global collectdata
  global pl_sequence
  global acknowledgement
  global sequence
  global data
  global data_length
  global recv_flag
  global source_ip
  global tcp_source
  global d_addr
  global dest_port
  global intiseq

  while True:
    packet = sock.recvfrom(65536)   
    packet = packet[0]    
    ip_header = packet[0:20]    
    iph = unpack('!BBHHHBBH4s4s' , ip_header)    
    version_ihl = iph[0]
    version = version_ihl >> 4
    ihl = version_ihl & 0xF   
    iph_length = ihl * 4   
    ttl = iph[5]
    protocol = iph[6]
    s_addr = socket.inet_ntoa(iph[8]);
    d_addr = socket.inet_ntoa(iph[9]);
    tcp_header = packet[iph_length:iph_length+20]    
    
    #unpacking the data
    tcph = unpack('!HHLLBBHHH' , tcp_header)   
    source_port = tcph[0]
    dest_port = tcph[1]
    sequence = tcph[2]
    acknowledgement = tcph[3]
    doff_reserved = tcph[4]
    recv_flag = tcph[5]
    tcph_length = doff_reserved >> 4
    h_size = iph_length + tcph_length * 4
    data_size = len(packet) - h_size
    data_length = len(packet) - len(tcp_header) - len(ip_header)
    
    data = packet[h_size:]
    tcp_check_in = socket.ntohs(tcph[7])

    ## Incoming packet checksum
    
    ip_saddr = iph[8]   
    ip_daddr = iph[9]
    if d_addr == source_ip and tcp_source == dest_port: 
     
     if pl_sequence == sequence:  
     	tcp_rst = 0
     	tcp_urg = 0
     	tcp_window = tcph[6]
     	tcp_check = 0
     	tcp_urg_ptr = 0
   	tcp_header_in = pack('!HHLLBBHHH' , source_port, dest_port, sequence, acknowledgement, doff_reserved, recv_flag,  tcp_window, tcp_check,  tcp_urg_ptr)
 	placeholder = 0
        protocol = socket.IPPROTO_TCP
     	tcp_length = len(tcp_header_in) + len(data)
  
        psh = pack('!4s4sBBH' , ip_saddr , ip_daddr , placeholder , protocol , tcp_length);
        psh = psh + tcp_header_in + data;
  
        tcp_check_incoming = checksum(psh) 
        
        checksum_diff = int(tcp_check_incoming) - int(tcp_check_in)
        
        if checksum_diff != 0:
           send_pack(2,acknowledgement,sequence,'')
           continue
    break;
    

def checkqueue(seq):
    if seq in tcp_map.keys():
	while len(tcp_map[seq]) > 0:
	    temp = tcp_map[seq]
	    
	    send_pack(2,acknowledgement,seq+len(temp),'')
	    seq = seq + len(temp)
	  
    return seq

def writemap():
	
	myseq = initseq
        f = 0
        filename = filenameurl[(filenameurl.rfind("/")+1): ]
        if filename == '':
           filename = 'index.html'
        print filename
 	while myseq in tcp_map:
	    temp = tcp_map[myseq] 
	    myseq = myseq + len(temp)
            if f == 0:
             data1,data2 = temp.split('\r\n\r\n')
             temp = data2
             f = 1           
            write_data(temp,filename)

# Tear down when a fin or fin psh ack is received.    
    
def teardownonfin(datalength):
  global sequence
  #"teardown on fin"
  send_pack (2,acknowledgement,sequence+datalength,'')
  send_pack (4,acknowledgement,sequence+datalength,'')
  pl_sequence = sequence + datalength
  writemap()
  recv('')
  
  while not (sequence == pl_sequence and recv_flag == 16):
    recv('')
  
  sys.exit()

def teardownonack(data_len):
  #"teardown on ack"
  writemap()
  send_pack (4,acknowledgement,sequence+data_len,'')
  pl_sequence = sequence+data_len
  start_ack = time.clock()
  recv('')
  while not (sequence == pl_sequence and recv_flag == 16):
    recv('')
    if (time.clock() - start_ack) > 60.0:
       send_pack (4,acknowledgement,pl_sequence,'')

  while not (sequence == pl_sequence and recv_flag == 17):
    recv('')
  send_pack(2,acknowledgement,sequence+1,'')
  
  sys.exit()
  
# Receive a packet after syn     
recv ('')

while not (recv_flag == 18 and acknowledgement == initial_seq_no + 1):
  recv('')
  if (time.clock() - start_syn) > 60:
    send_pack(1,initial_seq_no,0,'')

if d_addr == source_ip and tcp_source == dest_port:
      if recv_flag == 18:		#syn + ack
        pl_sequence = sequence + 1
        
        send_pack(2,acknowledgement,sequence+1,'')
	user_data = "GET "+path+" HTTP/1.0\r\n"+"Host:"+host+"\r\n"+"User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:23.0) Gecko/20100101 Firefox/23.0\r\n"+"Connection: keep-alive\r\n\r\n" 
	send_pack(3,acknowledgement,sequence+1,user_data)
        http_req_seq = sequence + 1
        http_req_ack = acknowledgement
	start = time.clock()
  
remembered_data = 0
flag = 0
tcp_map = {}
count = 0

recv('')

while not (sequence == pl_sequence and recv_flag == 16):
     recv('')
     if (time.clock() - start) > 60:
        send_pack(3,http_req_ack,http_req_seq,user_data) 
         

count = 0
flag = 0
flag1 = 0
fcontentlength = 0
while True:
    global count
    global flag
    global fcontentlength
    http_response = 'HTTP/'
    http_response_1 = 'HTTP/1.1 200 OK'
    http_response_2 = 'HTTP/1.0 200 OK'
    recv('')
    if d_addr == source_ip and tcp_source == dest_port:
      if http_response in data and flag1 == 0:
	if http_response_1 in data or http_response_2 in data:
	 if 'Content-Length' in data and flag1 == 0:
             flag1 == 1
	     headers,body = data.split('\r\n\r\n')
             header = headers.replace('\r\n',' ')
             headerlist = header.split(' ')
             x = headerlist.index('Content-Length:')
             contentlength = int(headerlist[x+1])
             contentlength -= len(body)
             send_pack(2,acknowledgement,sequence+data_length,'')
             pl_sequence = sequence+data_length
             initseq = sequence
	     tcp_map[sequence] = data
         else:
	     initseq = sequence
	     tcp_map[sequence] = data
             send_pack(2,acknowledgement,sequence+data_length,'')
             teardownonfin(data_length+1)
	else:
	  print "Some Invalid HTTP response was recieved."
	  sys.exit()
      elif sequence == pl_sequence:
	  if recv_flag == 17:
	    teardownonfin(1)
	  if recv_flag == 25:
	    send_pack(2,acknowledgement,sequence+data_length,'')
            tcp_map[sequence] = data
	    teardownonfin(data_length+1)
	  if contentlength <= 0:
	    
	    tcp_map[sequence] = data
            send_pack(2,acknowledgement,sequence+data_length,'')
	    teardownonack(data_length)
          send_pack(2,acknowledgement,sequence+data_length,'')
          tcp_map[sequence] = data
   	  pl_sequence = checkqueue(sequence+data_length)
	  contentlength -= len(data)
	  flag = 0
	  
      else:
	   tcp_map[sequence] = data		#check for data present at sequence only then reduce content_length
           send_pack(2,acknowledgement,pl_sequence,'')
	   if flag == 0:
	   	remembered_data = data_length
	   	flag = 1
