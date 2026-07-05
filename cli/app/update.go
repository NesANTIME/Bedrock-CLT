package app

import (
	"strings"
	"time"

	"github.com/charmbracelet/bubbles/textinput"
	"github.com/charmbracelet/bubbles/viewport"
	tea "github.com/charmbracelet/bubbletea"
)

func waitForLogs(logChan chan string) tea.Cmd {
	return func() tea.Msg {
		msg, ok := <-logChan
		if !ok {
			return nil
		}
		return LogMsg(msg)
	}
}

func waitForStatus(statusChan chan SystemStatus) tea.Cmd {
	return func() tea.Msg {
		msg, ok := <-statusChan
		if !ok {
			return nil
		}
		return StatusMsg(msg)
	}
}

func formatLogLine(level, msg string) string {
	ts := time.Now().Format("15:04:05")
	return ts + " " + logLevelStyle(level).Render("["+level+"]") + " " + msg
}

func (c Characteristics) handleKey(msg tea.KeyMsg) (tea.Model, tea.Cmd) {
	if c.prefixActive {
		c.prefixActive = false
		if msg.String() == "d" {
			return c, tea.Quit
		}
	}

	switch msg.String() {
	case "ctrl+b":
		c.prefixActive = true
		return c, nil

	case "up":
		c.logger.LineUp(1)
		return c, nil
	case "down":
		c.logger.LineDown(1)
		return c, nil
	case "pgup":
		c.logger.HalfViewUp()
		return c, nil
	case "pgdown":
		c.logger.HalfViewDown()
		return c, nil

	case "enter":
		cmdText := strings.TrimSpace(c.cmdInput.Value())
		if cmdText != "" {
			c.appendLogLines(formatLogLine("CMD", cmdText))
			c.logger.GotoBottom()
			if c.commandChan != nil {
				select {
				case c.commandChan <- cmdText:
				default:
				}
			}
			c.cmdInput.Reset()
		}
		return c, nil
	}

	var cmd tea.Cmd
	c.cmdInput, cmd = c.cmdInput.Update(msg)
	return c, cmd
}

func (c *Characteristics) rewrapAll() {
	width := c.logger.Width
	if width < 1 {
		width = 1
	}
	c.wrapWidth = width
	c.wrappedLog = make([]string, 0, len(c.logHistory))
	for _, line := range c.logHistory {
		c.wrappedLog = append(c.wrappedLog, wrapLogLine(line, width))
	}
	c.logger.SetContent(strings.Join(c.wrappedLog, "\n"))
}

func (c *Characteristics) appendLogLines(lines ...string) {
	width := c.logger.Width
	if width < 1 {
		width = 1
	}

	if width != c.wrapWidth {
		c.logHistory = append(c.logHistory, lines...)
		c.rewrapAll()
		return
	}

	c.logHistory = append(c.logHistory, lines...)
	for _, line := range lines {
		c.wrappedLog = append(c.wrappedLog, wrapLogLine(line, width))
	}
	c.logger.SetContent(strings.Join(c.wrappedLog, "\n"))
}

// Funciones principales

func (c Characteristics) Init() tea.Cmd {
	cmds := []tea.Cmd{textinput.Blink}
	if c.logChannel != nil {
		cmds = append(cmds, waitForLogs(c.logChannel))
	}
	if c.statusChan != nil {
		cmds = append(cmds, waitForStatus(c.statusChan))
	}
	return tea.Batch(cmds...)
}

func (c Characteristics) Update(msg tea.Msg) (tea.Model, tea.Cmd) {
	switch msg := msg.(type) {

	case LogMsg:
		raw := strings.TrimRight(string(msg), "\r\n")
		if raw != "" {
			parts := strings.Split(raw, "\n")
			newLines := make([]string, 0, len(parts))
			for _, line := range parts {
				newLines = append(newLines, formatLogLine("LOG", line))
			}
			c.appendLogLines(newLines...)
			c.logger.GotoBottom()
		}
		return c, waitForLogs(c.logChannel)

	case StatusMsg:
		c.status = SystemStatus(msg)
		return c, waitForStatus(c.statusChan)

	case tea.WindowSizeMsg:
		c.width_console = msg.Width
		c.height_console = msg.Height
		if !c.ready {
			c.logger = viewport.New(0, 0)
			c.ready = true
		}
		c.recalcLayout()
		c.rewrapAll()
		c.logger.GotoBottom()
		return c, nil

	case tea.KeyMsg:
		return c.handleKey(msg)
	}

	var cmd tea.Cmd
	c.logger, cmd = c.logger.Update(msg)
	return c, cmd
}
