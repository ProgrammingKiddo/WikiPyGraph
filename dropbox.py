import pika
import dropbox
from dropbox.files import WriteMode
from dropbox.exceptions import ApiError, AuthError
import os, time



TOKEN = 'zaOSmPB-YZAAAAAAAAAABs6lSuUqn7vXbcEfSZjZeNkTyrOMDGgjnV8rjcegmPlZ'
LOCALFILE = "file.dat"
UPLOAD_PATH = "/" + LOCALFILE


def publish():

    with open(LOCALFILE, "rb") as f:
        print("\n\nSubiendo " + LOCALFILE + " a Dropbox...")

        try:
            dbx.files_upload(f.read(), UPLOAD_PATH, mode=WriteMode('overwrite'))
            print("hi")
        except ApiError as err:
            # This checks for the specific error where a user doesn't have
            # enough Dropbox space quota to upload this file
            if (err.error.is_path() and
                    err.error.get_path().reason.is_insufficient_space()):
                sys.exit("ERROR: Cannot back up; insufficient space.")
            elif err.user_message_text:
                print(err.user_message_text)
                sys.exit()
            else:
                print(err)
                sys.exit()


url = os.environ.get('CLOUDAMQP_URL', 'amqp://guest:guest@localhost:5672/%2f')
params = pika.URLParameters(url)
connection = pika.BlockingConnection(params)
channel = connection.channel()
channel.queue_declare(queue='graficosRelacion') # Cola de lectura
channel.queue_declare(queue='linkDropbox') # Cola de escritura


print("Conectando con Dropbox...")
dbx = dropbox.Dropbox(TOKEN)
user = dbx.users_get_current_account()
print("Usuario " + user.name.display_name + " de " + user.country)

publish()
print("Listo!")












# Access the CLODUAMQP_URL environment variable and parse it (fallback to localhost)

# create a function which is called on incoming messages
def callback(ch, method, properties, body):
  pdf_process_function(body)

# set up subscription on the queue
channel.basic_consume(callback,
  queue='pdfprocess',
  no_ack=True)

# start consuming (blocks)
channel.start_consuming()
connection.close()