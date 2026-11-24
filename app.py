from flask import Flask, render_template_string, request
from modules.bed_no_repop import calc_bed_no_repop
from modules.bed_repop import calc_bed_repop
from modules.regimen_convert import convert_regimen
from modules.schedule_repair import repair_schedule

app = Flask(__name__)

BASE_HTML = """
<!doctype html>
<html lang="vi">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Accelerated Fractionation — LQ & BED Calculator</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Be+Vietnam+Pro:wght@400;500;600;700&display=swap" rel="stylesheet">
  <script>
    window.MathJax = {
      tex: { inlineMath: [['$', '$'], ['\\\\(', '\\\\)']] }
    };
  </script>
  <script defer src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
  <style>
    :root {
      --bg: #f1f5f9;
      --surface: #ffffff;
      --primary: #1d4ed8;
      --primary-dark: #0f294a;
      --primary-soft: #eff6ff;
      --border: #e2e8f0;
      --text: #0f172a;
      --muted: #475569;
      --accent: #0284c7;
      --warn-bg: #fffbeb;
      --warn-border: #f59e0b;
      --err-bg: #fef2f2;
      --err-border: #dc2626;
    }
    * { box-sizing: border-box; }
    body {
      margin: 0;
      font-family: 'Be Vietnam Pro', -apple-system, BlinkMacSystemFont, sans-serif;
      background: var(--bg);
      color: var(--text);
      line-height: 1.6;
    }
    header {
      background: linear-gradient(135deg, var(--primary-dark) 0%, var(--primary) 100%);
      color: #fff;
      padding: 28px 20px 24px;
      box-shadow: 0 4px 16px rgba(15, 41, 74, 0.14);
    }
    .header-inner, .container {
      max-width: 1020px;
      margin: 0 auto;
    }
    .badge {
      display: inline-block;
      background: rgba(255, 255, 255, 0.16);
      border: 1px solid rgba(255, 255, 255, 0.28);
      padding: 3px 10px;
      border-radius: 999px;
      font-size: 12px;
      font-weight: 600;
      letter-spacing: 0.3px;
      margin-bottom: 8px;
    }
    header h1 {
      margin: 0 0 6px;
      font-size: 23px;
      font-weight: 700;
    }
    header p {
      margin: 0;
      font-size: 14px;
      color: #dbeafe;
    }
    .nav-wrap {
      background: var(--surface);
      border-bottom: 1px solid var(--border);
      position: sticky;
      top: 0;
      z-index: 20;
    }
    nav {
      max-width: 1020px;
      margin: 0 auto;
      padding: 10px 20px;
      display: flex;
      gap: 8px;
      flex-wrap: wrap;
    }
    nav a {
      padding: 8px 14px;
      border-radius: 8px;
      text-decoration: none;
      font-size: 13.5px;
      font-weight: 600;
      color: var(--muted);
      transition: all 0.15s ease;
    }
    nav a:hover {
      background: var(--primary-soft);
      color: var(--primary);
    }
    nav a.active {
      background: var(--primary);
      color: #fff;
      box-shadow: 0 2px 6px rgba(29, 78, 216, 0.25);
    }
    .container {
      padding: 24px 20px 48px;
    }
    .card {
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: 14px;
      padding: 24px;
      box-shadow: 0 2px 10px rgba(15, 23, 42, 0.04);
    }
    .card-header {
      border-bottom: 1px solid var(--border);
      padding-bottom: 14px;
      margin-bottom: 20px;
    }
    .card-header h2 {
      margin: 0 0 4px;
      font-size: 19px;
      color: var(--primary-dark);
    }
    .subtitle {
      margin: 0;
      font-size: 13.5px;
      color: var(--muted);
    }
    .grid-2 {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
      gap: 16px;
    }
    .grid-3 {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
      gap: 16px;
    }
    .sub-panel {
      background: #f8fafc;
      border: 1px solid var(--border);
      border-radius: 10px;
      padding: 14px 16px;
    }
    .sub-panel h4 {
      margin: 0 0 10px;
      font-size: 14.5px;
      color: var(--primary-dark);
      border-bottom: 1px dashed #cbd5e1;
      padding-bottom: 6px;
    }
    .field {
      margin-bottom: 12px;
    }
    .field:last-child {
      margin-bottom: 0;
    }
    label {
      display: block;
      font-size: 13px;
      font-weight: 600;
      color: #334155;
      margin-bottom: 4px;
    }
    input {
      width: 100%;
      padding: 9px 11px;
      border: 1px solid #cbd5e1;
      border-radius: 8px;
      font-family: inherit;
      font-size: 14px;
      background: #fff;
      transition: border-color 0.15s, box-shadow 0.15s;
    }
    input:focus {
      outline: none;
      border-color: var(--primary);
      box-shadow: 0 0 0 3px rgba(29, 78, 216, 0.12);
    }
    .btn-row {
      display: flex;
      gap: 10px;
      flex-wrap: wrap;
      margin-top: 20px;
    }
    button.btn-primary {
      padding: 10px 20px;
      background: var(--primary);
      color: #fff;
      border: none;
      border-radius: 8px;
      font-family: inherit;
      font-size: 14px;
      font-weight: 600;
      cursor: pointer;
      box-shadow: 0 2px 6px rgba(29, 78, 216, 0.25);
    }
    button.btn-primary:hover {
      background: #1e40af;
    }
    a.btn-secondary {
      padding: 10px 16px;
      background: #f1f5f9;
      color: #334155;
      border: 1px solid #cbd5e1;
      border-radius: 8px;
      text-decoration: none;
      font-size: 13.5px;
      font-weight: 600;
    }
    a.btn-secondary:hover {
      background: #e2e8f0;
    }
    .result-section {
      margin-top: 24px;
      padding-top: 20px;
      border-top: 2px solid var(--border);
    }
    .kpi-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(190px, 1fr));
      gap: 12px;
      margin-bottom: 18px;
    }
    .kpi {
      background: var(--primary-soft);
      border: 1px solid #bfdbfe;
      border-radius: 10px;
      padding: 12px 14px;
    }
    .kpi .kpi-label {
      font-size: 12px;
      font-weight: 600;
      color: #1e40af;
      text-transform: uppercase;
      letter-spacing: 0.3px;
    }
    .kpi .kpi-value {
      font-size: 20px;
      font-weight: 700;
      color: var(--primary-dark);
      margin-top: 2px;
    }
    table {
      width: 100%;
      border-collapse: collapse;
      margin-top: 10px;
      font-size: 14px;
      border-radius: 8px;
      overflow: hidden;
    }
    th, td {
      border: 1px solid var(--border);
      padding: 10px 12px;
      text-align: left;
    }
    th {
      background: #f8fafc;
      color: var(--primary-dark);
      font-weight: 700;
    }
    tr:nth-child(even) td {
      background: #fcfdff;
    }
    .formula-box {
      background: #f8fafc;
      border: 1px solid var(--border);
      border-radius: 10px;
      padding: 14px 16px;
      margin-top: 14px;
      font-size: 13.5px;
    }
    .formula-box h4 {
      margin: 0 0 8px;
      font-size: 14px;
      color: var(--primary-dark);
    }
    .formula-box ul {
      margin: 0;
      padding-left: 18px;
    }
    .note {
      margin-top: 14px;
      padding: 12px 14px;
      background: var(--warn-bg);
      border-left: 4px solid var(--warn-border);
      border-radius: 6px;
      font-size: 13.5px;
      color: #78350f;
    }
    .error-box {
      margin-top: 18px;
      padding: 12px 14px;
      background: var(--err-bg);
      border-left: 4px solid var(--err-border);
      border-radius: 6px;
      color: #991b1b;
      font-size: 14px;
    }
    code {
      background: #e2e8f0;
      padding: 2px 6px;
      border-radius: 4px;
      font-size: 13px;
    }
    footer {
      max-width: 1020px;
      margin: 0 auto;
      padding: 0 20px 28px;
      text-align: center;
      font-size: 12.5px;
      color: var(--muted);
    }
  </style>
</head>
<body>
  <header>
    <div class="header-inner">
      <div class="badge">RADIOBIOLOGY · LINEAR-QUADRATIC MODEL & BED</div>
      <h1>Phân liều tăng tốc (Accelerated Fractionation) & Mô hình hóa BED</h1>
      <p>Hệ thống tính toán Liều hiệu dụng sinh học, Chuyển đổi phác đồ và Sửa sai phân liều trong xạ trị</p>
    </div>
  </header>

  <div class="nav-wrap">
    <nav>
      <a href="/" class="{{ 'active' if active_page == 'home' else '' }}">Tổng quan & Lý thuyết</a>
      <a href="/module1" class="{{ 'active' if active_page == 'm1' else '' }}">Module 1: BED (Không tái sinh)</a>
      <a href="/module2" class="{{ 'active' if active_page == 'm2' else '' }}">Module 2: BED (Có tái sinh)</a>
      <a href="/module3" class="{{ 'active' if active_page == 'm3' else '' }}">Module 3: Chuyển đổi phác đồ</a>
      <a href="/module4" class="{{ 'active' if active_page == 'm4' else '' }}">Module 4: Sửa sai phân liều</a>
      <a href="/references" class="{{ 'active' if active_page == 'ref' else '' }}">Công thức & Tham số</a>
    </nav>
  </div>

  <div class="container">
    <div class="card">
      {{ content | safe }}
    </div>
  </div>

  <footer>
    Công cụ mô phỏng học thuật môn Sinh học Bức xạ — Khoa Vật lý – Vật lý Kỹ thuật (Chuyên ngành Vật lý Y khoa)
  </footer>
</body>
</html>
"""


@app.route("/")
@app.route("/home")
def home():
    content = """
    <div class="card-header">
      <h2>Tổng quan đề tài & Khung liên kết 4 Modules</h2>
      <p class="subtitle">Mô hình hóa tác dụng sinh học của phân liều xạ trị dựa trên phương trình Tuyến tính – Bậc hai (LQ)</p>
    </div>

    <p>
      Trong xạ trị, cùng một tổng liều vật lý $D = n \\cdot d$ nhưng thay đổi số phân liều $n$, liều mỗi phân liều $d$ và tổng thời gian điều trị $T$
      sẽ tạo ra đáp ứng sinh học khác nhau trên <strong>mô bướu</strong> và <strong>mô lành</strong>. Website triển khai 4 module tính toán thống nhất theo bài giảng và y văn Sinh học bức xạ:
    </p>

    <div class="grid-2" style="margin-top:16px;">
      <div class="sub-panel">
        <h4>Module 1 · BED không tính đến tái sinh</h4>
        <p style="margin:0;font-size:13.5px;">Tính đồng thời $\\text{BED}$ và $\\text{EQD2}$ cho mô bướu, mô lành đáp ứng sớm và mô lành đáp ứng muộn theo công thức $\\text{BED} = nd\\left(1 + \\frac{d}{\\alpha/\\beta}\\right)$.</p>
      </div>
      <div class="sub-panel">
        <h4>Module 2 · BED có tính đến tái sinh</h4>
        <p style="margin:0;font-size:13.5px;">Hiệu chỉnh yếu tố thời gian xạ $T$, thời gian trì hoãn $T_{\\text{trì hoãn}}$ và hệ số tái sinh $K$: $\\text{BED} = \\text{BED}_0 - K\\max(0, T - T_{\\text{trì hoãn}})$.</p>
      </div>
      <div class="sub-panel">
        <h4>Module 3 · Chuyển đổi phác đồ điều trị</h4>
        <p style="margin:0;font-size:13.5px;">Chuyển đổi giữa các mức phân liều theo nguyên tắc $\\text{BED}_1 = \\text{BED}_2$, hiển thị cả số phân liều lý thuyết và phương án làm tròn nguyên.</p>
      </div>
      <div class="sub-panel">
        <h4>Module 4 · Sửa sai phân liều</h4>
        <p style="margin:0;font-size:13.5px;">Xác định tổng liều còn lại $D_c = D_p - D_e$, liều hiệu chỉnh $d_c = \\frac{D_p d_p - D_e d_e}{D_p - D_e}$ và số phân liều hiệu chỉnh $n_c$.</p>
      </div>
    </div>

    <div class="formula-box">
      <h4>Nền tảng sinh học & toán học cốt lõi</h4>
      <ul>
        <li><strong>5 chữ R trong sinh học xạ trị:</strong> <em>Repair</em> (sửa chữa), <em>Redistribution</em> (tái phân bố chu kỳ tế bào), <em>Reoxygenation</em> (tái oxy hóa), <em>Repopulation</em> (tái sinh), <em>Radiosensitivity</em> (độ nhạy xạ nội tại).</li>
        <li><strong>Tỷ lệ sống sót tế bào (LQ):</strong> $S(D) = e^{-(\\alpha D + \\beta D^2)}$, với $n$ phân liều bằng nhau: $S_n = e^{-n(\\alpha d + \\beta d^2)}$.</li>
        <li><strong>Liều hiệu dụng sinh học:</strong> $\\text{BED} = -\\frac{\\ln S}{\\alpha} = nd\\left(1 + \\frac{d}{\\alpha/\\beta}\\right)$.</li>
      </ul>
    </div>

    <div class="note">
      <strong>Lưu ý phạm vi học thuật:</strong> Công cụ được xây dựng phục vụ học tập, kiểm chứng bài toán và nghiên cứu mô hình sinh học bức xạ; không dùng để kê đơn hay quyết định điều trị lâm sàng.
    </div>
    """
    return render_template_string(BASE_HTML, content=content, active_page="home")


@app.route("/references")
def references():
    content = """
    <div class="card-header">
      <h2>Hệ thống công thức, Bảng tham số & Tài liệu tham khảo</h2>
      <p class="subtitle">Chuẩn hóa ký hiệu theo bài giảng trên lớp, Hall & Giaccia và Basic Clinical Radiobiology</p>
    </div>

    <table>
      <tr>
        <th>Module / Đại lượng</th>
        <th>Phương trình toán học</th>
        <th>Ký hiệu & Đơn vị</th>
      </tr>
      <tr>
        <td>BED cơ bản (Module 1)</td>
        <td>$\\text{BED} = nd\\left(1 + \\frac{d}{\\alpha/\\beta}\\right)$</td>
        <td>$n$: số phân liều; $d$: liều/phân liều (Gy); $\\alpha/\\beta$ (Gy)</td>
      </tr>
      <tr>
        <td>Liều tương đương 2 Gy</td>
        <td>$\\text{EQD2} = D \\cdot \\frac{d + \\alpha/\\beta}{2 + \\alpha/\\beta}$</td>
        <td>$D = n \\cdot d$: tổng liều vật lý (Gy)</td>
      </tr>
      <tr>
        <td>BED có tái sinh (Module 2)</td>
        <td>$\\text{BED} = \\text{BED}_0 - K \\cdot \\max(0, T - T_{\\text{trì hoãn}})$</td>
        <td>$T, T_{\\text{trì hoãn}}$ (ngày); $K$ (Gy/ngày)</td>
      </tr>
      <tr>
        <td>Chuyển đổi phác đồ (Module 3)</td>
        <td>$n_1 d_1\\left(1 + \\frac{d_1}{\\alpha/\\beta}\\right) = n_2 d_2\\left(1 + \\frac{d_2}{\\alpha/\\beta}\\right)$</td>
        <td>$n_2$ làm tròn số nguyên và kiểm tra lại $\\text{BED}_2$</td>
      </tr>
      <tr>
        <td>Sửa sai phân liều (Module 4)</td>
        <td>$D_c = D_p - D_e \\quad ; \\quad d_c = \\frac{D_p d_p - D_e d_e}{D_p - D_e}$</td>
        <td>$p$: kế hoạch; $e$: xạ sai; $c$: hiệu chỉnh; $n_c = D_c / d_c$</td>
      </tr>
    </table>

    <h4 style="margin-top:20px;margin-bottom:8px;color:#0f294a;">Bảng tham số minh họa & nguyên tắc kiểm soát học thuật</h4>
    <table>
      <tr>
        <th>Đối tượng mô / Endpoint</th>
        <th>Giá trị $\\alpha/\\beta$ minh họa</th>
        <th>Đặc điểm sinh học cần lưu ý</th>
      </tr>
      <tr>
        <td>Mô bướu (đáp ứng sớm)</td>
        <td>$10\\text{ Gy}$ (hoặc $4\\text{–}4{,}5\\text{ Gy}$ với u vú)</td>
        <td>Có thể xuất hiện tái sinh nhanh sau thời gian trễ $T_{\\text{trì hoãn}} \\approx 21\\text{–}28\\text{ ngày}$</td>
      </tr>
      <tr>
        <td>Mô lành đáp ứng sớm</td>
        <td>$10\\text{ Gy}$ (niêm mạc, da)</td>
        <td>Có khả năng tái sinh trong liệu trình; không mặc định $K = 0$ cho mọi mô lành</td>
      </tr>
      <tr>
        <td>Mô lành đáp ứng muộn</td>
        <td>$3\\text{ Gy}$ (tủy sống, xương, mô liên kết)</td>
        <td>Nhạy mạnh với liều mỗi phân liều $d$; không so sánh trực tiếp BED khác $\\alpha/\\beta$</td>
      </tr>
    </table>

    <div class="formula-box">
      <h4>Tài liệu tham khảo</h4>
      <ul>
        <li>Slide bài giảng & ghi chép môn Sinh học Bức xạ (Chương Liễu hiệu dụng sinh học & Phân liều).</li>
        <li>Hall EJ, Giaccia AJ — <em>Radiobiology for the Radiologist</em> (Chương 3 & Chương 23).</li>
        <li>Joiner MC, van der Kogel AJ — <em>Basic Clinical Radiobiology</em> (Chương 9–12 & Chương 16).</li>
      </ul>
    </div>
    """
    return render_template_string(BASE_HTML, content=content, active_page="ref")


@app.route("/module1", methods=["GET", "POST"])
def module1():
    n, d = 30, 2.0
    ab_tumor, ab_early, ab_late = 10.0, 10.0, 3.0
    d_total_in = 60.0
    res = None
    error_msg = None

    if request.method == "POST":
        try:
            n = int(request.form["n"])
            d = float(request.form["d"])
            ab_tumor = float(request.form["ab_tumor"])
            ab_early = float(request.form["ab_early"])
            ab_late = float(request.form["ab_late"])
            raw_d_total = request.form.get("d_total", "").strip()
            d_total_in = float(raw_d_total) if raw_d_total else n * d
            res = calc_bed_no_repop(n, d, ab_tumor, ab_early, ab_late, d_total_in)
        except ValueError as exc:
            error_msg = str(exc)

    detail_html = ""
    if error_msg:
        detail_html = f'<div class="error-box"><strong>Lỗi dữ liệu:</strong> {error_msg}</div>'
    elif res:
        warn_html = ""
        if res["consistency_warning"]:
            warn_html = f'<div class="note"><strong>Lưu ý kiểm tra $D = n \\cdot d$:</strong> {res["consistency_warning"]}</div>'

        detail_html = f"""
        <div class="result-section">
          {warn_html}
          <div class="kpi-grid">
            <div class="kpi">
              <div class="kpi-label">Tổng liều vật lý (D)</div>
              <div class="kpi-value">{res['dose_total']:.2f} Gy</div>
            </div>
            <div class="kpi">
              <div class="kpi-label">BED Mô bướu</div>
              <div class="kpi-value">{res['tumor']['bed']:.2f} Gy</div>
            </div>
            <div class="kpi">
              <div class="kpi-label">BED Mô lành sớm</div>
              <div class="kpi-value">{res['early']['bed']:.2f} Gy</div>
            </div>
            <div class="kpi">
              <div class="kpi-label">BED Mô lành muộn</div>
              <div class="kpi-value">{res['late']['bed']:.2f} Gy</div>
            </div>
          </div>

          <table>
            <tr>
              <th>Đối tượng / Endpoint</th>
              <th>$\\alpha/\\beta$ (Gy)</th>
              <th>$\\text{{BED}} = nd\\left(1 + \\frac{{d}}{{\\alpha/\\beta}}\\right)$</th>
              <th>$\\text{{EQD2}}$ (Gy)</th>
            </tr>
            <tr>
              <td>Mô bướu (Tumor)</td>
              <td>{res['tumor']['alpha_beta']:g}</td>
              <td><strong>{res['tumor']['bed']:.4f} Gy</strong></td>
              <td><strong>{res['tumor']['eqd2']:.4f} Gy</strong></td>
            </tr>
            <tr>
              <td>Mô lành đáp ứng sớm (niêm mạc, da)</td>
              <td>{res['early']['alpha_beta']:g}</td>
              <td><strong>{res['early']['bed']:.4f} Gy</strong></td>
              <td><strong>{res['early']['eqd2']:.4f} Gy</strong></td>
            </tr>
            <tr>
              <td>Mô lành đáp ứng muộn (tủy sống, xương)</td>
              <td>{res['late']['alpha_beta']:g}</td>
              <td><strong>{res['late']['bed']:.4f} Gy</strong></td>
              <td><strong>{res['late']['eqd2']:.4f} Gy</strong></td>
            </tr>
          </table>

          <div class="formula-box">
            <h4>Chi tiết thay số (Calculation)</h4>
            <ul>
              <li><strong>Mô bướu:</strong> <code>{res['tumor']['bed_formula']}</code></li>
              <li><strong>Mô lành đáp ứng sớm:</strong> <code>{res['early']['bed_formula']}</code></li>
              <li><strong>Mô lành đáp ứng muộn:</strong> <code>{res['late']['bed_formula']}</code></li>
            </ul>
          </div>

          <div class="note">
            <strong>Diễn giải & giới hạn:</strong> Giả định tổn thương dưới mức gây chết được sửa chữa hoàn toàn giữa các phân liều và chưa xét tái sinh tế bào theo thời gian. Không so sánh trực tiếp giá trị BED giữa hai endpoint có $\\alpha/\\beta$ khác nhau.
          </div>
        </div>
        """

    content = f"""
    <div class="card-header">
      <h2>Module 1: BED cho mô lành và mô bướu không tính đến tái sinh</h2>
      <p class="subtitle">Ví dụ lớp: $60\\text{{ Gy}} / 30\\text{{ phân liều}}$ ($d = 2\\text{{ Gy}}$), $\\alpha/\\beta = 10\\text{{ Gy}}$ (bướu, đáp ứng sớm) và $3\\text{{ Gy}}$ (đáp ứng muộn)</p>
    </div>

    <form method="post" action="/module1">
      <div class="grid-2">
        <div class="sub-panel">
          <h4>Thông số phác đồ xạ trị</h4>
          <div class="field"><label>Số phân liều ($n$):</label><input type="number" name="n" value="{n}" required></div>
          <div class="field"><label>Liều mỗi phân liều $d$ (Gy):</label><input type="number" step="any" name="d" value="{d}" required></div>
          <div class="field"><label>Tổng liều đối chiếu $D$ (Gy, tùy chọn):</label><input type="number" step="any" name="d_total" value="{d_total_in}"></div>
        </div>
        <div class="sub-panel">
          <h4>Tỷ số $\\alpha/\\beta$ theo từng nhóm mô</h4>
          <div class="field"><label>$\\alpha/\\beta$ Mô bướu (Gy):</label><input type="number" step="any" name="ab_tumor" value="{ab_tumor}" required></div>
          <div class="field"><label>$\\alpha/\\beta$ Mô lành đáp ứng sớm (Gy):</label><input type="number" step="any" name="ab_early" value="{ab_early}" required></div>
          <div class="field"><label>$\\alpha/\\beta$ Mô lành đáp ứng muộn (Gy):</label><input type="number" step="any" name="ab_late" value="{ab_late}" required></div>
        </div>
      </div>
      <div class="btn-row">
        <button type="submit" class="btn-primary">Tính BED & EQD2</button>
        <a href="/module1" class="btn-secondary">Nạp lại ví dụ lớp (60 Gy/30F)</a>
      </div>
    </form>
    {detail_html}
    """
    return render_template_string(BASE_HTML, content=content, active_page="m1")


@app.route("/module2", methods=["GET", "POST"])
def module2():
    n, d, total_time = 30, 2.0, 39.0
    t_ab, t_tk, t_k, t_dp = 10.0, 28.0, 0.9, 0.0
    e_ab, e_tk, e_k, e_dp = 10.0, 28.0, 0.0, 0.0
    l_ab, l_tk, l_k, l_dp = 3.0, 28.0, 0.0, 0.0

    res = None
    error_msg = None

    if request.method == "POST":
        try:
            n = int(request.form["n"])
            d = float(request.form["d"])
            total_time = float(request.form["total_time"])

            t_ab = float(request.form["t_ab"])
            t_tk = float(request.form["t_tk"])
            t_k = float(request.form["t_k"])
            t_dp = float(request.form["t_dp"])

            e_ab = float(request.form["e_ab"])
            e_tk = float(request.form["e_tk"])
            e_k = float(request.form["e_k"])
            e_dp = float(request.form["e_dp"])

            l_ab = float(request.form["l_ab"])
            l_tk = float(request.form["l_tk"])
            l_k = float(request.form["l_k"])
            l_dp = float(request.form["l_dp"])

            res = calc_bed_repop(
                n=n,
                d=d,
                total_time=total_time,
                tumor_cfg={"ab": t_ab, "tk": t_tk, "k": t_k, "d_prolif": t_dp},
                early_cfg={"ab": e_ab, "tk": e_tk, "k": e_k, "d_prolif": e_dp},
                late_cfg={"ab": l_ab, "tk": l_tk, "k": l_k, "d_prolif": l_dp},
            )
        except ValueError as exc:
            error_msg = str(exc)

    detail_html = ""
    if error_msg:
        detail_html = f'<div class="error-box"><strong>Lỗi dữ liệu:</strong> {error_msg}</div>'
    elif res:
        detail_html = f"""
        <div class="result-section">
          <div class="kpi-grid">
            <div class="kpi">
              <div class="kpi-label">Thời gian xạ (T)</div>
              <div class="kpi-value">{res['total_time']:g} ngày</div>
            </div>
            <div class="kpi">
              <div class="kpi-label">BED₀ Mô bướu</div>
              <div class="kpi-value">{res['tumor']['bed_0']:.2f} Gy</div>
            </div>
            <div class="kpi">
              <div class="kpi-label">Hao hụt do tái sinh</div>
              <div class="kpi-value">-{res['tumor']['repop_loss_bed']:.2f} Gy</div>
            </div>
            <div class="kpi">
              <div class="kpi-label">BED Mô bướu (hiệu chỉnh)</div>
              <div class="kpi-value">{res['tumor']['bed_corrected']:.2f} Gy</div>
            </div>
          </div>

          <table>
            <tr>
              <th>Đối tượng</th>
              <th>$\\alpha/\\beta$ (Gy)</th>
              <th>$T_{{\\text{{trì hoãn}}}}$</th>
              <th>$K$ (Gy/ngày)</th>
              <th>$\\text{{BED}}_0$ (Gy)</th>
              <th>$\\text{{BED}} = \\text{{BED}}_0 - K\\max(0, T - T_{{\\text{{trì hoãn}}}})$</th>
            </tr>
            <tr>
              <td>Mô bướu</td>
              <td>{t_ab:g}</td>
              <td>{t_tk:g} ngày</td>
              <td>{t_k:g}</td>
              <td>{res['tumor']['bed_0']:.4f}</td>
              <td><strong>{res['tumor']['bed_corrected']:.4f} Gy</strong></td>
            </tr>
            <tr>
              <td>Mô lành đáp ứng sớm</td>
              <td>{e_ab:g}</td>
              <td>{e_tk:g} ngày</td>
              <td>{e_k:g}</td>
              <td>{res['early']['bed_0']:.4f}</td>
              <td><strong>{res['early']['bed_corrected']:.4f} Gy</strong></td>
            </tr>
            <tr>
              <td>Mô lành đáp ứng muộn</td>
              <td>{l_ab:g}</td>
              <td>{l_tk:g} ngày</td>
              <td>{l_k:g}</td>
              <td>{res['late']['bed_0']:.4f}</td>
              <td><strong>{res['late']['bed_corrected']:.4f} Gy</strong></td>
            </tr>
          </table>

          <div class="formula-box">
            <h4>Chi tiết thay số (Calculation)</h4>
            <ul>
              <li><strong>Mô bướu:</strong> <code>{res['tumor']['bed_corr_formula']}</code></li>
              <li><strong>Mô lành đáp ứng sớm:</strong> <code>{res['early']['bed_corr_formula']}</code></li>
              <li><strong>Mô lành đáp ứng muộn:</strong> <code>{res['late']['bed_corr_formula']}</code></li>
            </ul>
          </div>

          <div class="note">
            <strong>Diễn giải & lưu ý học thuật:</strong> Với phác đồ 6 tuần trên lớp ($T = 6 \\times 7 - 2 - 1 = 39\\text{{ ngày}}$), $T_{{\\text{{trì hoãn}}}} = 28\\text{{ ngày}}$, $K = 0{{,}}9\\text{{ Gy/ngày}}$ cho $\\text{{BED}} = 62{{,}}1\\text{{ Gy}}$. Mô lành đáp ứng sớm cũng có thể tái sinh nên cho phép nhập riêng hệ số $K$ thay vì mặc định bằng $0$.
          </div>
        </div>
        """

    content = f"""
    <div class="card-header">
      <h2>Module 2: BED cho mô lành và mô bướu tính đến tái sinh</h2>
      <p class="subtitle">Ví dụ lớp: $60\\text{{ Gy}} / 30\\text{{F}}$ trong 6 tuần ($T = 39\\text{{ ngày}}$), $T_{{\\text{{trì hoãn}}}} = 28\\text{{ ngày}}$, $K = 0{{,}}9\\text{{ Gy/ngày}} \\rightarrow \\text{{BED}} = 62{{,}}1\\text{{ Gy}}$</p>
    </div>

    <form method="post" action="/module2">
      <div class="sub-panel" style="margin-bottom:16px;">
        <h4>Thông số phác đồ & thời gian điều trị chung</h4>
        <div class="grid-3">
          <div class="field"><label>Số phân liều ($n$):</label><input type="number" name="n" value="{n}" required></div>
          <div class="field"><label>Liều mỗi phân liều $d$ (Gy):</label><input type="number" step="any" name="d" value="{d}" required></div>
          <div class="field"><label>Thời gian xạ $T$ (ngày):</label><input type="number" step="any" name="total_time" value="{total_time}" required></div>
        </div>
      </div>

      <div class="grid-3">
        <div class="sub-panel">
          <h4>1. Mô bướu</h4>
          <div class="field"><label>$\\alpha/\\beta$ (Gy):</label><input type="number" step="any" name="t_ab" value="{t_ab}" required></div>
          <div class="field"><label>$T_{{\\text{{trì hoãn}}}}$ (ngày):</label><input type="number" step="any" name="t_tk" value="{t_tk}" required></div>
          <div class="field"><label>$K$ (Gy/ngày):</label><input type="number" step="any" name="t_k" value="{t_k}" required></div>
          <div class="field"><label>$D_{{\\text{{prolif}}}}$ (Gy/ngày, tùy chọn):</label><input type="number" step="any" name="t_dp" value="{t_dp}" required></div>
        </div>

        <div class="sub-panel">
          <h4>2. Mô lành đáp ứng sớm</h4>
          <div class="field"><label>$\\alpha/\\beta$ (Gy):</label><input type="number" step="any" name="e_ab" value="{e_ab}" required></div>
          <div class="field"><label>$T_{{\\text{{trì hoãn}}}}$ (ngày):</label><input type="number" step="any" name="e_tk" value="{e_tk}" required></div>
          <div class="field"><label>$K$ (Gy/ngày):</label><input type="number" step="any" name="e_k" value="{e_k}" required></div>
          <div class="field"><label>$D_{{\\text{{prolif}}}}$ (Gy/ngày, tùy chọn):</label><input type="number" step="any" name="e_dp" value="{e_dp}" required></div>
        </div>

        <div class="sub-panel">
          <h4>3. Mô lành đáp ứng muộn</h4>
          <div class="field"><label>$\\alpha/\\beta$ (Gy):</label><input type="number" step="any" name="l_ab" value="{l_ab}" required></div>
          <div class="field"><label>$T_{{\\text{{trì hoãn}}}}$ (ngày):</label><input type="number" step="any" name="l_tk" value="{l_tk}" required></div>
          <div class="field"><label>$K$ (Gy/ngày):</label><input type="number" step="any" name="l_k" value="{l_k}" required></div>
          <div class="field"><label>$D_{{\\text{{prolif}}}}$ (Gy/ngày, tùy chọn):</label><input type="number" step="any" name="l_dp" value="{l_dp}" required></div>
        </div>
      </div>

      <div class="btn-row">
        <button type="submit" class="btn-primary">Tính BED có tái sinh</button>
        <a href="/module2" class="btn-secondary">Nạp lại ví dụ lớp (60 Gy/30F, T=39)</a>
      </div>
    </form>
    {detail_html}
    """
    return render_template_string(BASE_HTML, content=content, active_page="m2")


@app.route("/module3", methods=["GET", "POST"])
def module3():
    n1, d1, d2, ab = 25, 2.0, 3.0, 4.5
    res = None
    error_msg = None

    if request.method == "POST":
        try:
            n1 = int(request.form["n1"])
            d1 = float(request.form["d1"])
            d2 = float(request.form["d2"])
            ab = float(request.form["ab"])
            res = convert_regimen(n1, d1, d2, ab)
        except ValueError as exc:
            error_msg = str(exc)

    detail_html = ""
    if error_msg:
        detail_html = f'<div class="error-box"><strong>Lỗi dữ liệu:</strong> {error_msg}</div>'
    elif res:
        detail_html = f"""
        <div class="result-section">
          <div class="kpi-grid">
            <div class="kpi">
              <div class="kpi-label">BED phác đồ gốc</div>
              <div class="kpi-value">{res['bed1']:.2f} Gy</div>
            </div>
            <div class="kpi">
              <div class="kpi-label">Số phân liều lý thuyết (n₂)</div>
              <div class="kpi-value">{res['n2_exact']:.2f} F</div>
            </div>
            <div class="kpi">
              <div class="kpi-label">Phương án làm tròn xuống</div>
              <div class="kpi-value">{res['n2_floor']} phân liều</div>
            </div>
            <div class="kpi">
              <div class="kpi-label">Phương án làm tròn lên</div>
              <div class="kpi-value">{res['n2_ceil']} phân liều</div>
            </div>
          </div>

          <table>
            <tr>
              <th>Phương án làm tròn số phân liều</th>
              <th>Số phân liều ($n_2$)</th>
              <th>Tổng liều mới ($n_2 \\cdot d_2$)</th>
              <th>$\\text{{BED}}_2$ thực tế (Gy)</th>
              <th>Chênh lệch so với $\\text{{BED}}_1$</th>
            </tr>
            <tr>
              <td>Làm tròn xuống</td>
              <td><strong>{res['n2_floor']} phân liều</strong></td>
              <td>{res['n2_floor'] * res['d2']:.2f} Gy</td>
              <td>{res['bed2_floor']:.4f} Gy</td>
              <td>{res['bed2_floor'] - res['bed1']:+.4f} Gy</td>
            </tr>
            <tr>
              <td>Làm tròn lên</td>
              <td><strong>{res['n2_ceil']} phân liều</strong></td>
              <td>{res['n2_ceil'] * res['d2']:.2f} Gy</td>
              <td>{res['bed2_ceil']:.4f} Gy</td>
              <td>{res['bed2_ceil'] - res['bed1']:+.4f} Gy</td>
            </tr>
          </table>

          <div class="note">
            <strong>Diễn giải học thuật:</strong> Số phân liều $n_2$ phải là số nguyên nên khi làm tròn lên hoặc xuống cần tính lại $\\text{{BED}}_2$ thực tế và đối chiếu thêm độc tính trên mô lành ($\\alpha/\\beta \\approx 3\\text{{ Gy}}$).
          </div>
        </div>
        """

    content = f"""
    <div class="card-header">
      <h2>Module 3: Chuyển đổi phác đồ điều trị</h2>
      <p class="subtitle">Ví dụ lớp: Chuyển $50\\text{{ Gy}} / 25\\text{{F}}$ ($d_1 = 2\\text{{ Gy}}$) sang $d_2 = 3\\text{{ Gy}}$ cho mô bướu vú ($\\alpha/\\beta = 4{{,}}5\\text{{ Gy}}$) $\\rightarrow n_2 \\approx 14{{,}}44$ (làm tròn $14$ phân liều)</p>
    </div>

    <form method="post" action="/module3">
      <div class="grid-2">
        <div class="sub-panel">
          <h4>Phác đồ chuẩn ban đầu (1)</h4>
          <div class="field"><label>Số phân liều $n_1$:</label><input type="number" name="n1" value="{n1}" required></div>
          <div class="field"><label>Liều mỗi phân liều $d_1$ (Gy):</label><input type="number" step="any" name="d1" value="{d1}" required></div>
        </div>
        <div class="sub-panel">
          <h4>Phác đồ mục tiêu (2) & đặc tính mô</h4>
          <div class="field"><label>Liều mỗi phân liều mới $d_2$ (Gy):</label><input type="number" step="any" name="d2" value="{d2}" required></div>
          <div class="field"><label>Tỷ số $\\alpha/\\beta$ của mô duy trì BED (Gy):</label><input type="number" step="any" name="ab" value="{ab}" required></div>
        </div>
      </div>
      <div class="btn-row">
        <button type="submit" class="btn-primary">Chuyển đổi phác đồ</button>
        <a href="/module3" class="btn-secondary">Nạp lại ví dụ lớp (50 Gy/25F → 3 Gy)</a>
      </div>
    </form>
    {detail_html}
    """
    return render_template_string(BASE_HTML, content=content, active_page="m3")


@app.route("/module4", methods=["GET", "POST"])
def module4():
    n_p, d_p, n_e, d_e, ab = 30, 1.8, 5, 2.0, 10.0
    res = None
    error_msg = None

    if request.method == "POST":
        try:
            n_p = int(request.form["n_p"])
            d_p = float(request.form["d_p"])
            n_e = int(request.form["n_e"])
            d_e = float(request.form["d_e"])
            ab = float(request.form["ab"])
            res = repair_schedule(n_p, d_p, n_e, d_e, ab)
        except ValueError as exc:
            error_msg = str(exc)

    detail_html = ""
    if error_msg:
        detail_html = f'<div class="error-box"><strong>Lỗi dữ liệu:</strong> {error_msg}</div>'
    elif res:
        detail_html = f"""
        <div class="result-section">
          <div class="kpi-grid">
            <div class="kpi">
              <div class="kpi-label">Tổng liều kế hoạch ($D_p$)</div>
              <div class="kpi-value">{res['d_p_total']:.2f} Gy</div>
            </div>
            <div class="kpi">
              <div class="kpi-label">Tổng liều còn lại ($D_c$)</div>
              <div class="kpi-value">{res['d_c_total']:.2f} Gy</div>
            </div>
            <div class="kpi">
              <div class="kpi-label">Mức phân liều mới ($d_c$)</div>
              <div class="kpi-value">{res['d_c']:.4f} Gy</div>
            </div>
            <div class="kpi">
              <div class="kpi-label">Số phân liều hiệu chỉnh ($n_c$)</div>
              <div class="kpi-value">{res['n_c_round']} F ({res['n_c_exact']:.2f})</div>
            </div>
          </div>

          <table>
            <tr>
              <th>Giai đoạn điều trị</th>
              <th>Số phân liều ($n$)</th>
              <th>Liều / phân liều ($d$)</th>
              <th>Tổng liều ($D$)</th>
            </tr>
            <tr>
              <td>Kế hoạch ban đầu ($p$)</td>
              <td>{res['n_p']}</td>
              <td>{res['d_p']:.4f} Gy</td>
              <td>{res['d_p_total']:.2f} Gy</td>
            </tr>
            <tr>
              <td>Phần đã xạ sai ($e$)</td>
              <td>{res['n_e']}</td>
              <td>{res['d_e']:.4f} Gy</td>
              <td>{res['d_e_total']:.2f} Gy</td>
            </tr>
            <tr>
              <td>Phần hiệu chỉnh còn lại ($c$)</td>
              <td><strong>{res['n_c_round']}</strong> (lý thuyết {res['n_c_exact']:.2f})</td>
              <td><strong>{res['d_c']:.4f} Gy</strong></td>
              <td><strong>{res['d_c_total']:.2f} Gy</strong></td>
            </tr>
          </table>

          <div class="formula-box">
            <h4>Đối chiếu BED kế hoạch và sau hiệu chỉnh</h4>
            <ul>
              <li><strong>Công thức áp dụng:</strong> $D_c = D_p - D_e = {res['d_c_total']:.2f}\\text{{ Gy}}$ ; $d_c = \\frac{{D_p d_p - D_e d_e}}{{D_p - D_e}} = {res['d_c']:.4f}\\text{{ Gy}}$ ; $n_c = \\frac{{D_c}}{{d_c}} = {res['n_c_exact']:.2f}$.</li>
              <li><strong>BED kế hoạch:</strong> {res['bed_plan']:.4f} Gy | <strong>BED sau sửa ({res['n_c_round']} phân liều hiệu chỉnh):</strong> {res['bed_actual_after_repair']:.4f} Gy.</li>
            </ul>
          </div>
        </div>
        """

    content = f"""
    <div class="card-header">
      <h2>Module 4: Sửa sai phân liều</h2>
      <p class="subtitle">Ví dụ lớp: Kế hoạch $30 \\times 1{{,}}8\\text{{ Gy}}$ ($D_p = 54\\text{{ Gy}}$), $5$ phân liều đầu xạ sai $2\\text{{ Gy}}$ ($D_e = 10\\text{{ Gy}}$) $\\rightarrow d_c \\approx 1{{,}}7545\\text{{ Gy}}$, $n_c \\approx 25{{,}}1$ (làm tròn $25$ phân liều, $d_c \\approx 1{{,}}76\\text{{ Gy}}$)</p>
    </div>

    <form method="post" action="/module4">
      <div class="grid-3">
        <div class="sub-panel">
          <h4>Kế hoạch ban đầu (p)</h4>
          <div class="field"><label>Số phân liều $n_p$:</label><input type="number" name="n_p" value="{n_p}" required></div>
          <div class="field"><label>Liều/phân liều $d_p$ (Gy):</label><input type="number" step="any" name="d_p" value="{d_p}" required></div>
        </div>
        <div class="sub-panel">
          <h4>Phần đã xạ sai (e)</h4>
          <div class="field"><label>Số phân liều sai $n_e$:</label><input type="number" name="n_e" value="{n_e}" required></div>
          <div class="field"><label>Liều đã phát sai $d_e$ (Gy):</label><input type="number" step="any" name="d_e" value="{d_e}" required></div>
        </div>
        <div class="sub-panel">
          <h4>Tham số đối chiếu BED</h4>
          <div class="field"><label>Tỷ số $\\alpha/\\beta$ (Gy):</label><input type="number" step="any" name="ab" value="{ab}" required></div>
        </div>
      </div>
      <div class="btn-row">
        <button type="submit" class="btn-primary">Tính hiệu chỉnh phân liều</button>
        <a href="/module4" class="btn-secondary">Nạp lại ví dụ lớp (30×1.8 Gy, sai 5F×2 Gy)</a>
      </div>
    </form>
    {detail_html}
    """
    return render_template_string(BASE_HTML, content=content, active_page="m4")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)