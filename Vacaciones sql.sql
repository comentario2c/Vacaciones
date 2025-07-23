# -------------------------------------- Tablas --------------------------------------
CREATE TABLE `Trabajador` (
  `RutTrabajador` varchar(9) PRIMARY KEY, # Formato sin puntos ni guion
  `Nombre` varchar(50), 
  `FechaContrato` date, # Dato que se almacenará solo para tener la información a mano
  `AnosRestantes` int, # Cantidad de años que faltan para obtener el primer dia progresivo
  `Cargo` varchar(100), # Cargo que desempeña dentro de la empresa
  `DiasProgresivosBase` INT DEFAULT 0, # Días progresivos acumulados antes de ingresar al sistema
  `DiasPendientesBase` INT DEFAULT 0, # Cantidad de dias pendientes antes de ser ingresado al sistema
  `Estado` boolean # Para evitar eliminar los registros en cascada solo se oculta cambiando el estado a false
);

CREATE TABLE `MovimientoVacaciones` (
  `ID_Movimiento` int PRIMARY KEY auto_increment,
  `RutTrabajador` varchar(9),
  `FechaInicio` date,
  `FechaFin` date,
  `DiasTomados` int, # Cantidad de dias tomados desde la fecha de inicio de las vacaciones
  `Observaciones` varchar(255) 
);

CREATE TABLE `Permisos` (
  `ID_Permiso` int PRIMARY KEY auto_increment,
  `RutTrabajador` varchar(9),
  `FechaInicio` date,
  `FechaFin` date,
  `DiasTomados` int, # Cantidad de dias tomados desde la fecha de inicio del permiso
  `ConCargoVacaciones` boolean, # Se aplica un descuento en el saldo de vacaciones? Si / No
  `Motivo` varchar(255)
);

CREATE TABLE `ConfiguracionVacaciones`(
  `Clave` VARCHAR(50) PRIMARY KEY,
  `Valor` VARCHAR(100),
  `Descripcion` TEXT
);

CREATE TABLE `FeriadosNacionales` (
  `ID_FeriadosNacionales` INT PRIMARY KEY AUTO_INCREMENT,
  `Fecha` DATE UNIQUE,
  `Nombre` VARCHAR(100)
);

CREATE TABLE `LogsAuditoria` (
  `ID_Log` INT PRIMARY KEY AUTO_INCREMENT,
  `Tabla` VARCHAR(50),             -- Ej: 'Trabajador', 'Permisos'
  `Operacion` ENUM('INSERT', 'UPDATE', 'DELETE'), 
  `RutTrabajador` VARCHAR(9),      -- Quién fue afectado (si aplica)
  `CampoAfectado` VARCHAR(50),     -- Ej: 'Cargo', 'Estado', etc.
  `ValorAnterior` TEXT, 
  `ValorNuevo` TEXT, 
  `FechaHora` TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE `Usuario` (
  `Email` VARCHAR(50) PRIMARY KEY,
  `Rol` VARCHAR(30),
  `PasswordHash` VARCHAR(100) # Contraseñas deben de guardarse hasheadas
);

ALTER TABLE `MovimientoVacaciones` ADD FOREIGN KEY (`RutTrabajador`) REFERENCES `Trabajador` (`RutTrabajador`);

ALTER TABLE `Permisos` ADD FOREIGN KEY (`RutTrabajador`) REFERENCES `Trabajador` (`RutTrabajador`);

select * from trabajador
# -------------------------------------- Proteger eliminar y Actualizar cascada --------------------------------------
# Consultar los nombres de las claves foraneas
SELECT CONSTRAINT_NAME 
FROM information_schema.KEY_COLUMN_USAGE
WHERE TABLE_NAME = 'MovimientoVacaciones' AND CONSTRAINT_SCHEMA = 'dbname' AND REFERENCED_TABLE_NAME IS NOT NULL;


# Eliminar claves foranias
ALTER TABLE MovimientoVacaciones DROP FOREIGN KEY MovimientoVacaciones_ibfk_1;
ALTER TABLE Permisos DROP FOREIGN KEY Permisos_ibfk_1;

# delete protect y update cascade
ALTER TABLE MovimientoVacaciones
  ADD CONSTRAINT FK_Movimiento_Trabajador
  FOREIGN KEY (RutTrabajador)
  REFERENCES Trabajador(RutTrabajador)
  ON DELETE RESTRICT ON UPDATE CASCADE;

# delete protect y update cascade
ALTER TABLE Permisos
  ADD CONSTRAINT FK_Permiso_Trabajador
  FOREIGN KEY (RutTrabajador)
  REFERENCES Trabajador(RutTrabajador)
  ON DELETE RESTRICT ON UPDATE CASCADE;

# -------------------------------------- Índices --------------------------------------

# Filtrar trabajadores activos
CREATE INDEX idx_estado_trabajador ON Trabajador(Estado);

# Buscar vacaciones de un trabajador por fechas
CREATE INDEX idx_vacaciones_rut_fecha ON MovimientoVacaciones(RutTrabajador, FechaInicio);

# Buscar permisos de un trabajador por fechas
CREATE INDEX idx_permisos_rut_fecha ON Permisos(RutTrabajador, FechaInicio);

# Buscar permisos a cuenta de vacaciones
CREATE INDEX idx_permiso_vacaciones ON Permisos(ConCargoVacaciones);

# -------------------------------------- Triggers --------------------------------------

# Cambios en "Estado" del trabajador
DELIMITER //
CREATE TRIGGER trg_trabajador_estado_update
AFTER UPDATE ON Trabajador
FOR EACH ROW
BEGIN
  IF OLD.Estado <> NEW.Estado THEN
    INSERT INTO LogsAuditoria (
      Tabla, Operacion, RutTrabajador, CampoAfectado, ValorAnterior, ValorNuevo
    ) VALUES (
      'Trabajador', 'UPDATE', OLD.RutTrabajador, 'Estado',
      IF(OLD.Estado, 'Activo', 'Inactivo'),
      IF(NEW.Estado, 'Activo', 'Inactivo')
    );
  END IF;
END;
//
DELIMITER ;

# -------------------------------------- INSERT INTO --------------------------------------
# Ingresar desde el backend
INSERT INTO ConfiguracionVacaciones (Clave, Valor, Descripcion) VALUES
  ('DíasBaseAnuales', '15', 'Cantidad de días base por año trabajado'),
  ('AñosParaPrimerProgresivo', '10', 'Años de cotización previos para tener derecho a progresivos'),
  ('AñosParaProgresivoEmpresa', '13', 'Años en la empresa si no ha trabajado antes'),
  ('PeriodoEntreProgresivos', '3', 'Cada cuántos años se suma un día progresivo'),
  ('AnioInicioCalculoPendientes', '2025', 'Año desde el cual se comienzan a calcular los días pendientes');

Select * from configuracionvacaciones
# -------------------------------------- Vistas --------------------------------------
CREATE OR REPLACE VIEW PermisosListar AS
SELECT
	p.ID_Permiso,
    p.RutTrabajador,
    t.Nombre AS NombreTrabajador,
    p.FechaInicio,
    p.FechaFin,
    p.DiasTomados,
    p.ConCargoVacaciones,
    p.Motivo
FROM Permisos p
JOIN Trabajador t ON p.RutTrabajador = t.RutTrabajador;

CREATE OR REPLACE VIEW VacacionesListar AS
SELECT 
  mv.ID_Movimiento,
  mv.RutTrabajador,
  t.Nombre AS NombreTrabajador,
  mv.FechaInicio,
  mv.FechaFin,
  mv.DiasTomados,
  mv.Observaciones
FROM MovimientoVacaciones mv
JOIN Trabajador t ON mv.RutTrabajador = t.RutTrabajador;

Drop table configuracionvacaciones;
Drop table feriadosnacionales;
Drop table logsauditoria;
Drop table movimientovacaciones;
Drop table permisos;
Drop table trabajador;
Drop table usuario;
