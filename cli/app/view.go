package app

import (
	"fmt"
	"strings"

	"github.com/charmbracelet/lipgloss"
)

const (
	panelChromeWidth  = 4
	panelChromeHeight = 2
	headerHeight      = 1
	headerGap         = 1
	separatorHeight   = 1
	inputRowHeight    = 1
	footerHeight      = 1

	leftPanelRatio     = 78
	minLeftPanelWidth  = 30
	minRightPanelWidth = 30
	minLogHeight       = 1
)

var (
	baseTitleStyle = lipgloss.NewStyle().
			Foreground(lipgloss.Color("#E0D0B0")).
			Background(lipgloss.Color("#406080")).
			Bold(true).
			Align(lipgloss.Left).
			Padding(0, 2)

	basePanelStyle = lipgloss.NewStyle().
			Border(lipgloss.RoundedBorder()).
			Padding(0, 1)

	helpStyle      = lipgloss.NewStyle().Foreground(lipgloss.Color("#555555"))
	separatorStyle = lipgloss.NewStyle().Foreground(lipgloss.Color("#3a3a3a"))
	sectionStyle   = lipgloss.NewStyle().Foreground(lipgloss.Color("#E0D0B0")).Bold(true).Underline(true)
	labelStyle     = lipgloss.NewStyle().Foreground(lipgloss.Color("#8fa8c9")).Bold(true)
	valueStyle     = lipgloss.NewStyle().Foreground(lipgloss.Color("#e0e0e0"))
)

func (c *Characteristics) recalcLayout() {
	c.leftPanelWidth = c.width_console * leftPanelRatio / 100
	c.rightPanelWidth = c.width_console - c.leftPanelWidth

	if c.rightPanelWidth < minRightPanelWidth {
		c.rightPanelWidth = minRightPanelWidth
	}
	c.leftPanelWidth = c.width_console - c.rightPanelWidth
	if c.leftPanelWidth < minLeftPanelWidth {
		c.leftPanelWidth = minLeftPanelWidth
	}

	c.panelHeight = c.height_console - headerHeight - headerGap
	if c.panelHeight < 5 {
		c.panelHeight = 5
	}

	innerWidth := c.leftPanelWidth - panelChromeWidth
	innerHeight := c.panelHeight - panelChromeHeight

	loggerHeight := innerHeight - separatorHeight - inputRowHeight - footerHeight
	if loggerHeight < minLogHeight {
		loggerHeight = minLogHeight
	}
	if innerWidth < 1 {
		innerWidth = 1
	}

	c.logger.Width = innerWidth
	c.logger.Height = loggerHeight

	promptWidth := innerWidth - len(c.cmdInput.Prompt)
	if promptWidth < 1 {
		promptWidth = 1
	}
	c.cmdInput.Width = promptWidth
}

func logLevelStyle(level string) lipgloss.Style {
	switch level {
	case "CMD":
		return lipgloss.NewStyle().Foreground(lipgloss.Color("#f0c674")).Bold(true)
	case "ERROR", "ERR":
		return lipgloss.NewStyle().Foreground(lipgloss.Color("#e06c75")).Bold(true)
	case "WARN":
		return lipgloss.NewStyle().Foreground(lipgloss.Color("#d9a441")).Bold(true)
	default: // INFO, LOG, etc.
		return lipgloss.NewStyle().Foreground(lipgloss.Color("#7fb08a")).Bold(true)
	}
}

func stateStyle(state string) lipgloss.Style {
	switch state {
	case "encendido":
		return lipgloss.NewStyle().Foreground(lipgloss.Color("#7fb08a")).Bold(true)
	case "reiniciando":
		return lipgloss.NewStyle().Foreground(lipgloss.Color("#d9a441")).Bold(true)
	case "apagado":
		return lipgloss.NewStyle().Foreground(lipgloss.Color("#e06c75")).Bold(true)
	default:
		return lipgloss.NewStyle().Foreground(lipgloss.Color("#888888"))
	}
}

func wrapLogLine(line string, width int) string {
	return lipgloss.NewStyle().Width(width).Render(line)
}

// Funcion Principal --------------------------------------------------------

func (c Characteristics) View() string {
	if !c.ready {
		return "Iniciando..."
	}

	titleStyle := baseTitleStyle.Copy().Width(c.width_console)
	leftPanelStyle := basePanelStyle.Copy().
		BorderForeground(lipgloss.Color("#60c0FF")).
		Width(c.leftPanelWidth - 2).
		Height(c.panelHeight - 2)
	rightPanelStyle := basePanelStyle.Copy().
		BorderForeground(lipgloss.Color("#8c2a3d")).
		Width(c.rightPanelWidth - 2).
		Height(c.panelHeight - 2)

	header := titleStyle.Render("••• Bedrock-CLT •••")

	// --- Panel izquierdo: logs + separador + entrada de comandos + ayuda ---
	separator := separatorStyle.Render(strings.Repeat("─", c.logger.Width))
	help := helpStyle.Render(" [↑/↓ PgUp/PgDn] Scroll  [Enter] Enviar  [Ctrl+B,D / Esc] Salir ")

	leftContent := lipgloss.JoinVertical(lipgloss.Left,
		c.logger.View(),
		separator,
		c.cmdInput.View(),
		help,
	)
	leftPanel := leftPanelStyle.Render(leftContent)

	// --- Panel derecho: estado del sistema ---
	rightPanel := rightPanelStyle.Render(c.renderStatus())

	body := lipgloss.JoinHorizontal(lipgloss.Top, leftPanel, rightPanel)
	return header + "\n" + body
}

func (c Characteristics) renderStatus() string {
	row := func(label, value string) string {
		return labelStyle.Render(fmt.Sprintf("%-11s", label+":")) + valueStyle.Render(value)
	}

	lines := []string{
		sectionStyle.Render("Estado del sistema"),
		"",
		row("Nombre", c.status.Name),
		row("Ubicación", c.status.Location),
		row("Usuarios", fmt.Sprintf("%d conectados", c.status.ConnectedUsers)),
		row("CPU", fmt.Sprintf("%.1f %%", c.status.CPUUsage)),
		row("RAM", fmt.Sprintf("%.1f %%", c.status.RAMUsage)),
		"",
		labelStyle.Render(fmt.Sprintf("%-11s", "Estado:")) + stateStyle(c.status.State).Render(c.status.State),
	}

	return lipgloss.JoinVertical(lipgloss.Left, lines...)
}
