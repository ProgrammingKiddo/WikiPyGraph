import scrapy
from scrapy.selector import Selector 
from scrapy.http.request import Request

class WikiSpider(scrapy.Spider):
    name="Wiki Spider"
    file=open("origen.txt","r")
    n_enlaces=1
    for line in file:
        origen=[line.split("$")[0]]
        urls=[line.split("$")[1]]
        n_enlaces=int(line.split("$")[2])
        n_saltos=int(line.split("$")[3])
        saltos=n_saltos*n_enlaces
    n_terminos=0
    c_saltos=0
    #Nombre$enlace$enlaces$saltos

    def start_requests(self):
        yield Request(WikiSpider.urls[0], self.parse)

    def parse(self, response):
        nombre=WikiSpider.origen[0]+"_"+str(WikiSpider.n_enlaces)+"_"+str(WikiSpider.n_saltos)
        file = open(nombre+".txt","a")
        file.write(WikiSpider.origen[WikiSpider.n_terminos]+":")
        WikiSpider.n_terminos=WikiSpider.n_terminos+1
        a_selectors = response.xpath("//p/a")
        iterator=iter(a_selectors)
        n_enlaces_rec = WikiSpider.n_enlaces
        

        while n_enlaces_rec>0:
            n_enlaces_rec=n_enlaces_rec-1
            selector=next(iterator)
            text = str(selector.xpath("text()").extract_first())
            link = selector.xpath("@href").extract_first()
            WikiSpider.urls.append(link)
            WikiSpider.origen.append(text)
            print("Listo")
            if n_enlaces_rec>0:
                file.write(text+"/")
            else:
                file.write(text+"\n")
            if WikiSpider.c_saltos<WikiSpider.saltos:
                WikiSpider.c_saltos=WikiSpider.c_saltos+1
                yield response.follow(WikiSpider.urls[WikiSpider.c_saltos], self.parse)
        file.close