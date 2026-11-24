import math


def convert_regimen(n1: int, d1: float, d2: float, alpha_beta: float) -> dict:
    """Chuyển đổi phác đồ n1 * d1 sang liều phân liều d2 theo BED1 = BED2."""
    if n1 <= 0 or d1 <= 0 or d2 <= 0 or alpha_beta <= 0:
        raise ValueError("Các giá trị n1, d1, d2 và alpha/beta phải lớn hơn 0.")

    bed1 = n1 * d1 * (1.0 + d1 / alpha_beta)
    n2_exact = bed1 / (d2 * (1.0 + d2 / alpha_beta))
    n2_floor = math.floor(n2_exact)
    n2_ceil = math.ceil(n2_exact)

    bed2_floor = n2_floor * d2 * (1.0 + d2 / alpha_beta)
    bed2_ceil = n2_ceil * d2 * (1.0 + d2 / alpha_beta)

    return {
        "n1": n1,
        "d1": d1,
        "d2": d2,
        "alpha_beta": alpha_beta,
        "bed1": bed1,
        "n2_exact": n2_exact,
        "n2_floor": n2_floor,
        "bed2_floor": bed2_floor,
        "n2_ceil": n2_ceil,
        "bed2_ceil": bed2_ceil,
    }