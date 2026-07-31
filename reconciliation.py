def reconcile(computed, invoiced, tolerance=0.01):
    gap = computed - invoiced
    verdict = "RECONCILED" if abs(gap) <= tolerance else "DISCREPANCY"
    return verdict, gap
