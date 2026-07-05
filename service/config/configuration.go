package config

import (
	readerconfig "bedrock-clt/modules/reader_config"
	verifyconfig "bedrock-clt/modules/verify_config"
	"log/slog"
	"path/filepath"
)

// Estructura principal de configuracion
type Configuration_App struct {
	Path_server    string
	Launch_command []string
	Path_sock      string
}

func Load_Configuration() (Configuration_App, error) {
	Path_Configuration_App := filepath.Join("/home", "nesantime", "Pruebas", "config.toml")
	Path_Sock := filepath.Join("/home", "nesantime", "Pruebas", "bedrock-clt_sock.sock")
	Path_Configuration_Server := filepath.Join("/home", "nesantime", "Pruebas", "configuration.json")

	Config_App, Config_Server, err := readerconfig.Reader_Configuration_Files(Path_Configuration_App, Path_Configuration_Server)
	if err != nil {
		slog.Error("[B-CLT] - Error al cargar la configuracion: ", "error", err)
		return Configuration_App{}, err
	}

	// Verificacion de seguridad -----------

	launch_command, err := verifyconfig.Verify_ConfigApp(Config_App)
	if err != nil {
		slog.Error("[B-CLT] - Error: ", "error", err)
		return Configuration_App{}, err
	}

	// -------------------------------------

	return Configuration_App{
		Path_server:    Config_Server.Configuration_server.Path,
		Launch_command: launch_command,
		Path_sock:      Path_Sock,
	}, nil
}
