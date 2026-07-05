package main

import (
	"github.com/coreos/go-systemd/v22/journal"

	"bedrock-clt/config"
	"bedrock-clt/connection/channel"
	"bufio"
	"fmt"
	"log"
	"log/slog"
	"os/exec"
)

func main() {
	var channel_connection = make(chan channel.Lenguage_Channel)
	var cmd_exec []string

	Configuration, err := config.Load_Configuration()
	if err != nil {
		slog.Error("[B-CLT]", "error", err)
		return
	}

	cmd_exec = append(cmd_exec, Configuration.Launch_command...)
	cmd_exec = append(cmd_exec, "nice", "-n", "-20", "./bedrock_server")

	process_server := exec.Command(cmd_exec[0], cmd_exec[1:]...)
	process_server.Dir = Configuration.Path_server

	stdout, err := process_server.StdoutPipe()
	if err != nil {
		slog.Error("Error al enlazar el flujo de salida: ", "error", err)
		return
	}

	process_server.Stderr = process_server.Stdout

	stdin, err := process_server.StdinPipe()
	if err != nil {
		slog.Error("Error al enlazar el flujo de entrada (Stdin): ", "error", err)
		return
	}

	if err := process_server.Start(); err != nil {
		slog.Error("Error crítico al iniciar el subproceso: ", "error", err)
		return
	}

	fmt.Println("[B-CLT] ¡Servidor iniciado con éxito!")
	fmt.Println(Configuration.Path_server)

	go channel.Connection_Sock(channel_connection, Configuration.Path_sock)

	go func() {
		scanner := bufio.NewScanner(stdout)
		for scanner.Scan() {
			journal.Send(scanner.Text(), journal.PriInfo, map[string]string{
				"SYSLOG_IDENTIFIER": "bedrock-clt_process_BDS",
			})
		}
	}()

	go func() {
		defer stdin.Close()

		for {
			message := <-channel_connection
			if message.Error != nil {
				slog.Error("[B_CLT] - Error: No se logro iniciar el socket", "error", err)
				return
			}

			journal.Send(fmt.Sprintf("[CONSOLA CMD] Ejecutando: %s", message.Message), journal.PriInfo, map[string]string{
				"SYSLOG_IDENTIFIER": "bedrock-clt_process_BDS",
				"COMMAND_EXECUTED":  message.Message,
			})

			_, err := fmt.Fprintln(stdin, message.Message)
			if err != nil {
				slog.Error("Error al enviar comando al servidor", "error", err)
				return
			}
		}
	}()

	if err := process_server.Wait(); err != nil {
		log.Printf("El servidor de Minecraft se detuvo: %v", err)
	} else {
		fmt.Println("Servidor cerrado de forma limpia.")
	}
}
