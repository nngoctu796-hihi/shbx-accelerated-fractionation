import math


def repair_schedule(
    n_p: int,
    d_p: float,
    n_e: int,
    d_e: float,
    alpha_beta: float = 10.0,
) -> dict:
    """Tính liều hiệu chỉnh d_c và số phân liều hiệu chỉnh n_c theo ký hiệu p, e, c."""
    if n_p <= 0 or d_p <= 0 or alpha_beta <= 0:
        raise ValueError("n_p, d_p và alpha/beta phải lớn hơn 0.")
    if n_e < 0 or d_e < 0:
        raise ValueError("n_e và d_e không được âm.")

    d_p_total = n_p * d_p
    d_e_total = n_e * d_e
    d_c_total = d_p_total - d_e_total

    if d_c_total <= 0:
        raise ValueError("Tổng liều còn lại D_c = D_p - D_e phải lớn hơn 0.")

    numerator = d_p_total * d_p - d_e_total * d_e
    d_c = numerator / d_c_total
    if d_c <= 0:
        raise ValueError("Liều hiệu chỉnh d_c tính ra không dương, hãy kiểm tra lại số liệu.")

    n_c_exact = d_c_total / d_c
    n_c_round = round(n_c_exact)

    bed_plan = d_p_total * (1.0 + d_p / alpha_beta)
    bed_actual_after_repair = (
        d_e_total * (1.0 + d_e / alpha_beta)
        + (n_c_round * d_c) * (1.0 + d_c / alpha_beta)
    )

    return {
        "n_p": n_p,
        "d_p": d_p,
        "d_p_total": d_p_total,
        "n_e": n_e,
        "d_e": d_e,
        "d_e_total": d_e_total,
        "d_c_total": d_c_total,
        "d_c": d_c,
        "n_c_exact": n_c_exact,
        "n_c_round": n_c_round,
        "bed_plan": bed_plan,
        "bed_actual_after_repair": bed_actual_after_repair,
    }