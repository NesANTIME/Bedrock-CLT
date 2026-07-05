package logger

import (
	"fmt"
	"log"

	"github.com/coreos/go-systemd/v22/sdjournal"
)

func Logger_Capt(match string, Log_Channel chan string) {
	api_journald, err := sdjournal.NewJournal()
	if err != nil {
		log.Fatalf("Error abriendo la API de journald: %v", err)
	}
	defer api_journald.Close()

	if err := api_journald.AddMatch(match); err != nil {
		log.Fatalf("Error añadiendo filtro: %v", err)
	}

	if err := api_journald.SeekTail(); err != nil {
		log.Fatalf("Error buscando el final del journal: %v", err)
	}

	if _, err := api_journald.Previous(); err != nil {
		log.Fatalf("Error posicionando el cursor: %v", err)
	}

	for {
		c, err := api_journald.Next()
		if err != nil {
			log.Fatalf("Error leyendo el siguiente log: %v", err)
		}

		if c == 0 {
			api_journald.Wait(sdjournal.IndefiniteWait)
			continue
		}

		entry, err := api_journald.GetEntry()
		if err != nil {
			log.Printf("Error decodificando la entrada: %v", err)
			continue
		}

		msg, hasMsg := entry.Fields["MESSAGE"]
		if !hasMsg {
			continue
		}

		Log_Channel <- fmt.Sprintf("%s\n", msg)
	}
}
