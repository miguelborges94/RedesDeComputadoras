importar  sys
importar  socket
importar  subprocesos
def  server_loop ( local_host , local_port , remote_host , remote_port , receive_first ):

	servidor  =  enchufe . enchufe ( enchufe . AF_INET , enchufe . SOCK_STREAM )

	prueba :
		servidor . enlazar (( local_host , local_port ))
	excepto :
				print  "[!!] Error al escuchar en $ s: $ d"  % ( local_host , local_port )
				imprimir  "[!!] Compruebe si hay otras tomas de escucha o los permisos correctos".
				sys . salir ( 0 )
				print  "[*] Escuchando en $ s: $ d"  % ( local_host , local_port )
		
		
				servidor . escuchar ( 5 )

				mientras que es  verdadero :
					client_socket , addr  =  servidor . aceptar ()

					# imprime la información de conexión local
					print  "[==>] Recibí conexión entrante de% s:% d"  % ( addr [ 0 ], addr [ 1 ])

					# iniciar un hilo para hablar con el host remoto
					proxy_thread  =  subprocesamiento . Subproceso ( target = proxy_handler , args = ( client_socket , remote_host , remote_port , receive_first ))

					proxy_thread . inicio ()

def  main ():

	# aquí no hay análisis sofisticados de la línea de comandos
	si  len ( sys . argv [ 1 :]) ! =  5 :
		imprimir  "Uso: ./tcpproxy.py [localhost] [localport] [remotehost] [remoteport] [receive_first]"
		imprimir  "Ejemplo: ./tcpproxy.py 127.0.0.1 9000 10.12.132.1 9000 True"
		sys . salir ( 0 )

	# configurar los parámetros de escucha locales
	local_host  =  sys . argv [ 1 ]
	puerto_local  =  int ( sys . argv [ 2 ])

	# configurar objetivo remoto
	host_remoto  =  sys . argv [ 3 ]
	puerto_remoto  =  int ( sys . argv [ 4 ])

	# esto le dice a nuestro proxy que se conecte y reciba datos
	# antes de enviar al host remoto
	recibir_primero  =  sys . argv [ 5 ]

	si es  "Verdadero"  en  Receive_first :
		recibir_primero  =  Verdadero
	otra cosa :
		recibir_primero  =  Falso


	# ahora gira nuestro enchufe de escucha
	server_loop ( local_host , local_port , remote_host , remote_port , receive_first )

principal ()

def  proxy_handler ( client_socket , remote_host , remote_port , receive_first ):

	# conectarse al host remoto
	toma_remoto  =  toma . enchufe ( enchufe . AF_INET , enchufe . SOCK_STREAM )

	# recibir datos del extremo remoto si es necesario
	si  recibe_primero :

		remote_buffer  =  receive_from ( socket_remoto )
		hexdump ( búfer_remoto )

		# envíelo a nuestro manejador de respuestas
		remote_buffer  =  response_handler ( socket_remoto )

		# si tenemos datos para enviar a nuestro cliente local, envíelos
		si  len ( remote_buffer ):
			print  "[<==] Enviando% d bytes a localhost".  %  len ( búfer_remoto )
			client_socket . enviar ( remote_buffer )
	# ahora vamos a recorrer y leer desde local,
		# enviar a remoto, enviar a local
	# enjuagar, lavar, repetir
	mientras que es  verdadero :

		# leer del host local
		local_buffer  =  receive_from ( client_socket )


		si  len ( local_buffer ):

			print  "[==>] Recibido% d bytes de localhost".  %  len ( búfer_local )
			hexdump ( búfer_local )

			# envíelo a nuestro gestor de solicitudes
			local_buffer  =  request_handler ( local_buffer )

			# enviar los datos al host remoto
			toma_remoto . enviar ( local_buffer )
			print  "[==>] Enviado a remoto".

			# recibir de vuelta a la respuesta
			remote_buffer  =  receive_from ( socket_remoto )

			si  len ( remote_buffer ):

				imprimir  "[<==] Recibido% d bytes desde el control remoto".  %  len ( búfer_remoto )
				hexdump ( búfer_remoto )

				# enviar a nuestro manejador de respuestas
				remote_buffer  =  response_handler ( remote_buffer )

				# envía la respuesta al socket local
				client_socket . enviar ( remote_buffer )

				print  "[<==] Enviado a localhost".

			# si no hay más datos en ninguno de los lados, cierre las conexiones
			si  no  len ( local_buffer ) o  no  len ( remote_buffer ):
				client_socket . cerrar ()
				toma_remoto . cerrar ()
				imprimir  "[*] No hay más datos. Cerrando conexiones".

				descanso

# esta es una bonita función de volcado hexadecimal directamente tomada de
# los comentarios aquí:
# http://code.activestate.com/recipes/142812-hex-dumper/
def  hexdump ( src , longitud = 16 ):
	resultado  = []
	dígitos  =  4  si  isinstance ( src , unicode ) else  2

	para  i  en  xrange ( 0 , len ( src ), longitud ):
		s  =  sr [ i : i + longitud ]
		hexa  =  b '' . unirse ([ "% 0 * X"  % ( dígitos , ord ( x )) para  x  en  s ])
		texto  =  b '' unir ([ x  si  0x20  <=  ord ( x ) <  0x7F  si no  b '.'  para  x  en  s ])
		resultado . añadir ( b "% 04X% - * s% s"  % ( i , longitud * ( dígitos  +  1 ), hexadecimal , texto ))

	imprimir  b ' \ n ' . unirse ( resultado )

def  receive_from ( conexión ):

	buffer  =  ""

	# Establecemos un tiempo de espera de 2 segundos; depende de tu
	# objetivo, es posible que deba ajustarse
	conexión . settimeout ( 2 )

		prueba :
			# siga leyendo en el búfer hasta
			# no hay más datos
			# o nos desconectamos
			mientras que es  verdadero :
				datos  =  conexión . recv ( 4096 )

				si  no son  datos :
					descanso

				búfer  + =  datos

		excepto :
		pasar

		 búfer de retorno

# modificar las solicitudes destinadas al host remoto
def  request_handler ( búfer ):
	# realizar modificaciones de paquetes
	 búfer de retorno

# modificar cualquier respuesta destinada al host local
def  manejador_respuesta ( búfer ):
	# realizar modificaciones de paquetes
	 búfer de retorno