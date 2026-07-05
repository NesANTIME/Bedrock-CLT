package channel

import (
	"bufio"
	"fmt"
	"log/slog"
	"net"
	"os"
	"strings"
	"sync"
)

type Lenguage_Channel struct {
	Message string
	Error   error
}

var (
	isBusy      bool
	statusMutex sync.Mutex
)

func Connection_Sock(channel_connection chan Lenguage_Channel, Path_sock string) {
	if err := os.RemoveAll(Path_sock); err != nil {
		slog.Error("[B-CLT] - Error: No se logro limpiar el socket antiguo", "error", err)
		channel_connection <- Lenguage_Channel{Error: err}
		return
	}

	listener, err := net.Listen("unix", Path_sock)
	if err != nil {
		slog.Error("[B_CLT] - Error: No se logro iniciar el socket", "error", err)
		channel_connection <- Lenguage_Channel{Error: err}
		return
	}

	defer listener.Close()

	if err := os.Chmod(Path_sock, 0666); err != nil {
		slog.Warn("No se pudieron establecer permisos en el socket", "error", err)
	}

	slog.Info("[B-CLT] - OK: Socket iniciado correctamente!")

	for {
		conn, err := listener.Accept()
		if err != nil {
			slog.Error("[B-CLT] - Error: No se logro establecer una conexion recientemente. %v\n", "error", err)
			continue
		}

		statusMutex.Lock()
		if isBusy {
			statusMutex.Unlock()
			fmt.Fprintln(conn, "ERROR: No se pudo establecer conexión. ¡Ya hay una consola conectada!")
			conn.Close()
			slog.Warn("[B-CLT]: Conexion rechazada: Un cliente ha intentado una conexion!")
			continue
		}

		isBusy = true
		statusMutex.Unlock()

		go reader_channel(conn, channel_connection)
	}
}

func reader_channel(conn net.Conn, channel chan Lenguage_Channel) {
	defer func() {
		conn.Close()
		statusMutex.Lock()
		isBusy = false
		statusMutex.Unlock()
	}()

	channel <- Lenguage_Channel{Message: "[B-CLT] Conectado con exito!", Error: nil}

	scanner := bufio.NewScanner(conn)
	for scanner.Scan() {
		text := strings.TrimSpace(scanner.Text())
		if text == "" {
			continue
		}
		channel <- Lenguage_Channel{Message: text}
	}

	if err := scanner.Err(); err != nil {
		slog.Error("[B-CLT] - Error: No se logro leer la conexión socket", "error", err)
	}

}
