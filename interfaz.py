import sys
import os
import pika



def callback(self, ch, method, properties, body):
    print(body)


url = os.environ.get('CLOUDAMQP_URL', 'amqp://guest:guest@localhost:5672/%2f')
params = pika.URLParameters(url)
params.socket_timeout = 5
connection = pika.BlockingConnection(params)

channel = connection.channel()
channel.queue_declare(queue='linkDropbox') # Cola de lectura
channel.queue_declare(queue='scrapyInput') # Cola de escritura


print("Bienvenido al generador de gráficos de Wikipedia España.")
print("\nIntroduzca el nombre del articulo a buscar: ")
nombre = sys.stdin.read()
print("Introduzca la url del articulo:")
url = sys.stdin.read()
print("Introduzca el numero de enlaces a buscar en el artículo:")
n_enlaces = sys.stdin.read()
print("Introduzca el numero de saltos a realizar durante la busqueda:")
n_saltos = sys.stdin.read()

input = nombre.rstrip() + "$" + url.rstrip() + "$" + n_enlaces.rstrip() + "$" + n_saltos.rstrip()

channel.basic_publish(exchange='', routing_key='scrapyInput', body=input)

print("\nEnviado, esperando para consumir...\n")
print(input)

channel.basic_consume(callback, queue='linkDropbox', no_ack=True)
channel.start_consuming()
connection.close()

""" Un comentario eLn Python """