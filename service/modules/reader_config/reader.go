package readerconfig

import (
	"encoding/json"
	"log/slog"
	"os"

	"github.com/BurntSushi/toml"
)

// Estructuras de archivo de configuracion "toml"
type AppConfigApp struct {
	Configuration_app ConfigurationSectionApp `toml:"Configuracion"`
}

type ConfigurationSectionApp struct {
	Mode_Launch     string `toml:"launch-mode"`
	Args_Launch     string `toml:"launch-argument"`
	Priority_Launch string `toml:"launch-priority"`
}

// Estructuras de archivo de configuracion "json"
type AppConfigServer struct {
	Configuration_server ConfigurationSectionServer `json:"Bedrock-Dedicate-Server"`
}

type ConfigurationSectionServer struct {
	Path    string `json:"Path"`
	Version string `json:"Version"`
}

// Funcion lectora principal
func Reader_Configuration_Files(Path_Config_App string, Path_Config_Server string) (AppConfigApp, AppConfigServer, error) {
	var Config_App AppConfigApp
	var Config_Server AppConfigServer

	bytes_toml, err := os.ReadFile(Path_Config_App)
	if err != nil {
		slog.Error("[B-CLT] - Error al leer archivo de configuracion: ", "error", err)
		return Config_App, Config_Server, err
	}

	err = toml.Unmarshal(bytes_toml, &Config_App)
	if err != nil {
		slog.Error("[B-CLT] - Error al parsear la configuracion: ", "error", err)
		return Config_App, Config_Server, err
	}

	bytes_json, err := os.ReadFile(Path_Config_Server)
	if err != nil {
		slog.Error("[B-CLT] - Error al leer archivo de configuracion daemon: ", "error", err)
		return Config_App, Config_Server, err
	}

	err = json.Unmarshal(bytes_json, &Config_Server)
	if err != nil {
		slog.Error("[B-CLT] - Error al parsear la configuracion daemon: ", "error", err)
		return Config_App, Config_Server, err
	}

	return Config_App, Config_Server, nil
}
