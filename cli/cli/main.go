package main

import (
	"bedrock-clt_cli/app"
	"bedrock-clt_cli/core"
)

func main() {
	LogsChan := make(chan string)

	go core.Capture_Logs(LogsChan)
	app.Launch_App(LogsChan)
}
