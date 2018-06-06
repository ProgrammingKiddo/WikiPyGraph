import scrapy
import pika, os, logging
from scrapy.selector import Selector 
from scrapy.http.request import Request

class WikiSpider(scrapy.Spider):



    name="Wiki Spider"
    cuerpo = ""
    origen = []
    urls = []
    n_enlaces = 0
    n_saltos = 0
    n_terminos = 0
    c_saltos = 0
    saltos = 0

    url = os.environ.get('CLOUDAMQP_URL', 'amqp://guest:guest@localhost:5672/%2f')
    params = pika.URLParameters(url)
    connection = pika.BlockingConnection(params)

    channel = connection.channel() # Abrimos un canal de comunicación
    channel.queue_declare(queue='scrapyInput') # Cola de lectura
    channel.queue_declare(queue="relacionNodos") # Cola de escritura

    channel.basic_consume(callback, queue='scrapyInput', no_ack=True)
    channel.start_consuming()
    connection.close()


    def input_proces(self, mensaje):

        for line in mensaje:
            origen=[line.split("$")[0]]
            urls=[line.split("$")[1]]
            n_enlaces=int(line.split("$")[2])
            n_saltos=int(line.split("$")[3])
            saltos=n_saltos*n_enlaces
        n_terminos=0
        c_saltos=0
        #Nombre$enlace$enlaces$saltos

    #Creamos una función que va a ser llamada al llegar procesos nuevos
    # a la cola de mensajes
    def callback(self, ch, method, properties, body):
        self.input_proces(body)

    def start_requests(self):
        yield Request(WikiSpider.urls[0], self.parse)

    def parse(self, response):
        #nombre=WikiSpider.origen[0]+"_"+str(WikiSpider.n_enlaces)+"_"+str(WikiSpider.n_saltos)
        
        self.cuerpo += WikiSpider.origen[WikiSpider.n_terminos]+":"
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

            if n_enlaces_rec>0:
                self.cuerpo += text + "/"
            else:
                self.cuerpo += text + "/n"
            if WikiSpider.c_saltos<WikiSpider.saltos:
                WikiSpider.c_saltos=WikiSpider.c_saltos+1
                yield response.follow(WikiSpider.urls[WikiSpider.c_saltos], self.parse)
                
        self.channel.basic_publish(exchange="", routing_key="relacionNodos", body=cuerpo)
