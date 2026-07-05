package app

import (
	"fmt"
	"os"

	"github.com/charmbracelet/bubbles/textinput"
	"github.com/charmbracelet/bubbles/viewport"
	tea "github.com/charmbracelet/bubbletea"
)

type SystemStatus struct {
	Name           string
	Location       string
	ConnectedUsers int
	CPUUsage       float64
	RAMUsage       float64
	State          string
}

type Characteristics struct {
	width_console  int
	height_console int
	ready          bool

	leftPanelWidth  int
	rightPanelWidth int
	panelHeight     int

	logger      viewport.Model
	logHistory  []string
	wrappedLog  []string
	wrapWidth   int
	logChannel  chan string
	cmdInput    textinput.Model
	commandChan chan string

	status     SystemStatus
	statusChan chan SystemStatus

	prefixActive bool
}

type LogMsg string
type StatusMsg SystemStatus

func Launch_App(logChan chan string, statusChan chan SystemStatus, cmdChan chan string) {
	input := textinput.New()
	input.Placeholder = "Escribe un comando y presiona Enter..."
	input.Prompt = "❯ "
	input.CharLimit = 256
	input.Focus()

	m := Characteristics{
		logChannel:  logChan,
		statusChan:  statusChan,
		commandChan: cmdChan,
		logHistory:  []string{formatLogLine("INFO", "Iniciando sistema...")},
		cmdInput:    input,
		status: SystemStatus{
			Name:  "—",
			State: "desconocido",
		},
	}

	p := tea.NewProgram(m, tea.WithAltScreen())
	if _, err := p.Run(); err != nil {
		fmt.Printf("Error: %v\n", err)
		os.Exit(1)
	}
}
