from weasyprint import HTML

html_content = """<!DOCTYPE html>
<html lang="bs">
<head>
<meta charset="UTF-8">
<style>
    @page {
        size: A4;
        margin: 15mm 12mm;
        background-color: #f8fafc;
    }

    *, *::before, *::after {
        box-sizing: border-box;
    }

    body {
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
        color: #1e293b;
        margin: 0;
        padding: 0;
        font-size: 10pt;
        line-height: 1.5;
    }

    .header-card {
        background-color: #0f172a;
        color: #ffffff;
        padding: 20px 24px;
        border-radius: 8px;
        margin-bottom: 20px;
    }

    .header-table {
        width: 100%;
        border-collapse: collapse;
    }

    .header-table td {
        vertical-align: middle;
    }

    .header-title {
        font-size: 18pt;
        font-weight: bold;
        letter-spacing: 0.5px;
        margin: 0;
        color: #f8fafc;
    }

    .header-subtitle {
        font-size: 9pt;
        color: #94a3b8;
        margin-top: 4px;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    .header-badge {
        text-align: right;
        font-size: 9pt;
        color: #cbd5e1;
    }

    .meta-section {
        background-color: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 6px;
        padding: 14px 18px;
        margin-bottom: 18px;
    }

    .meta-table {
        width: 100%;
        border-collapse: collapse;
    }

    .meta-table td {
        padding: 4px 8px;
        font-size: 9.5pt;
        width: 50%;
    }

    .meta-label {
        color: #64748b;
        font-weight: 600;
    }

    .meta-value {
        color: #0f172a;
        font-weight: bold;
    }

    .status-card {
        background-color: #fefce8;
        border: 2px solid #eab308;
        border-radius: 6px;
        padding: 14px 18px;
        margin-bottom: 20px;
    }

    .status-title {
        font-size: 11pt;
        font-weight: bold;
        color: #854d0e;
        margin-bottom: 6px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    .status-msg {
        font-size: 9.5pt;
        color: #1e293b;
        margin: 0;
    }

    .section-title {
        font-size: 12pt;
        font-weight: bold;
        color: #0f172a;
        border-left: 4px solid #2563eb;
        padding-left: 10px;
        margin-top: 20px;
        margin-bottom: 10px;
    }

    .data-table {
        width: 100%;
        border-collapse: collapse;
        margin-bottom: 20px;
        background-color: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 6px;
        overflow: hidden;
    }

    .data-table th {
        background-color: #f1f5f9;
        color: #334155;
        font-size: 9pt;
        font-weight: bold;
        text-align: left;
        padding: 8px 12px;
        border-bottom: 1px solid #cbd5e1;
    }

    .data-table td {
        padding: 8px 12px;
        font-size: 9pt;
        border-bottom: 1px solid #f1f5f9;
        color: #334155;
    }

    .data-table tr:last-child td {
        border-bottom: none;
    }

    .highlight-row {
        background-color: #f8fafc;
        font-weight: bold;
    }

    .gum-card {
        background-color: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 6px;
        padding: 14px 18px;
        margin-bottom: 20px;
    }

    .gum-list {
        margin: 0;
        padding-left: 18px;
    }

    .gum-list li {
        margin-bottom: 6px;
        font-size: 9.5pt;
    }

    .device-card {
        background-color: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 6px;
        padding: 14px 18px;
        margin-bottom: 20px;
    }

    .footer {
        margin-top: 30px;
        border-top: 1px solid #cbd5e1;
        padding-top: 10px;
        text-align: center;
        font-size: 8pt;
        color: #94a3b8;
    }
</style>
</head>
<body>

<div class="header-card">
    <table class="header-table">
        <tr>
            <td>
                <div class="header-title">SKO CERTIFIKAT SIGURNOSTI PLENUMA</div>
                <div class="header-subtitle">LAT-CES Scientific Core • ISO GUM Compliance Verified</div>
            </td>
            <td class="header-badge">
                <strong>Dokument:</strong> CERT-2026-0807<br>
                <strong>Verzija:</strong> 1.0 (Final)
            </td>
        </tr>
    </table>
</div>

<div class="meta-section">
    <table class="meta-table">
        <tr>
            <td><span class="meta-label">Projekat:</span> <span class="meta-value">LAT-CES Plenum Vent Analysis</span></td>
            <td><span class="meta-label">Plenum ID:</span> <span class="meta-value">PLENUM-MAIN-01</span></td>
        </tr>
        <tr>
            <td><span class="meta-label">Inzenjer:</span> <span class="meta-value">fahrudin Susnjar</span></td>
            <td><span class="meta-label">Datum (UTC):</span> <span class="meta-value">2026-08-07</span></td>
        </tr>
    </table>
</div>

<div class="status-card">
    <div class="status-title">STATUS EVALUACIJE: METROLOGICAL RISK (UPOZORENJE / METROLOSKI RIZIK)</div>
    <p class="status-msg">
        <strong>Inzenjerska procjena:</strong> Nominalna vrijednost (206.04 Pa) je unutar granica, ali prosirena mjerna neodredjenost (+/-17.36 Pa, k=2.0) probija dozvoljeni strukturalni limit od 220.00 Pa.
    </p>
</div>

<div class="section-title">1. Metroloski i Fizikalni Rezultati</div>
<table class="data-table">
    <thead>
        <tr>
            <th>Parametar / Opis</th>
            <th>Nominalno</th>
            <th>Mjerna Neodredjenost (u)</th>
            <th>Jedinica</th>
            <th>Relativna Neodredjenost</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>Ulaz: Brzina strujanja (v)</td>
            <td>18.5000</td>
            <td>+/-0.3780</td>
            <td>m/s</td>
            <td>2.04%</td>
        </tr>
        <tr>
            <td>Ulaz: Gustoca zraka (&rho;)</td>
            <td>1.2040</td>
            <td>+/-0.0120</td>
            <td>kg/m3</td>
            <td>1.00%</td>
        </tr>
        <tr class="highlight-row">
            <td><strong>Izracunat Dinamicki Pritisak (p<sub>dyn</sub>)</strong></td>
            <td><strong>206.0400</strong></td>
            <td><strong>+/-8.6800</strong></td>
            <td><strong>Pa</strong></td>
            <td><strong>4.21%</strong></td>
        </tr>
        <tr>
            <td>Dozvoljeni Strukturalni Limit</td>
            <td>220.0000</td>
            <td>&mdash;</td>
            <td>Pa</td>
            <td>&mdash;</td>
        </tr>
    </tbody>
</table>

<div class="section-title">2. Sigurnosni Raspon i Margine (ISO GUM)</div>
<div class="gum-card">
    <ul class="gum-list">
        <li><strong>Prosirena neodredjenost (k = 2.0, 95% nivo pouzdanosti):</strong> &plusmn;17.3600 Pa</li>
        <li><strong>Gornja granica opsega pouzdanosti (Worst-Case):</strong> 223.4000 Pa (Prekoracenje limita za +3.40 Pa)</li>
        <li><strong>Nominalna margina do limita:</strong> 13.9600 Pa</li>
        <li><strong>Standard uskladjenosti:</strong> ISO/IEC Guide 98-3:2008 (GUM) / LAT-CES Constitutional Science</li>
    </ul>
</div>

<div class="section-title">3. Specifikacija Mjernog Instrumenta</div>
<div class="device-card">
    <table class="meta-table">
        <tr>
            <td><span class="meta-label">Uredjaj:</span> <span class="meta-value">Pitot-Prandtl Sonda #HVAC-01</span></td>
            <td><span class="meta-label">Tip instrumenta:</span> <span class="meta-value">Pitot Tube</span></td>
        </tr>
        <tr>
            <td><span class="meta-label">Radni opseg:</span> <span class="meta-value">[0.0 - 50.0] m/s</span></td>
            <td><span class="meta-label">UUID Sljedivost:</span> <span class="meta-value" style="font-family: monospace;">dev-pitot-sonda-hvac01</span></td>
        </tr>
    </table>
</div>

<div class="footer">
    Sluzbeni dokument generisan automatski putem LAT-CES Scientific Core v1.0 (ISO GUM Compliant) • Stranica 1 od 1
</div>

</body>
</html>
"""

output_pdf = "demo_report.pdf"
HTML(string=html_content).write_pdf(output_pdf)
print(f"PDF generated successfully at {output_pdf}")
