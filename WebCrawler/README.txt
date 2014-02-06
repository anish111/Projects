High-level approch:
We have used Sockets Library in java to connect to the Server and send messages.
The messages sent to the server were raw http header which were made manually.
Looked for both approaches Http/1.1 and Http/1.0 and all its required header properties.
Started out with Http/1.1 approach to get from the login page and recieve cookies and session ids.
Implemented multi-threading which brought down the time taken to around 35 minutes.
But this approach still seemed longer so started cleaning code and looking for other alternatives.
	
Challenges Faced:
	Stuck for long on how to login. Found later looking through wireshark that a new session-id was sent on post which had to be used on the new requests.
	Did not understand the meaning of 302 status later found the session id issue and then got a sucessfull 200 message.
	Single threaded took time so started multithreading.
	Time not reducing after many changes finally closed the stream after request and it worked.

Testing:
	- Giving several differnt parameters in which not all parameters are cumpolsary to send.
	- Calling the program through script with different parameters to check whether the approach still works.
        -Tried load testing on the PC.