import pika, os, json

print("Iniciando o envio de tarefas...")

# Pega o segredo que vamos configurar no Render
url = os.environ.get('RABBITMQ_URL')
if not url:
    raise ValueError("A variável RABBITMQ_URL não foi encontrada!")

# Conecta no CloudAMQP
params = pika.URLParameters(url)
connection = pika.BlockingConnection(params)
channel = connection.channel()

# Cria a fila se ela não existir
channel.queue_declare(queue='scraping_tasks', durable=True)

# Portais que vamos raspar
sites = [
    {'url': 'https://g1.globo.com/tecnologia/', 'fonte': 'G1 Tecnologia'},
    {'url': 'https://techcrunch.com/', 'fonte': 'TechCrunch'}
]

# Envia para a fila
for site in sites:
    mensagem = json.dumps(site)
    channel.basic_publish(
        exchange='',
        routing_key='scraping_tasks',
        body=mensagem,
        properties=pika.BasicProperties(delivery_mode=2)
    )
    print(f'Tarefa na fila: {mensagem}')

connection.close()
print("Processo finalizado com sucesso!")
