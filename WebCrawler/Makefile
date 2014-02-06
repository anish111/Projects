JFLAGS = -g
JC = javac
.SUFFIXES: .java .class
.java.class:
        
CLASSES = \
        WebCrawler.java \
        ToRun.java

default: WebCrawler.class ToRun.class

WebCrawler.class: WebCrawler.java
ToRun.class: ToRun.java
	$(JC) $(JFLAGS) -cp ./jsoup.jar WebCrawler.java ToRun.java

classes: $(CLASSES:.java=.class)
clean:
	 $(RM) *.class

