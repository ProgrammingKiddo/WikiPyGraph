import pika
import sys
import os, time
import dropbox



TOKEN = 'zaOSmPB-YZAAAAAAAAAABs6lSuUqn7vXbcEfSZjZeNkTyrOMDGgjnV8rjcegmPlZ'


def publish(self, msg):

    print("Conectando con Dropbox...")
    dbx = dropbox.Dropbox(TOKEN)
    user = dbx.users_get_current_account()
    print("Usuario " + user.name.display_name + " de " + user.country)

    print("\n\nSubiendo diagrama a Dropbox...")

    try:
        nombre = [line.split(":")[0]]
        fichero = "/" + nombre + "png"
        dbx.files_upload(msg, fichero, mode=dropbox.files.WriteMode('overwrite'))
        print("hi")
    except dropbox.exceptions.ApiError as err:
        if (err.error.is_path() and
                err.error.get_path().reason.is_insufficient_space()):
            sys.exit("ERROR: Cannot back up; insufficient space.")
        elif err.user_message_text:
            print(err.user_message_text)
            sys.exit()
        else:
            print(err)
            sys.exit()

    metadata = dropbox.sharing.GetFileMetadataIndividualResult(fichero)
    finalURL = metadata.preview_url
    channel.basic_publish(exchange='', routing_key='linkDropbox', body=finalURL)



def callback(ch, method, properties, body) :
    self.publish(body)



url = os.environ.get('CLOUDAMQP_URL', 'amqp://guest:guest@localhost:5672/%2f')
params = pika.URLParameters(url)
connection = pika.BlockingConnection(params)

channel = connection.channel()
channel.queue_declare(queue='graficosRelacion') # Cola de lectura
channel.queue_declare(queue='linkDropbox') # Cola de escritura

channel.basic_consume(callback, queue='graficosRelacion', no_ack=True)
channel.start_consuming()
connection.close()