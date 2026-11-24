def calc_endpoint_repop(
    label: str,
    n: int,
    d: float,
    alpha_beta: float,
    total_time: float,
    kickoff_time: float,
    k_per_day: float,
    d_prolif_per_day: float = 0.0,
    ref_time_t: float | None = None,
) -> dict:
    """Tính BED hiệu chỉnh tái sinh (mô hình K) và EQD2 hiệu chỉnh thời gian (mô hình D_prolif)."""
    if alpha_beta <= 0:
        raise ValueError(f"{label}: Tỷ số alpha/beta phải lớn hơn 0.")
    if total_time < 0 or kickoff_time < 0:
        raise ValueError(f"{label}: Thời gian T và Tk không được âm.")
    if k_per_day < 0 or d_prolif_per_day < 0:
        raise ValueError(f"{label}: Hệ số tái sinh K và D_prolif không được âm.")

    dose_total = n * d
    bed_0 = dose_total * (1.0 + d / alpha_beta)
    eqd2_0 = dose_total * ((d + alpha_beta) / (2.0 + alpha_beta))

    effective_days = max(0.0, total_time - kickoff_time)
    repop_loss_bed = k_per_day * effective_days
    bed_corrected = bed_0 - repop_loss_bed

    # Mô hình EQD2_T = EQD2_t - D_prolif * delta_t_effective (mặc định t = 0 nếu không nhập t)
    t_0 = 0.0 if ref_time_t is None else ref_time_t
    if t_0 < 0:
        raise ValueError(f"{label}: Thời điểm tham chiếu t không được âm.")
    delta_t_eff = max(0.0, total_time - kickoff_time) - max(0.0, t_0 - kickoff_time)
    repop_loss_eqd2 = d_prolif_per_day * delta_t_eff
    eqd2_corrected = eqd2_0 - repop_loss_eqd2

    return {
        "label": label,
        "alpha_beta": alpha_beta,
        "dose_total": dose_total,
        "bed_0": bed_0,
        "effective_days": effective_days,
        "repop_loss_bed": repop_loss_bed,
        "bed_corrected": bed_corrected,
        "eqd2_0": eqd2_0,
        "delta_t_eff": delta_t_eff,
        "repop_loss_eqd2": repop_loss_eqd2,
        "eqd2_corrected": eqd2_corrected,
        "bed_corr_formula": (
            f"{bed_0:.4f} - {k_per_day:g} * max(0, {total_time:g} - {kickoff_time:g}) "
            f"= {bed_0:.4f} - {repop_loss_bed:.4f} = {bed_corrected:.4f}"
        ),
        "eqd2_corr_formula": (
            f"{eqd2_0:.4f} - {d_prolif_per_day:g} * {delta_t_eff:g} = {eqd2_corrected:.4f}"
        ),
    }


def calc_bed_repop(
    n: int,
    d: float,
    total_time: float,
    tumor_cfg: dict,
    early_cfg: dict,
    late_cfg: dict,
) -> dict:
    """Tính toán tái sinh cho 3 nhóm: Mô bướu, Mô lành đáp ứng sớm, Mô lành đáp ứng muộn."""
    if n <= 0:
        raise ValueError("Số phân liều (n) phải là số nguyên dương.")
    if d <= 0:
        raise ValueError("Liều mỗi phân liều (d) phải lớn hơn 0.")

    return {
        "n": n,
        "d": d,
        "total_time": total_time,
        "tumor": calc_endpoint_repop(
            "Mô bướu (Tumor)",
            n,
            d,
            tumor_cfg["ab"],
            total_time,
            tumor_cfg["tk"],
            tumor_cfg["k"],
            tumor_cfg["d_prolif"],
        ),
        "early": calc_endpoint_repop(
            "Mô lành đáp ứng sớm (Early)",
            n,
            d,
            early_cfg["ab"],
            total_time,
            early_cfg["tk"],
            early_cfg["k"],
            early_cfg["d_prolif"],
        ),
        "late": calc_endpoint_repop(
            "Mô lành đáp ứng muộn (Late)",
            n,
            d,
            late_cfg["ab"],
            total_time,
            late_cfg["tk"],
            late_cfg["k"],
            late_cfg["d_prolif"],
        ),
    }