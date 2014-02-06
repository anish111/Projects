import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.io.PrintWriter;
import java.net.Socket;
import java.net.UnknownHostException;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Set;

import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;
import org.jsoup.nodes.Element;
import org.jsoup.select.Elements;

public class WebCrawler {
	Socket mySocket = null;
	BufferedReader reader = null;
	PrintWriter writer=null;
	public Map<String,String> httpHeader = new HashMap<String,String>();
	public static List<String> flags = new ArrayList<String>();
	public static Set<String> sitesToCrawl = new HashSet<String>();
	public static Set<String> sitesCrawled = new HashSet<String>();
	public String[] tokens;
	
	public synchronized String get(String page) {
        try {
			writer = new PrintWriter(new OutputStreamWriter(mySocket.getOutputStream()));
		} catch (IOException e2) {
			// TODO Auto-generated catch block
			e2.printStackTrace();
		}
        writer.println("GET "+ page +" HTTP/1.1");
        writer.print(headerToString());
        writer.println("");
        writer.flush();
        String htmlpage="",line="";
        try {
			reader = new BufferedReader(new InputStreamReader(mySocket.getInputStream()));
		} catch (IOException e1) {
			// TODO Auto-generated catch block
			e1.printStackTrace();
		}
        try {
        	while((line = reader.readLine()) != null) {
			    		htmlpage = htmlpage + line;
			}
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
        return htmlpage;
	}
	
	public static void main(String args[]) 
		{
				
		long startTime = System.nanoTime();
				
		String serverName = "129.10.113.83";
		String u_name = "001943901";
		String pass = "B92TF2J3";
				
		if (args.length > 0 && !args[0].isEmpty() && args[0].length()==9)
			u_name = args[0];
		if (args.length > 1 && !args[1].isEmpty())
			pass = args[1];
		WebCrawler wCrawl = new WebCrawler();
		
		int portNumber = 80;
		wCrawl.tokens = new String[20];

		// Creating a new Socket.
		try {
			wCrawl.mySocket = new Socket(serverName, portNumber);

		} catch (UnknownHostException e) {
			e.printStackTrace();
		} catch (IOException e) {
			e.printStackTrace();
		}
		
		// Writing the Hello message to the output Stream
		try {
			
            int i=0;
            String line=null;
            wCrawl.writer = new PrintWriter(new OutputStreamWriter(wCrawl.mySocket.getOutputStream()));
            String cookie="";
            String sessionId="";
           
			wCrawl.writer = new PrintWriter(new OutputStreamWriter(wCrawl.mySocket.getOutputStream()));
			wCrawl.writer.println("GET /accounts/login/?next=/fakebook/ HTTP/1.0");
			wCrawl.writer.println(wCrawl.headerToString());
			wCrawl.writer.flush();
            int i1=0;
            
            wCrawl.tokens[0]="";
            String token1[]=new String[10];
            wCrawl.reader = new BufferedReader(new InputStreamReader(wCrawl.mySocket.getInputStream()));
            while((line = wCrawl.reader.readLine()) != null) {
                if (line.isEmpty()) break; // Stop when headers are completed. We're not interested in all the HTML.
                {
                	if(line.contains("Set-Cookie")) {
                		
                		line=line.substring(12,55);
                		token1[i1++]=line.substring(10,42);
                		wCrawl.tokens[0]=wCrawl.tokens[0] + " " + line;
                		
                	}
                
                }
            }
            wCrawl.tokens[0]="Cookie:".concat(wCrawl.tokens[0]);
            wCrawl.tokens[0]=wCrawl.tokens[0].substring(0,wCrawl.tokens[0].length()-1);
            
            String[] split = new String[10];
            split = wCrawl.tokens[0].split(": ");
            if(split[1].contains("csrftoken")) {
            	cookie = split[1].split(" sessionid=")[0];
            	sessionId = split[1].split(" sessionid=")[1];
            	cookie = cookie.split("csrftoken=")[1];
            }
            
            wCrawl.mySocket.close();
    		try {
    			wCrawl.mySocket = new Socket(serverName, portNumber);

    		} catch (UnknownHostException e) {
    			e.printStackTrace();
    		} catch (IOException e) {
    			e.printStackTrace();
    		}
    		wCrawl.writer = new PrintWriter(new OutputStreamWriter(wCrawl.mySocket.getOutputStream()));
            
            wCrawl.writer.println("POST /accounts/login/ HTTP/1.0");

            wCrawl.httpHeader.put("Content-Length",new Integer(("csrfmiddlewaretoken="+token1[0]+"&username="+u_name+"&password="+pass+"&next=%2Ffakebook%2F").length()).toString());

            wCrawl.httpHeader.put("Content-Type", "application/x-www-form-urlencoded");

            wCrawl.httpHeader.put("Cookie", "csrftoken="+cookie+" sessionid="+sessionId);
            
            wCrawl.writer.print(wCrawl.headerToString());
            wCrawl.writer.println("");
            wCrawl.writer.print("csrfmiddlewaretoken="+token1[0]+"&username=001943901&password=B92TF2J3&next=%2Ffakebook%2F");
            
            wCrawl.writer.flush();
            wCrawl.tokens[0]="";
            wCrawl.tokens[1]="";

            wCrawl.reader = new BufferedReader(new InputStreamReader(wCrawl.mySocket.getInputStream()));
           
            
            while((line = wCrawl.reader.readLine()) != null) {
                if (line.isEmpty()) break; // Stop when headers are completed. We're not interested in all the HTML.
                {
                	if(line.contains("Set-Cookie")) {
                		
                		line=line.substring(12,55);
                		token1[i1++]=line.substring(10,42);
                		wCrawl.tokens[0]=wCrawl.tokens[0] + " " + line;
                		
                	}
                	
                }
            }
            wCrawl.writer.close();wCrawl.reader.close();
            wCrawl.mySocket.close();
    		try {
    			wCrawl.mySocket = new Socket(serverName, portNumber);

    		} catch (UnknownHostException e) {
    			e.printStackTrace();
    		} catch (IOException e) {
    			e.printStackTrace();
    		}
    		wCrawl.writer = new PrintWriter(new OutputStreamWriter(wCrawl.mySocket.getOutputStream()));
    		wCrawl.reader = new BufferedReader(new InputStreamReader(wCrawl.mySocket.getInputStream()));
            
            

            sessionId = wCrawl.tokens[0].split("sessionid=")[1].replace(";", "");
            
            wCrawl.writer.println("GET http://129.10.113.83/fakebook/ HTTP/1.0");

            wCrawl.httpHeader.remove("Content-Type");
            wCrawl.httpHeader.remove("Content-Length");
            
            wCrawl.httpHeader.put("Cookie", "csrftoken="+cookie+" sessionid="+sessionId);
            wCrawl.writer.print(wCrawl.headerToString());
            
            wCrawl.writer.println("");
            wCrawl.writer.flush();
            
            String htmlpage="";
            
            while((line = wCrawl.reader.readLine()) != null) {
                		htmlpage = htmlpage + line;
            }

            List<Thread> threads = new ArrayList<Thread>();
            Document doc = Jsoup.parse(htmlpage);
            wCrawl.add("/fakebook/");
            Elements links = doc.getElementsByTag("a");
            for (Element link : links) {
            	String linkHref = link.attr("href");
            
              linkHref = link.attr("href");
              String linkText = link.text();
              
              if(!linkHref.contains("fakebook"))
            	  links.removeAttr(linkHref);
              else {
            	  Runnable task = new ToRun(wCrawl,linkHref,wCrawl.httpHeader.get("Cookie"));
                  Thread crawler = new Thread(task);
                  crawler.setName(String.valueOf(i));
                  crawler.start();
                  threads.add(crawler);
              }
            }
            
              int running = 0;
              do {
                running = 0;
                for (Thread thread : threads) {
                  if (thread.isAlive()) {
                    running++;
                  }
                }
                
              } while (running > 0);
              wCrawl.mySocket.close();
		} catch(Exception e) {}
	
		HashSet hs = new HashSet(flags);
		flags.clear();
		flags.addAll(hs);
		  for (int j = 0; j < flags.size(); j++) {
		  	String tempSplit[]=flags.get(j).split(": ");
			System.out.println(tempSplit[1]);
			}
		long endTime = System.nanoTime();
		//System.out.println("Took "+(endTime - startTime) + " ns"); 
	}
	
	public String headerToString() {
		String header = "";
		for (Map.Entry<String, String> map : httpHeader.entrySet()) {
	       String key = map.getKey();
	       String value = map.getValue();
	       header = header.concat(key + ": " + value + "\r\n");
		}
		return header;
	}

	public synchronized boolean add(String linkHref) {
		if(sitesCrawled.add(linkHref))
			return true;
		return false;
	}

	public synchronized void addflag(String text) {
		flags.add(text);
	}

	public synchronized boolean isCrawled(String myLink) {
		if(sitesCrawled.contains(myLink))
			return true;
		return false;
	}

	public synchronized int getFlagLength() {
		// TODO Auto-generated method stub
		return flags.size();
	}
	
}