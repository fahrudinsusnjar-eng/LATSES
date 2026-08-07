from __future__ import annotations

from typing import BinaryIO, Union

from lat_ces.scientific.analysis.plenum import SafetyStatus
from lat_ces.scientific.reports.exporter import SKOReportExporter

try:
    from reportlab.lib import colors
    from reportlab.lib.enums import TA_LEFT
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
    from reportlab.lib.units import cm
    from reportlab.platypus import (
        HRFlowable,
        Paragraph,
        SimpleDocTemplate,
        Spacer,
        Table,
        TableStyle,
    )
except Exception as import_error:  # pragma: no cover - environment dependent
    _REPORTLAB_IMPORT_ERROR = import_error
else:
    _REPORTLAB_IMPORT_ERROR = None


class SKOPDFGenerator:
    """Generate printable PDF certificates from SKOReportExporter output."""

    @staticmethod
    def generate_pdf(exporter: SKOReportExporter, output: Union[str, BinaryIO]) -> None:
        """Generate a PDF document to a file path or writable binary stream."""
        if _REPORTLAB_IMPORT_ERROR is not None:  # pragma: no cover - environment dependent
            raise ModuleNotFoundError(
                "reportlab is required for PDF generation"
            ) from _REPORTLAB_IMPORT_ERROR

        data = exporter.to_dict()

        doc = SimpleDocTemplate(
            output,
            pagesize=A4,
            leftMargin=1.5 * cm,
            rightMargin=1.5 * cm,
            topMargin=1.5 * cm,
            bottomMargin=1.5 * cm,
        )

        styles = getSampleStyleSheet()

        title_style = ParagraphStyle(
            "CertTitle",
            parent=styles["Heading1"],
            fontSize=16,
            leading=20,
            textColor=colors.HexColor("#1E293B"),
            alignment=TA_LEFT,
            fontName="Helvetica-Bold",
        )
        subtitle_style = ParagraphStyle(
            "CertSubTitle",
            parent=styles["Normal"],
            fontSize=9,
            leading=12,
            textColor=colors.HexColor("#64748B"),
            alignment=TA_LEFT,
        )
        section_heading = ParagraphStyle(
            "SectionHeading",
            parent=styles["Heading2"],
            fontSize=11,
            leading=15,
            textColor=colors.HexColor("#0F172A"),
            fontName="Helvetica-Bold",
            spaceBefore=8,
            spaceAfter=4,
        )
        body_style = ParagraphStyle(
            "CertBody",
            parent=styles["Normal"],
            fontSize=9,
            leading=12,
            textColor=colors.HexColor("#334155"),
        )

        status = data["evaluation"]["status"]
        if status == SafetyStatus.SAFE.value:
            bg_color = colors.HexColor("#DCFCE7")
            text_color = colors.HexColor("#15803D")
            border_color = colors.HexColor("#22C55E")
            status_text = "STATUS: SAFE (SIGURNO)"
        elif status == SafetyStatus.METROLOGICAL_RISK.value:
            bg_color = colors.HexColor("#FEF9C3")
            text_color = colors.HexColor("#A16207")
            border_color = colors.HexColor("#EAB308")
            status_text = "STATUS: UPOZORENJE / METROLOSKI RIZIK"
        else:
            bg_color = colors.HexColor("#FEE2E2")
            text_color = colors.HexColor("#B91C1C")
            border_color = colors.HexColor("#EF4444")
            status_text = "STATUS: KRITICNO PREKORACENJE"

        elements = []
        elements.append(Paragraph("SKO CERTIFIKAT SIGURNOSTI PLENUMA", title_style))
        elements.append(
            Paragraph(
                "LAT-CES Scientific Core - ISO GUM Compliance Verified",
                subtitle_style,
            )
        )
        elements.append(Spacer(1, 8))
        elements.append(
            HRFlowable(
                width="100%",
                thickness=1.5,
                color=colors.HexColor("#CBD5E1"),
                spaceAfter=10,
            )
        )

        meta = data["metadata"]
        meta_data = [
            [
                Paragraph(f"<b>Projekat:</b> {meta['project_name']}", body_style),
                Paragraph(f"<b>Plenum ID:</b> {meta['plenum_id']}", body_style),
            ],
            [
                Paragraph(f"<b>Inzenjer:</b> {meta['engineer_name']}", body_style),
                Paragraph(
                    f"<b>Datum (UTC):</b> {meta['timestamp_utc'][:10]}",
                    body_style,
                ),
            ],
        ]
        meta_table = Table(meta_data, colWidths=[9 * cm, 9 * cm])
        meta_table.setStyle(
            TableStyle(
                [
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
                    ("TOPPADDING", (0, 0), (-1, -1), 0),
                    ("LEFTPADDING", (0, 0), (-1, -1), 0),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                ]
            )
        )
        elements.append(meta_table)
        elements.append(Spacer(1, 10))

        status_banner_style = ParagraphStyle(
            "StatusBannerText",
            parent=styles["Normal"],
            fontSize=10,
            leading=14,
            textColor=text_color,
            fontName="Helvetica-Bold",
        )
        msg_style = ParagraphStyle(
            "StatusBannerMsg",
            parent=styles["Normal"],
            fontSize=8.5,
            leading=12,
            textColor=colors.HexColor("#1E293B"),
        )
        banner_content = [
            [Paragraph(status_text, status_banner_style)],
            [Paragraph(f"<b>Izvjestaj:</b> {data['evaluation']['message']}", msg_style)],
        ]
        banner_table = Table(banner_content, colWidths=[18 * cm])
        banner_table.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, -1), bg_color),
                    ("BOX", (0, 0), (-1, -1), 1, border_color),
                    ("PADDING", (0, 0), (-1, -1), 6),
                    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ]
            )
        )
        elements.append(banner_table)
        elements.append(Spacer(1, 12))

        elements.append(Paragraph("1. Metroloski i Fizikalni Rezultati", section_heading))
        headers = [
            "Parametar",
            "Nominalno",
            "Mjer. Neodredjenost (u)",
            "Jedinica",
            "Rel. Neodr.",
        ]
        rows = [[Paragraph(f"<b>{header}</b>", body_style) for header in headers]]

        for param_name, value in data["inputs"].items():
            rows.append(
                [
                    Paragraph(f"Ulaz ({param_name})", body_style),
                    Paragraph(f"{value['value']:.4f}", body_style),
                    Paragraph(f"+/-{value['uncertainty']:.4f}", body_style),
                    Paragraph(value["unit_symbol"], body_style),
                    Paragraph(f"{value['relative_uncertainty_pct']:.2f}%", body_style),
                ]
            )

        calculated = data["evaluation"]["calculated_value"]
        calc_rel_unc = (
            calculated["uncertainty"] / abs(calculated["value"]) * 100
            if calculated["value"] != 0
            else 0
        )
        rows.append(
            [
                Paragraph("<b>Izracunat Pritisak</b>", body_style),
                Paragraph(f"<b>{calculated['value']:.4f}</b>", body_style),
                Paragraph(f"<b>+/-{calculated['uncertainty']:.4f}</b>", body_style),
                Paragraph(f"<b>{calculated['unit_symbol']}</b>", body_style),
                Paragraph(f"<b>{calc_rel_unc:.2f}%</b>", body_style),
            ]
        )

        limit = data["evaluation"]["limit_value"]
        rows.append(
            [
                Paragraph("Dozvoljeni Limit", body_style),
                Paragraph(f"{limit['value']:.4f}", body_style),
                Paragraph("-", body_style),
                Paragraph(limit["unit_symbol"], body_style),
                Paragraph("-", body_style),
            ]
        )

        result_table = Table(rows, colWidths=[4 * cm, 3 * cm, 4.5 * cm, 3 * cm, 3.5 * cm])
        result_table.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#F1F5F9")),
                    ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
                    ("PADDING", (0, 0), (-1, -1), 4),
                    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ]
            )
        )
        elements.append(result_table)
        elements.append(Spacer(1, 10))

        elements.append(Paragraph("2. Sigurnosni Raspon i Margine (ISO GUM)", section_heading))
        evaluation = data["evaluation"]
        expanded_uncertainty = evaluation["expanded_uncertainty"]
        k_factor = evaluation["coverage_factor_k"]
        worst_case = calculated["value"] + expanded_uncertainty
        margin = evaluation["margin_to_limit"]

        lines = [
            (
                f"- <b>Prosirena neodredjenost (k={k_factor:.1f}, 95% pouzdanosti):</b> "
                f"+/-{expanded_uncertainty:.4f} {calculated['unit_symbol']}"
            ),
            (
                f"- <b>Gornja granica opsega (Worst-Case):</b> "
                f"{worst_case:.4f} {calculated['unit_symbol']}"
            ),
            (
                f"- <b>Nominalna margina do limita:</b> "
                f"{margin:.4f} {calculated['unit_symbol']}"
            ),
        ]
        for line in lines:
            elements.append(Paragraph(line, body_style))
            elements.append(Spacer(1, 2))

        if data.get("device"):
            device = data["device"]
            elements.append(Spacer(1, 8))
            elements.append(Paragraph("3. Specifikacija Mjernog Instrumenta", section_heading))
            device_lines = [
                f"- <b>Uredjaj:</b> {device['name']} ({device['device_type']})",
                f"- <b>Radni opseg:</b> [{device['min_range']} - {device['max_range']}] {device['unit']}",
                f"- <b>UUID Sljedivost:</b> <code>{device['uuid']}</code>",
            ]
            for line in device_lines:
                elements.append(Paragraph(line, body_style))
                elements.append(Spacer(1, 2))

        elements.append(Spacer(1, 15))
        elements.append(
            HRFlowable(
                width="100%",
                thickness=0.5,
                color=colors.HexColor("#CBD5E1"),
                spaceAfter=6,
            )
        )
        elements.append(
            Paragraph(
                "<i>Sluzbeni dokument generisan automatski putem "
                "LAT-CES Scientific Core v1.0 (ISO GUM Compliant)</i>",
                subtitle_style,
            )
        )

        doc.build(elements)


__all__ = ["SKOPDFGenerator"]