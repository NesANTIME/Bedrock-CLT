package main

import (
	"github.com/coreos/go-systemd/v22/journal"

	"bedrock-clt/config"
	"bufio"
	"fmt"
	"log"
	"log/slog"
	"os/exec"
)

func main() {
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

	if err := process_server.Start(); err != nil {
		slog.Error("Error crítico al iniciar el subproceso: ", "error", err)
		return
	}

	fmt.Println("[B-CLT] ¡Servidor iniciado con éxito!")
	fmt.Println(Configuration.Path_server)

	go func() {
		scanner := bufio.NewScanner(stdout)
		for scanner.Scan() {
			journal.Send(scanner.Text(), journal.PriInfo, map[string]string{
				"SYSLOG_IDENTIFIER": "bedrock-clt_process_BDS",
			})
		}
	}()

	if err := process_server.Wait(); err != nil {
		log.Printf("El servidor de Minecraft se detuvo: %v", err)
	} else {
		fmt.Println("Servidor cerrado de forma limpia.")
	}
}
