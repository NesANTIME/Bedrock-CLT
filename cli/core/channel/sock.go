package channel

import (
	"fmt"
	"net"
)

func ConnectSock(PathSock string, ChannelCmd chan string) {
	conn, err := net.Dial("unix", PathSock)
	if err != nil {
		fmt.Println("[B_CLT] - Error: No se logro iniciar el socket: %w", err)
		return
	}

	defer conn.Close()

	for {
		command := <-ChannelCmd
		_, err = fmt.Fprintf(conn, "%s\n", command)
		if err != nil {
			fmt.Println("[[B_CLT] - Error al enviar el comando al servidor: %w", err)
		}
	}
}
