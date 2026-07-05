package app

import (
	"strings"

	"github.com/charmbracelet/bubbles/viewport"
	tea "github.com/charmbracelet/bubbletea"
)

type LogMsg string

func waitForLogs(logChan chan string) tea.Cmd {
	return func() tea.Msg {
		msg, ok := <-logChan
		if !ok {
			return nil
		}
		return LogMsg(msg)
	}
}

// Funcion principal "Init"
func (c Characteristics) Init() tea.Cmd {
	return waitForLogs(c.logChannel)
}

// Funcion Principal "Update"
func (c Characteristics) Update(msg tea.Msg) (tea.Model, tea.Cmd) {
	var cmd tea.Cmd
	var cmds []tea.Cmd

	switch msg := msg.(type) {
	case LogMsg:
		c.logHistory = append(c.logHistory, string(msg))
		c.logger.SetContent(strings.Join(c.logHistory, "\n"))
		c.logger.GotoBottom()

		return c, waitForLogs(c.logChannel)

	case tea.KeyMsg:
		switch msg.String() {
		case "q", "ctrl+c", "esc":
			return c, tea.Quit
		}

	case tea.WindowSizeMsg:
		c.width_console = msg.Width
		c.height_console = msg.Height

		leftWidth := c.width_console / 2
		panelHeight := c.height_console - 2
		viewportHeight := panelHeight - 3

		if !c.ready {
			c.logger = viewport.New(leftWidth-2, viewportHeight)
			c.logger.SetContent(strings.Join(c.logHistory, "\n"))
			c.ready = true
		} else {
			c.logger.Width = leftWidth - 2
			c.logger.Height = viewportHeight
		}
		return c, nil
	}

	c.logger, cmd = c.logger.Update(msg)
	cmds = append(cmds, cmd)

	return c, tea.Batch(cmds...)
}
