package core

import (
	"fmt"
	"log"

	"github.com/coreos/go-systemd/v22/sdjournal"
)

func Capture_Logs(LogChan chan string) {
	j, err := sdjournal.NewJournal()
	if err != nil {
		log.Fatalf("Error abriendo la API de journald: %v", err)
	}
	defer j.Close()

	serviceName := "bedrock-clt_process_BDS"
	match := "SYSLOG_IDENTIFIER=bedrock-clt_process_BDS"

	if err := j.AddMatch(match); err != nil {
		log.Fatalf("Error añadiendo filtro: %v", err)
	}

	if err := j.SeekTail(); err != nil {
		log.Fatalf("Error buscando el final del journal: %v", err)
	}

	if _, err := j.Previous(); err != nil {
		log.Fatalf("Error posicionando el cursor: %v", err)
	}

	fmt.Printf("Monitoreando %s de forma nativa. Esperando nuevos logs...\n", serviceName)
	fmt.Println("---------------------------------------------------")

	for {
		c, err := j.Next()
		if err != nil {
			log.Fatalf("Error leyendo el siguiente log: %v", err)
		}

		if c == 0 {
			j.Wait(sdjournal.IndefiniteWait)
			continue
		}

		entry, err := j.GetEntry()
		if err != nil {
			log.Printf("Error decodificando la entrada: %v", err)
			continue
		}

		msg, hasMsg := entry.Fields["MESSAGE"]
		if !hasMsg {
			continue
		}

		LogChan <- fmt.Sprintf("%s\n", msg)
	}
}
