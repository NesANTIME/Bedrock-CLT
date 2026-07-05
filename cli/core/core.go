package core

import (
	"bedrock-clt_cli/app"
	"bedrock-clt_cli/core/channel"
	"bedrock-clt_cli/core/logger"
	"path/filepath"
)

func Core_TUI() {
	Path_Sock := filepath.Join("/home", "nesantime", "Pruebas", "bedrock-clt_sock.sock")

	Log_Channel := make(chan string)
	StatusServer_Channel := make(chan app.SystemStatus)
	CmdUser_Channel := make(chan string)

	// Listener Logs
	go logger.Logger_Capt("SYSLOG_IDENTIFIER=bedrock-clt_process_BDS", Log_Channel)

	// Send Command
	go channel.ConnectSock(Path_Sock, CmdUser_Channel)

	// Status System

	// TUI
	app.Launch_App(Log_Channel, StatusServer_Channel, CmdUser_Channel)
}
