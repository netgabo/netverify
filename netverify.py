import os
import socket
import datetime
import time
import winsound

FILE = os.path.join(os.getcwd(), "networkinfo.log")

# creando un archivo de registro en el directorio actual
# ??getcwd?? obtener directorio actual,
# función OS, ??path?? para especificar la ruta


def ping():
	# Hacer ping a un IP en particular 
	try:
		socket.setdefaulttimeout(3)
		# si la interrupción de datos ocurre durante 3 segundos
		# <except> parte se ejecutará

		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		# AF_INET: Dirección familiar
		# SOCK_STREAM: tipo para TCP

		host = "1.1.1.1"
		port = 53

		server_address = (host, port)
		s.connect(server_address)
        
	except OSError as error:
            return False
		# la función devuelve un valor falso
		# después de la interrupción de datos
                    
	else:
        
		s.close()
		# cerrar la conexión después de 
		# completa la comunicación con el servidor
		return True


def calculate_time(start, stop):

	# calculando la indisponibilidad de
    # tiempo y convirtiéndolo en segundos
	difference = stop - start
	seconds = float(str(difference.total_seconds()))
	return str(datetime.timedelta(seconds=seconds)).split(".")[0]
    

   
def first_check():

	# para comprobar si el sistema ya estaba
    # conectado a una conexión a Internet
	if ping():
		# Si ping devuelve true
            
		live = "\nCONECTADO A LA RED\n"
		print(live)
        # Inicia un sonido al establecerse la conexión
		connection_acquired_time = datetime.datetime.now(winsound.PlaySound("ESTABLE.wav", winsound.SND_ASYNC | winsound.SND_ALIAS ))
		aquiring_message = "Conectado a internet: " + \
			str(connection_acquired_time).split(".")[0]
		print(aquiring_message)

        
        
		with open(FILE, "a") as file:
		
			# writes into the log file
			file.write(live)
			file.write(aquiring_message)
        
		return True
    

	else:
		# Si ping devuelve false
		not_live = "\nNO CONECTADO A LA RED \n" 
		print(not_live)
        
		with open(FILE, "a") as file:
			# writes into the log file
			file.write(not_live)
		return False


def main():

	# main función para llamar funciones
    # Inicia un sonido al establecerse la conexión
	monitor_start_time = datetime.datetime.now(winsound.PlaySound("CONNECTING.wav", winsound.SND_ASYNC | winsound.SND_ALIAS ))
	monitoring_date_time = "Monitoreando: " + \
		str(monitor_start_time).split(".")[0]
        
	if first_check():
		# Si es true
		print(monitoring_date_time)
		# el monitoreo solo comenzará cuando
        # se adquirirá la conexión
        
	else:
		# Si false
		while True:
		
			# bucle infinito para ver si se adquiere la conexión
			if not ping():
				
				# si la conexión no se adquiere
				time.sleep(1)
			else:
				
				# si se adquiere la conexión
				first_check()
				print(monitoring_date_time)
				break
                
	with open(FILE, "a") as file:
	
		# escribir en el archivo como en networkinfo.log,
        # "a" - append: abre el archivo para agregar,
        # crea el archivo si no existe ???
		file.write("\n")
		file.write(monitoring_date_time + "\n") 

	while True:
	
        # bucle infinito, ya que estamos monitoreando 
        # la conexión de red hasta que la máquina se ejecuta
		if ping():
			
			# Si es true: el ciclo se ejecutará cada 5 segundos
			time.sleep(1)
            

		else:
			# Si es false: se mostrará un mensaje de error
            # Inicia un sonido al no haber conexión
			down_time = datetime.datetime.now(winsound.PlaySound("DISCONNECTING.wav", winsound.SND_ASYNC | winsound.SND_ALIAS ))
			fail_msg = "Sin Internet: " + str(down_time).split(".")[0]
			print(fail_msg)
            
			with open(FILE, "a") as file:
				# writes into the log file
				file.write(fail_msg + "\n") 
                

			while not ping():
			
				# Bucle infinito, se ejecutará hasta que ping() devuelva true
				time.sleep(1)
            # Inicia un sonido al establecerse la conexión
			up_time = datetime.datetime.now(winsound.PlaySound("CONNECTING.wav", winsound.SND_ASYNC | winsound.SND_ALIAS ))
			
			# después de que el bucle se rompe, la conexión se restablece
			uptime_message = "Conectado a Internet: " + str(up_time).split(".")[0]
            
			down_time = calculate_time(down_time, up_time)
			unavailablity_time = "Tiempo desconectado: " + down_time
            

			print(uptime_message)
			print(unavailablity_time)
            

			with open(FILE, "a") as file:
				
                # entrada de registro para el tiempo de restauración de la conexión,
                # y tiempo de indisponibilidad
				file.write(uptime_message + "\n")
				file.write(unavailablity_time + "\n")

main()
