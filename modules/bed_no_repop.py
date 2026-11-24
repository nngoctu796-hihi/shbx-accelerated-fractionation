def calc_single_endpoint(dose_total: float, n: int, d: float, alpha_beta: float) -> dict:
    """Tính BED và EQD2 cho một endpoint/mô cụ thể (không xét tái sinh)."""
    if alpha_beta <= 0:
        raise ValueError("Tỷ số alpha/beta phải lớn hơn 0.")
    bed = dose_total * (1.0 + d / alpha_beta)
    eqd2 = dose_total * ((d + alpha_beta) / (2.0 + alpha_beta))
    return {
        "alpha_beta": alpha_beta,
        "bed": bed,
        "eqd2": eqd2,
        "bed_formula": f"{dose_total:g} * (1 + {d:g} / {alpha_beta:g}) = {bed:.4f}",
        "eqd2_formula": f"{dose_total:g} * (({d:g} + {alpha_beta:g}) / (2 + {alpha_beta:g})) = {eqd2:.4f}",
    }


def calc_bed_no_repop(
    n: int,
    d: float,
    ab_tumor: float,
    ab_early: float = 10.0,
    ab_late: float = 3.0,
    d_total_input: float | None = None,
) -> dict:
    """Tính BED & EQD2 không tái sinh cho mô bướu, mô lành sớm và mô lành muộn."""
    if n <= 0:
        raise ValueError("Số phân liều (n) phải là số nguyên dương.")
    if d <= 0:
        raise ValueError("Liều mỗi phân liều (d) phải lớn hơn 0.")

    computed_d_total = n * d
    consistency_warning = None
    if d_total_input is not None and abs(d_total_input - computed_d_total) > 1e-6:
        consistency_warning = (
            f"Tổng liều nhập ({d_total_input:g} Gy) khác với n × d = {computed_d_total:g} Gy. "
            f"Hệ thống đang dùng tổng liều tính theo n × d = {computed_d_total:g} Gy."
        )

    dose_total = computed_d_total

    return {
        "n": n,
        "d": d,
        "dose_total": dose_total,
        "consistency_warning": consistency_warning,
        "tumor": calc_single_endpoint(dose_total, n, d, ab_tumor),
        "early": calc_single_endpoint(dose_total, n, d, ab_early),
        "late": calc_single_endpoint(dose_total, n, d, ab_late),
    }