import { CargoRow } from "../api/client";
import { Role } from "../auth/AuthContext";

const KG_TO_LBS = 2.20462;

interface Props {
  rows: CargoRow[];
  role: Role;
}

// Business Rule 3: heaviest → lightest, with Earth always pinned to the
// absolute bottom regardless of weight.
function sortForDisplay(rows: CargoRow[]): CargoRow[] {
  return [...rows].sort((a, b) => {
    const aEarth = a.destination.toLowerCase() === "earth";
    const bEarth = b.destination.toLowerCase() === "earth";
    if (aEarth !== bEarth) return aEarth ? 1 : -1;
    return b.weight_kg - a.weight_kg;
  });
}

// Business Rule 2: Admin sees KG, Standard sees LBS (KG * 2.20462).
function formatWeight(weightKg: number, role: Role): string {
  if (role === "Admin") return `${weightKg} KG`;
  return `${(weightKg * KG_TO_LBS).toFixed(2)} LBS`;
}

export function CargoTable({ rows, role }: Props) {
  const sorted = sortForDisplay(rows);
  return (
    <table>
      <thead>
        <tr>
          <th>Cargo ID</th>
          <th>Origin</th>
          <th>Destination</th>
          <th>Weight</th>
        </tr>
      </thead>
      <tbody>
        {sorted.map((row) => {
          const isEarth = row.destination.toLowerCase() === "earth";
          return (
            <tr key={row.id} className={isEarth ? "earth-row" : undefined}>
              <td>{row.cargo_id}</td>
              <td>{row.origin}</td>
              <td>{row.destination}</td>
              <td>{formatWeight(row.weight_kg, role)}</td>
            </tr>
          );
        })}
      </tbody>
    </table>
  );
}
