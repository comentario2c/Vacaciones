export interface Vacaciones {
    RutTrabajador: string;
    FechaInicio: string;
    FechaFin: string;
    DiasTomados: number;
    Observaciones: string;
}

export interface VacacionesEditar {
    ID_Movimiento: number;
    RutTrabajador: string;
    FechaInicio: string;
    FechaFin: string;
    DiasTomados: number;
    Observaciones?: string;
}