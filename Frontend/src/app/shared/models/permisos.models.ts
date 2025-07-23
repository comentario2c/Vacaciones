export interface Permiso {
  ID_Permiso: number;
  RutTrabajador: string;
  NombreTrabajador: string;
  FechaInicio: string;
  FechaFin: string;
  DiasTomados: number;
  ConCargoVacaciones: boolean;
  Motivo: string;
}