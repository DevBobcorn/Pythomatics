import feedparser,time

src = ['https://www.minecraftglobal.com/feed/','http://www.9minecraft.net/feed/','https://wikiminecraft.com/feed/']

for url in src:
	feed = feedparser.parse(url)
	print("News Source:",feed.channel.title)
	print("There are",len(feed.entries),"pieces of news from this source.\n")
	for e in feed.entries:
		print('%-70s%s     By %s' %('[ '+e.title+' ]',time.strftime("%b/%d/%Y,%H:%M:%S(%a)", e.published_parsed),e.author))
		print('>>',e.description[3:200],'...[',e.link[0:100],']')
	print('\n\n')
