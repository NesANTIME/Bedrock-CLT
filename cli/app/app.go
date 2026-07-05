package app

import (
	"fmt"
	"os"

	"github.com/charmbracelet/bubbles/viewport"
	tea "github.com/charmbracelet/bubbletea"
)

type Characteristics struct {
	width_console  int
	height_console int
	ready          bool

	logger     viewport.Model
	logChannel chan string
	logHistory []string
}

func Launch_App(LogChan chan string) {
	p := tea.NewProgram(
		Characteristics{
			logChannel: LogChan,
			logHistory: []string{"[!] Iniciando sistema..."},
		}, tea.WithAltScreen())

	if _, err := p.Run(); err != nil {
		fmt.Printf("Error: %v\n", err)
		os.Exit(1)
	}
}
