#     Sistema para controle de temperatura criado na matéria de Fundamentos de 
#     Internet das Coisas do curso de ADS da PUCPR. Juntamente com o colega 
#     Dyonata, a gente desenvolveu todo o código que faz a leitura da temperatura
#     utilizando um sensor de temperatura e umidade DHT, um relé, um módulo ESP32
#     e uma API chamada ThingSpeak para visualização das informações geradas.
#     Criado por Thiago Souza e Dyonata Mahcado no ano de 2022.

import machine
import time
from wifi_lib import conecta
import urequests
import dht

rele = machine.Pin(2, machine.Pin.OUT)
rele.value(0)

dht = dht.DHT11(machine.Pin(4))
station = conecta("Ap 11 2.4G", "32392937")

if not station.isconnected():
    print("Não há conexão")
else:
    print("Conectado")

while True:
    dht.measure()

    temperatura = dht.temperature()
    umidade = dht.humidity()
    
    if temperatura > 31 or umidade > 70:
        rele.value(1)
    else:
        rele.value(0)
        
    print("Temperatura: {} - Umidade: {}".format(temperatura, umidade))
    
    resposta = urequests.get("https://api.thingspeak.com/update?api_key=S45VONYYXT9GMYKX&field1={}&field2={}".format(temperatura, umidade))
    print('resposta', resposta.text)
    time.sleep(15)