package verifyconfig

import (
	readerconfig "bedrock-clt/modules/reader_config"
	"fmt"
	"log/slog"
	"regexp"
	"runtime"
	"strconv"
)

// funciones auxiliares -----------------------------------------------
func aux_randcore(input string) error {
	coresDisponibles := runtime.NumCPU()
	re := regexp.MustCompile(`^([0-9]+)-([0-9]+)$`)
	matches := re.FindStringSubmatch(input)

	if len(matches) != 3 {
		return fmt.Errorf("formato invalido '%s'. Debe ser como '0-3' (ejemplo)", input)
	}

	inicio, _ := strconv.Atoi(matches[1])
	fin, _ := strconv.Atoi(matches[2])

	if inicio > fin {
		return fmt.Errorf("rango ilogico: el core de inicio (%d) es mayor que el de fin (%d)", inicio, fin)
	}

	if fin >= coresDisponibles {
		return fmt.Errorf("rango excede el hardware: solicitaste hasta el core %d, pero el sistema solo tiene %d cores (0-%d)", fin, coresDisponibles, coresDisponibles-1)
	}

	return nil
}

// --------------------------------------------------------------------

func Verify_ConfigApp(Config_App readerconfig.AppConfigApp) ([]string, error) {
	switch Config_App.Configuration_app.Mode_Launch {
	case "taskset":
		err := aux_randcore(Config_App.Configuration_app.Args_Launch)
		if err != nil {
			slog.Error("[B-CLT] - Error: %s", "error", err)
			return nil, err
		}
		return []string{"taskset", "-c", Config_App.Configuration_app.Args_Launch}, nil

	case "numactl":
		return nil, nil
	}

	return nil, fmt.Errorf("ninguna de las opciones de lanzamiento son validas!")
}
