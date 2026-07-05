package app

import "github.com/charmbracelet/lipgloss"

// Estilos Estaticos
var (
	baseTitleStyle = lipgloss.NewStyle().Foreground(lipgloss.Color("#E0D0B0")).
			Background(lipgloss.Color("#406080")).Bold(true).
			Align(lipgloss.Left).Padding(0, 2)

	basePanelStyle = lipgloss.NewStyle().Border(lipgloss.RoundedBorder()).
			Padding(0, 1)
)

func (c Characteristics) View() string {
	if !c.ready {
		return "Iniciando..."
	}

	leftWidth := c.width_console / 2
	rightWidth := c.width_console - leftWidth
	panelHeight := c.height_console - 6

	// Estilos de lipgloss
	TitleStyle := baseTitleStyle.Copy().Width(c.width_console)

	// TUS TAMAÑOS RESTAURADOS
	LeftPanelStyle := basePanelStyle.Copy().BorderForeground(lipgloss.Color("#60c0FF")).
		Width((leftWidth + 40) - 2).Height(panelHeight)

	RightPanelStyle := basePanelStyle.Copy().BorderForeground(lipgloss.Color("#8c2a3d")).
		Width(rightWidth - 42).Height(panelHeight)

	// Render
	header_render := TitleStyle.Render("••• Bedrock-CLT •••")

	piepanel := lipgloss.NewStyle().Foreground(lipgloss.Color("#555555")).
		Render(" [↑/↓] Scroll | Controles [q] Salir ")
	leftpanel_render := LeftPanelStyle.Render(lipgloss.JoinVertical(lipgloss.Left, c.logger.View(), piepanel))

	rightpanel_render := RightPanelStyle.Render("")

	paneles_render := lipgloss.JoinHorizontal(lipgloss.Top, leftpanel_render, rightpanel_render)

	return header_render + "\n" + paneles_render + "\n"
}
