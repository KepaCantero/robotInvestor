import { useMemo } from "react";
import { AgGridReact } from "ag-grid-react";
import type { ColDef, RowClickedEvent } from "ag-grid-community";
import "ag-grid-community/styles/ag-grid.css";
import "ag-grid-community/styles/ag-theme-quartz.css";
import type { Posicion } from "@/api/tipos";
import { euros, eurosConSigno, numero } from "@/logica/formato";

const AG_ES = {
  noRowsToShow: "No hay posiciones",
  loadingOoo: "Cargando…",
  sortAscending: "Orden ascendente",
  sortDescending: "Orden descendente",
};

export function TablaPosiciones({
  filas,
  seleccion,
  alElegir,
}: {
  filas: Posicion[];
  seleccion: string | null;
  alElegir: (id: string) => void;
}) {
  const columnas = useMemo<ColDef<Posicion>[]>(
    () => [
      { field: "instrumento", headerName: "Instrumento", flex: 2, minWidth: 170 },
      { field: "cantidad", headerName: "Cantidad", type: "rightAligned", valueFormatter: (p) => numero(p.value), minWidth: 100 },
      { field: "precio", headerName: "Precio", type: "rightAligned", valueFormatter: (p) => numero(p.value), minWidth: 95 },
      { field: "valor", headerName: "Valor", type: "rightAligned", valueFormatter: (p) => euros(p.value), minWidth: 100 },
      {
        field: "resultado",
        headerName: "Resultado",
        type: "rightAligned",
        valueFormatter: (p) => eurosConSigno(p.value),
        cellClass: (p) => ((p.value as number) < 0 ? "text-mal" : "text-bien"),
        minWidth: 105,
      },
      {
        headerName: "Rango esperado (H)",
        type: "rightAligned",
        valueGetter: (p) => (p.data ? `${numero(p.data.rangoMin)} – ${numero(p.data.rangoMax)}` : ""),
        minWidth: 160,
      },
      {
        field: "estres",
        headerName: "Caída tipo 2008 (M)",
        type: "rightAligned",
        valueFormatter: (p) => `−${euros(p.value)}`,
        minWidth: 160,
      },
    ],
    [],
  );
  return (
    <div className="ag-theme-quartz w-full" data-testid="tabla-posiciones">
      <AgGridReact<Posicion>
        rowData={filas}
        columnDefs={columnas}
        defaultColDef={{ sortable: true, resizable: true, cellClass: "cifra", flex: 1 }}
        domLayout="autoHeight"
        getRowId={(p) => p.data.id}
        rowSelection="single"
        localeText={AG_ES}
        onRowClicked={(e: RowClickedEvent<Posicion>) => e.data && alElegir(e.data.id)}
        rowClassRules={{ "ag-row-selected": (p) => p.data?.id === seleccion }}
        suppressCellFocus
      />
    </div>
  );
}
