import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileWriter;
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

public class ToRun implements Runnable {
	private WebCrawler myCrawl;
	private String myLink;
	public Map<String,String> httpHeader = new HashMap<String, String>();
	Socket mySocket = null;
	BufferedReader reader = null;
	PrintWriter writer=null;
	private List<String> myList = new ArrayList<String>();
	public ToRun(WebCrawler crawl, String link, String cookie) {
		myCrawl=crawl;
		myList.add(link);
		httpHeader.put("Cookie", cookie);
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
	
	public String get(String page) {
		String serverName = "129.10.113.83";
		int portNumber = 80;
		try {
			 mySocket = new Socket(serverName, portNumber);
			} catch (UnknownHostException e1) {
			
				e1.printStackTrace();
			} catch (IOException e1) {
				e1.printStackTrace();
			}
		try {
			writer = new PrintWriter(new OutputStreamWriter(mySocket.getOutputStream()));
		} catch (IOException e2) {
	
			e2.printStackTrace();
		}
		try {
			reader = new BufferedReader(new InputStreamReader(mySocket.getInputStream()));
		} catch (IOException e1) {
	
			e1.printStackTrace();
		}

		httpHeader.put("Host","129.10.113.83");

		httpHeader.put("Referer", "http://129.10.113.83/accounts/login/?next=/fakebook/");
		httpHeader.put("Connection", "close");
        
        writer.println("GET "+ page +" HTTP/1.0");
        writer.print(headerToString());
        writer.println("");
        writer.flush();
        String htmlpage="",line="";
        int code=0;
        try {
        	line=reader.readLine();
        	if(line.contains("HTTP"))
				{
					
					String tempSplit[];
					tempSplit= line.split(" ");
					if(tempSplit[1].equals("200"))
					{
						code=200;
					}
					else if(tempSplit[1].equals("320"))
					{
						code=320;
					}
					else if(tempSplit[1].equals("500"))
					{
						code=500;
					}
					
				}
						if(code == 500)
						{
						
							writer.close();
						    try {
								reader.close();
							} catch (IOException e) {
								// TODO Auto-generated catch block
								e.printStackTrace();
							}
							
							
							return get(page);
						}
			while((line = reader.readLine()) != null) {
				
				switch(code) {
						case 200: htmlpage = htmlpage + line;
							break;
						case 320: if(line.contains("location")) {
							String moreSplit[];
							moreSplit= line.split(": ");
							writer.close();
						    try {
								reader.close();
							} catch (IOException e) {
								// TODO Auto-generated catch block
								e.printStackTrace();
							}
							get(moreSplit[1]);
						}
							break;

						default:
							break;
					}
			}
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		} 
        writer.close();
        try {
			reader.close();
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		try {
				mySocket.close();
			} catch (IOException e) {
				e.printStackTrace();
			}		
        return htmlpage;
	}

	@Override
	public void run() {
		String serverName = "129.10.113.83";
		int portNumber = 80;
		
		while(!myList.isEmpty() && myCrawl.getFlagLength()<5) {

			myLink = myList.get(0);
			if(!myCrawl.isCrawled(myLink))
			{
				String page = get(myLink);
				Document doc = Jsoup.parse(page);
				Elements flags = doc.getElementsByClass("secret_flag");
				for(Element flag : flags) {
					myCrawl.addflag(flag.text());
					File file = new File("flag.txt");
					 
					// if file doesnt exists, then create it
					if (!file.exists()) {
						try {
							file.createNewFile();
						} catch (IOException e) {
						
							e.printStackTrace();
						}
					}
						try {							
							FileWriter fw = new FileWriter(file.getAbsoluteFile(),true);
							fw.write(flag.text()+"\n");
							fw.close();
						} catch (IOException e) {
							// TODO Auto-generated catch block
							e.printStackTrace();
						}
		 
					
				}
				Elements links = doc.getElementsByTag("a");
				for (Element link : links) {
					String linkHref = link.attr("href");
					String linkText = link.text();
					if(!linkHref.contains("fakebook"))
						links.removeAttr(linkHref);
					else {
						myList.add(linkHref);
					}
				}
				myList.remove(myLink);
				myCrawl.add(myLink);
			}
			else
				myList.remove(myLink);

		}
		
	}
	public void getlinks(){
		synchronized( this ) {

		}
	}

}