#!/usr/bin/env python3
"""Generate Kakao Account phone-number consent review scenarios for three apps."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas


PAGE_WIDTH, PAGE_HEIGHT = A4
FONT_PATH = "/System/Library/Fonts/Supplemental/AppleGothic.ttf"
FONT_NAME = "KakaoReviewKorean"
INK = colors.HexColor("#171717")
MUTED = colors.HexColor("#5F6368")
LINE = colors.HexColor("#E6E8EB")
PANEL = colors.HexColor("#F7F8FA")
WHITE = colors.white
KAKAO = colors.HexColor("#FEE500")


@dataclass(frozen=True)
class Service:
    korean_name: str
    english_name: str
    package: str
    policy_url: str
    output_name: str
    accent: colors.Color
    effective_date: str = "2026년 8월 7일"


SERVICES = (
    Service(
        korean_name="낚시캐시",
        english_name="CashLoop2",
        package="com.ttalkkag.cashloop2",
        policy_url="https://aihaejwo.site/www/ttalkkag/privacy_policy_loop2.html",
        output_name="cashloop2_kakao_phone_signup_review.pdf",
        accent=colors.HexColor("#2865A7"),
        effective_date="2026년 8월 14일",
    ),
    Service(
        korean_name="캐시주사위",
        english_name="CashDiceW",
        package="com.ttalkkag.cashdice",
        policy_url="https://aihaejwo.site/www/ttalkkag/privacy_policy_dice.html",
        output_name="cashdicew_kakao_phone_signup_review.pdf",
        accent=colors.HexColor("#C65A45"),
        effective_date="2026년 8월 11일",
    ),
    Service(
        korean_name="캐시딸깍",
        english_name="Tree",
        package="com.ttalkkag.tree",
        policy_url="https://aihaejwo.site/www/ttalkkag/privacy-policy.html",
        output_name="tree_kakao_phone_signup_review.pdf",
        accent=colors.HexColor("#D99A00"),
    ),
    Service(
        korean_name="캐시딸깍 라이트",
        english_name="TreeGo",
        package="com.ttalkkag.treelite",
        policy_url="https://aihaejwo.site/www/ttalkkag/privacy-policy_.html",
        output_name="treego_kakao_phone_signup_review.pdf",
        accent=colors.HexColor("#5B8A45"),
    ),
    Service(
        korean_name="캐시펑",
        english_name="CashPub",
        package="com.ttalkkag.cashpung",
        policy_url="https://aihaejwo.site/www/ttalkkag/privacy_policy_pung.html",
        output_name="cashpub_kakao_phone_signup_review.pdf",
        accent=colors.HexColor("#5A72E8"),
    ),
    Service(
        korean_name="캐시펑 미니",
        english_name="CashPubGo",
        package="com.ttalkkag.cashpungmini",
        policy_url="https://aihaejwo.site/www/ttalkkag/privacy_policy_pung_go.html",
        output_name="cashpubgo_kakao_phone_signup_review.pdf",
        accent=colors.HexColor("#D99600"),
    ),
    Service(
        korean_name="캐시캐",
        english_name="CashDuck",
        package="com.ttalkkag.cashduck",
        policy_url="https://aihaejwo.site/www/ttalkkag/privacy_policy_duck.html",
        output_name="cashduck_kakao_phone_signup_review.pdf",
        accent=colors.HexColor("#24705C"),
    ),
)


def register_font() -> None:
    if FONT_NAME not in pdfmetrics.getRegisteredFontNames():
        pdfmetrics.registerFont(TTFont(FONT_NAME, FONT_PATH))


def set_font(pdf: canvas.Canvas, size: float, color: colors.Color = INK) -> None:
    pdf.setFont(FONT_NAME, size)
    pdf.setFillColor(color)


def split_lines(text: str, width: float, size: float) -> list[str]:
    lines: list[str] = []
    for paragraph in text.split("\n"):
        if not paragraph:
            lines.append("")
            continue
        line = ""
        for character in paragraph:
            candidate = f"{line}{character}"
            if line and pdfmetrics.stringWidth(candidate, FONT_NAME, size) > width:
                lines.append(line.rstrip())
                line = character.lstrip() if character == " " else character
            else:
                line = candidate
        if line:
            lines.append(line.rstrip())
    return lines


def draw_text(
    pdf: canvas.Canvas,
    text: str,
    *,
    x: float,
    top: float,
    width: float,
    size: float,
    leading: float | None = None,
    color: colors.Color = INK,
) -> float:
    leading = leading or size * 1.5
    set_font(pdf, size, color)
    y = top
    for line in split_lines(text, width, size):
        pdf.drawString(x, y, line)
        y -= leading
    return y


def panel(
    pdf: canvas.Canvas,
    x: float,
    y: float,
    width: float,
    height: float,
    *,
    fill: colors.Color = WHITE,
    stroke: colors.Color = LINE,
) -> None:
    pdf.setFillColor(fill)
    pdf.setStrokeColor(stroke)
    pdf.setLineWidth(0.8)
    pdf.roundRect(x, y, width, height, 12, fill=1, stroke=1)


def chrome(pdf: canvas.Canvas, service: Service, page: int, section: str) -> None:
    pdf.setFillColor(WHITE)
    pdf.rect(0, 0, PAGE_WIDTH, PAGE_HEIGHT, fill=1, stroke=0)
    set_font(pdf, 8.5, service.accent)
    pdf.drawString(52, PAGE_HEIGHT - 42, service.english_name.upper())
    set_font(pdf, 8.5, MUTED)
    pdf.drawRightString(PAGE_WIDTH - 52, PAGE_HEIGHT - 42, section)
    pdf.setStrokeColor(LINE)
    pdf.line(52, PAGE_HEIGHT - 52, PAGE_WIDTH - 52, PAGE_HEIGHT - 52)
    pdf.line(52, 48, PAGE_WIDTH - 52, 48)
    set_font(pdf, 7.4, MUTED)
    pdf.drawString(52, 31, "카카오계정(전화번호) 필수 동의항목 심사 제출 시나리오")
    pdf.drawRightString(PAGE_WIDTH - 52, 31, f"{page} / 3")


def heading(pdf: canvas.Canvas, eyebrow: str, title: str, subtitle: str, accent: colors.Color) -> None:
    set_font(pdf, 9.5, accent)
    pdf.drawString(52, PAGE_HEIGHT - 86, eyebrow)
    set_font(pdf, 25, INK)
    pdf.drawString(52, PAGE_HEIGHT - 122, title)
    set_font(pdf, 10, MUTED)
    pdf.drawString(52, PAGE_HEIGHT - 147, subtitle)


def label_value(pdf: canvas.Canvas, label: str, value: str, x: float, y: float, width: float) -> None:
    set_font(pdf, 8.3, MUTED)
    pdf.drawString(x, y, label)
    draw_text(pdf, value, x=x + 82, top=y, width=width - 82, size=8.5, leading=12.5)


def page_one(pdf: canvas.Canvas, service: Service) -> None:
    chrome(pdf, service, 1, "01. 신청 항목")
    heading(
        pdf,
        "카카오 동의항목 심사 제출자료",
        f"{service.korean_name} · {service.english_name}",
        "회원 가입에 필요한 카카오계정(전화번호) 필수 동의 시나리오",
        service.accent,
    )

    panel(pdf, 52, 538, PAGE_WIDTH - 104, 80, fill=colors.HexColor("#FFFBE0"), stroke=KAKAO)
    set_font(pdf, 10, INK)
    pdf.drawString(70, 590, "신청 동의항목")
    set_font(pdf, 17, INK)
    pdf.drawString(70, 562, "카카오계정(전화번호) · 필수")
    set_font(pdf, 8.7, MUTED)
    pdf.drawRightString(PAGE_WIDTH - 70, 565, "카카오 로그인 및 리워드 회원 가입 시")

    # Kakao review attachments must not contain actual contact information.
    panel(pdf, 52, 369, PAGE_WIDTH - 104, 144)
    set_font(pdf, 11, service.accent)
    pdf.drawString(70, 486, "서비스 및 공개 방침")
    label_value(pdf, "서비스", f"{service.korean_name} ({service.english_name})", 70, 459, PAGE_WIDTH - 140)
    label_value(pdf, "패키지명", service.package, 70, 429, PAGE_WIDTH - 140)
    label_value(pdf, "운영자", "에이아이해줘(aiHaejwo)", 70, 399, PAGE_WIDTH - 140)
    set_font(pdf, 8.3, MUTED)
    pdf.drawString(70, 382, "공개 개인정보처리방침")
    set_font(pdf, 7.7, service.accent)
    pdf.drawString(170, 382, service.policy_url)

    panel(pdf, 52, 168, PAGE_WIDTH - 104, 154, fill=PANEL)
    set_font(pdf, 11, service.accent)
    pdf.drawString(70, 295, "심사 기준에 맞춘 회원 가입 원칙")
    draw_text(
        pdf,
        "• 카카오 로그인 동의 화면에서 카카오계정 전화번호를 필수로 제공합니다.\n"
        "• 카카오 회원번호와 카카오계정 전화번호는 회원 식별, 계정 관리, 중복·부정 이용 방지에만 사용합니다.\n"
        "• 카카오계정에 전화번호가 없거나 필수 제공에 동의하지 않으면 리워드 회원 가입을 완료할 수 없습니다.\n"
        "• 앱은 단말 전화 권한으로 번호를 읽거나 이용자에게 전화번호를 직접 입력받지 않습니다.",
        x=70,
        top=268,
        width=PAGE_WIDTH - 140,
        size=8.8,
        leading=21,
        color=INK,
    )

    set_font(pdf, 7.8, MUTED)
    pdf.drawString(52, 101, f"적용 기준: {service.effective_date} 시행 개인정보처리방침")


def flow_step(pdf: canvas.Canvas, service: Service, number: int, y: float, title: str, body: str) -> None:
    x = 52
    width = PAGE_WIDTH - 104
    height = 75
    panel(pdf, x, y, width, height)
    pdf.setFillColor(service.accent)
    pdf.circle(x + 27, y + 37.5, 15, fill=1, stroke=0)
    set_font(pdf, 9.5, WHITE)
    pdf.drawCentredString(x + 27, y + 33.5, str(number))
    set_font(pdf, 10, INK)
    pdf.drawString(x + 54, y + 47, title)
    draw_text(pdf, body, x=x + 54, top=y + 27, width=width - 72, size=8.3, leading=12.3, color=MUTED)


def page_two(pdf: canvas.Canvas, service: Service) -> None:
    chrome(pdf, service, 2, "02. 회원 가입 흐름")
    heading(
        pdf,
        "카카오 로그인 시나리오",
        "회원 가입 처리 흐름",
        "필수 동의를 한 이용자만 리워드 회원 가입을 완료하는 기준",
        service.accent,
    )
    steps = (
        ("카카오로 시작", "이용자가 앱 로그인 화면에서 카카오 로그인을 선택합니다."),
        ("카카오 동의 화면 표시", "카카오계정(전화번호)이 회원 가입을 위한 필수 동의항목으로 표시됩니다."),
        ("필수 제공 동의", "이용자가 전화번호 제공에 동의하면 카카오 회원번호와 카카오계정 전화번호가 카카오 로그인 연동을 통해 제공됩니다."),
        ("리워드 회원 식별", "제공받은 정보는 회원 가입, 계정 관리 및 중복·부정 이용 방지를 위해 처리됩니다."),
        ("회원 가입 완료", "필수 동의를 완료한 이용자만 리워드 적립·사용 기능을 이용할 수 있습니다."),
        ("미동의 또는 미보유", "카카오계정에 전화번호가 없거나 제공에 동의하지 않으면 회원 가입을 완료하지 않습니다."),
    )
    y = 592
    for index, (step_title, body) in enumerate(steps, start=1):
        flow_step(pdf, service, index, y, step_title, body)
        if index < len(steps):
            pdf.setStrokeColor(colors.HexColor("#C9D5D2"))
            pdf.setLineWidth(1)
            pdf.line(PAGE_WIDTH / 2, y - 9, PAGE_WIDTH / 2, y)
        y -= 84

    panel(pdf, 52, 75, PAGE_WIDTH - 104, 63, fill=colors.HexColor("#FFFBE0"), stroke=KAKAO)
    set_font(pdf, 9.5, INK)
    pdf.drawString(70, 113, "전화번호 수집 방식")
    draw_text(
        pdf,
        "카카오 로그인 동의에 따른 카카오 API 제공 정보만 사용합니다. 단말의 전화번호 권한 또는 직접 입력 방식은 사용하지 않습니다.",
        x=70,
        top=94,
        width=PAGE_WIDTH - 140,
        size=8.1,
        leading=12,
        color=MUTED,
    )


def table_row(
    pdf: canvas.Canvas,
    cells: tuple[str, str, str, str],
    y: float,
    height: float,
    widths: tuple[float, float, float, float],
) -> None:
    x = 52
    cursor = x
    for width, cell in zip(widths, cells):
        pdf.setStrokeColor(LINE)
        pdf.rect(cursor, y, width, height, fill=0, stroke=1)
        draw_text(pdf, cell, x=cursor + 9, top=y + height - 16, width=width - 18, size=7.6, leading=10.6)
        cursor += width


def page_three(pdf: canvas.Canvas, service: Service) -> None:
    chrome(pdf, service, 3, "03. 방침 기재 내용")
    heading(
        pdf,
        "개인정보처리방침 대조",
        "수집 항목 · 이용 목적 · 제한",
        "심사 신청 항목과 공개 개인정보처리방침의 일치 내용",
        service.accent,
    )
    x = 52
    widths = (135, 70, 184, 112)
    total = sum(widths)
    top = 610
    header_height = 34
    pdf.setFillColor(service.accent)
    pdf.roundRect(x, top - header_height, total, header_height, 9, fill=1, stroke=0)
    headers = ("수집 항목", "구분", "이용 목적", "보유 및 제한")
    cursor = x
    for width, header in zip(widths, headers):
        set_font(pdf, 8.4, WHITE)
        pdf.drawCentredString(cursor + width / 2, top - 22, header)
        cursor += width

    rows = (
        ("카카오 회원번호", "필수", "회원 가입, 로그인, 계정 관리", "회원 탈퇴 시까지"),
        ("카카오계정 전화번호", "필수", "리워드 계정 식별 및 중복·부정 이용 방지", "회원 탈퇴 시까지"),
        ("동의하지 않거나 전화번호가 없는 경우", "가입 제한", "필수 회원 가입 요건 확인", "리워드 회원 가입 미완료"),
        ("단말 전화번호", "미수집", "단말 전화 권한·직접 입력 방식 미사용", "해당 없음"),
    )
    y = 492
    for row in rows:
        table_row(pdf, row, y, 70, widths)
        y -= 70

    panel(pdf, 52, 144, PAGE_WIDTH - 104, 93, fill=PANEL)
    set_font(pdf, 10, service.accent)
    pdf.drawString(70, 211, "공개 방침의 핵심 문구")
    draw_text(
        pdf,
        "“카카오계정에 전화번호가 없거나 필수 제공에 동의하지 않는 경우 리워드 회원 가입을 완료할 수 없습니다.”",
        x=70,
        top=186,
        width=PAGE_WIDTH - 140,
        size=9,
        leading=14,
    )
    set_font(pdf, 7.8, MUTED)
    pdf.drawString(52, 101, "공개 개인정보처리방침")
    set_font(pdf, 7.5, service.accent)
    pdf.drawString(145, 101, service.policy_url)


def generate(service: Service, output_dir: Path) -> Path:
    output_path = output_dir / service.output_name
    pdf = canvas.Canvas(str(output_path), pagesize=A4)
    pdf.setTitle(f"{service.english_name} 카카오계정 전화번호 심사 제출 시나리오")
    pdf.setAuthor("에이아이해줘(aiHaejwo)")
    pdf.setSubject("카카오계정(전화번호) 필수 동의항목 심사 제출 시나리오")
    page_one(pdf, service)
    pdf.showPage()
    page_two(pdf, service)
    pdf.showPage()
    page_three(pdf, service)
    pdf.save()
    return output_path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--service",
        choices=[service.english_name.lower() for service in SERVICES],
        action="append",
        help="Generate only the selected service; repeat to generate more than one.",
    )
    args = parser.parse_args()
    register_font()
    output_dir = Path(__file__).resolve().parents[1] / "output" / "pdf"
    output_dir.mkdir(parents=True, exist_ok=True)
    selected_services = SERVICES
    if args.service:
        selected_names = set(args.service)
        selected_services = tuple(
            service for service in SERVICES if service.english_name.lower() in selected_names
        )
    for service in selected_services:
        print(generate(service, output_dir))


if __name__ == "__main__":
    main()
