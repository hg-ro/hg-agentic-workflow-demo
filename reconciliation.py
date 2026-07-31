import csv
import sys


def reconcile(computed, invoiced, tolerance=0.01):
    gap = computed - invoiced
    verdict = "RECONCILED" if abs(gap) <= tolerance else "DISCREPANCY"
    return verdict, gap


def reconcile_csv(path, tolerance=0.01):
    reconciled_count = 0
    flagged = []

    with open(path, newline="") as f:
        for row in csv.DictReader(f):
            row_id = row.get("id")
            computed_raw = row.get("computed")
            invoiced_raw = row.get("invoiced")

            if not computed_raw or not invoiced_raw:
                flagged.append({
                    "id": row_id,
                    "computed": computed_raw,
                    "invoiced": invoiced_raw,
                    "gap": None,
                    "error": "missing column",
                })
                continue

            try:
                computed = float(computed_raw)
                invoiced = float(invoiced_raw)
            except ValueError:
                flagged.append({
                    "id": row_id,
                    "computed": computed_raw,
                    "invoiced": invoiced_raw,
                    "gap": None,
                    "error": "non-numeric amount",
                })
                continue

            verdict, gap = reconcile(computed, invoiced, tolerance)
            if verdict == "RECONCILED":
                reconciled_count += 1
            else:
                flagged.append({
                    "id": row_id,
                    "computed": computed,
                    "invoiced": invoiced,
                    "gap": gap,
                    "error": None,
                })

    return {
        "reconciled": reconciled_count,
        "flagged": len(flagged),
        "details": flagged,
    }


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"usage: {sys.argv[0]} <path-to-csv> [tolerance]")
        sys.exit(1)

    csv_path = sys.argv[1]
    tol = float(sys.argv[2]) if len(sys.argv) > 2 else 0.01

    summary = reconcile_csv(csv_path, tolerance=tol)
    print(f"reconciled: {summary['reconciled']}")
    print(f"flagged:    {summary['flagged']}")
    for detail in summary["details"]:
        print(f"  {detail}")
