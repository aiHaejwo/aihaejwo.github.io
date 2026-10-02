#!/usr/bin/env python3
"""Build project-specific, pre-release Kakao review documents without user data."""
from html import escape
from pathlib import Path
import argparse
import re
import shutil
from pypdf import PdfReader

from reportlab.pdfgen import canvas
import generate_kakao_phone_signup_review_pdfs as base

ROOT = Path(__file__).resolve().parents[1]
PROJECTS = Path('/Users/healthmax/Documents/aihaejwo/ttalkkag')
DATE = '2026년 10월 1일'
PLAN = '카카오계정 전화번호 필수 수집과 미동의 가입 제한은 권한 승인 후 적용할 회원가입 정책입니다.'
APPS = (
    (5, '채굴캐시', '광맥을 채굴하고 포인트를 받아보세요', '광맥 채굴'),
    (6, '뽑기캐시', '캡슐을 뽑아 포인트를 받아보세요', '캡슐 뽑기'),
)
MINING_SCREENS = (
    ('screenshot_01_home.png', '광맥 채굴 홈', '홈에서 보유 포인트와 오늘 남은 채굴 횟수를 확인하고 광맥 채굴에 참여합니다. 채굴 후 포인트와 남은 횟수가 갱신됩니다.'),
    ('screenshot_02_charge_station.png', '목표·미션 선택', '홈 하단에서 상품·출금 목표와 무료충전소 참여 목표를 확인합니다. 출석체크, 룰렛, 보물찾기 및 충전하기 진입 버튼을 제공합니다.'),
    ('screenshot_03_roulette.png', '룰렛', '룰렛 화면에서 GO 버튼을 선택해 리워드 미션에 참여합니다. 화면에는 포인트 보상 구간이 표시됩니다.'),
    ('screenshot_04_treasure.png', '보물찾기', '황금 광석 중 하나를 선택해 보물찾기 미션에 참여합니다. 현재 보상 포인트를 화면에서 확인할 수 있습니다.'),
    ('screenshot_05_store.png', '포인트 상점', '보유 포인트와 상품별 필요 포인트, 신청 가능 여부를 확인합니다. 현금 출금·상품 교환 항목과 무료충전소 참여 조건을 안내하며, 신청은 접수 후 운영자 확인을 거칩니다.'),
)
SCREENS = {
    5: MINING_SCREENS,
    6: (
        ('screenshot_01_home.png', '캡슐 뽑기 홈', '홈에서 보유 포인트와 남은 캡슐 수를 확인하고 캡슐 뽑기에 참여합니다. 상품·출금 목표와 무료충전소 참여 목표도 함께 확인합니다.'),
        ('screenshot_02_charge_station.png', '혜택·무료충전소', '혜택 탭에서 무료충전소 시작 버튼을 선택합니다. 제공되는 혜택에 참여해 포인트를 적립하는 기능의 진입 화면입니다.'),
        MINING_SCREENS[2],
        ('screenshot_04_treasure.png', '캡슐 보물찾기', '뽑기 캡슐 중 하나를 선택해 보물찾기 미션에 참여합니다. 현재 보상 포인트를 화면에서 확인할 수 있습니다.'),
        MINING_SCREENS[4],
    ),
}
SCREEN_NOTE = '프로젝트에 저장된 앱 UI 테스트 캡처입니다. 포인트·상품은 테스트 예시이며 실제 이용자 정보는 포함하지 않습니다.'


def markdown_html(source):
    """Render these plain legal Markdown files using headings, lists and paragraphs."""
    blocks = []
    for line in source.splitlines():
        line = line.strip()
        if not line:
            continue
        heading = re.match(r'^(#{1,3}) (.+)$', line)
        if heading:
            level = len(heading[1])
            blocks.append(f'<h{level}>{escape(heading[2])}</h{level}>')
        elif line.startswith('- ') or re.match(r'^\d+\. ', line):
            content = re.sub(r'^(?:- |\d+\. )', '', line)
            blocks.append(f'<ul><li>{escape(content.replace("`", ""))}</li></ul>')
        else:
            blocks.append(f'<p>{escape(line.replace("`", ""))}</p>')
    return '\n'.join(blocks)


def page_html(title, body, number):
    return f'''<!doctype html>
<html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title><style>
body{{margin:0;background:#f4f7fb;color:#15243b;font-family:-apple-system,BlinkMacSystemFont,"Apple SD Gothic Neo",sans-serif;line-height:1.8;word-break:keep-all}}
main{{max-width:820px;margin:auto;padding:28px 20px}} article{{background:white;padding:28px;border:1px solid #dce4ef;border-radius:18px}}
h1{{font-size:28px}}h2{{font-size:20px;margin-top:30px}}a{{color:#1f5aaf}}nav{{display:flex;gap:18px;flex-wrap:wrap;margin-bottom:20px}}
.notice{{padding:16px;background:#fffbe0;border:1px solid #ead366;border-radius:12px}}.phone{{max-width:320px;padding:30px;margin:20px auto;background:#171717;color:white;border-radius:22px;text-align:center}}
.button{{padding:12px;margin-top:15px;background:#fee500;color:#171717;border-radius:8px}}.guest{{background:#fff;color:#171717}}
.screens{{display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:24px}}figure{{margin:0}}figure img{{width:100%;max-width:320px;height:auto;border-radius:12px}}figcaption{{font-weight:700}}
</style></head><body><main><nav><a href="service_review_loop{number}.html">서비스 소개·가입 시나리오</a><a href="privacy_policy_loop{number}.html">개인정보처리방침</a><a href="terms_loop{number}.html">이용약관</a></nav><article>{body}</article></main></body></html>'''


def build_html(number, name, tagline, activity, scenario_only=False):
    project = PROJECTS / f'cashLoop{number}'
    policy = (project / 'store/privacy_policy.md').read_text()
    policy = policy.replace('버전 1.1 · 시행일: 2026년 7월 27일', f'버전 1.2 · 시행일: {DATE}')
    policy = policy.replace('## 1. 개인정보처리자 및 개인정보 보호 담당', '## 1. 서비스 운영자 및 사업자 정보')
    policy = policy.replace(f'- 개인정보처리자: {name} 운영팀\n- 개인정보 보호 담당: {name} 운영팀\n- 이메일: `support@aihaejwo.site`',
        f'본 개인정보처리방침은 {name}(CashLoop{number}, 패키지명: com.ttalkkag.cashloop{number})에 적용됩니다.\n\n'
        '- 상호: 에이아이해줘(aiHaejwo)\n- 사업자등록번호: 457-06-03603\n- 개인정보 문의: aihaejwo@gmail.com\n'
        f'- {name}는 에이아이해줘(aiHaejwo)가 운영합니다.')
    policy = policy.replace('- 회원 및 로그인 관리:', '- 회원가입 신청 항목(필수): 카카오계정 전화번호. 회원가입, 계정 관리 및 중복·부정 이용 방지 목적으로 처리합니다.\n- 회원 및 로그인 관리:')
    policy = policy.replace('## 3. 개인정보의 처리 및 보유 기간',
        '### 카카오계정 전화번호 회원가입 정책\n\n' + PLAN + '\n\n'
        '카카오 로그인 동의 화면에서 전화번호 제공에 동의한 경우 카카오 API를 통해 전달받습니다. 단말의 전화번호 권한이나 직접 입력 방식은 사용하지 않습니다.\n\n'
        '카카오계정에 전화번호가 없거나 필수 제공에 동의하지 않는 경우 리워드 회원가입을 완료하지 않습니다. 게스트 모드는 화면 확인만 가능하며 실제 포인트 적립·교환·출금 신청을 제공하지 않습니다.\n\n'
        '전화번호는 회원 탈퇴 시 삭제하며, 법령상 별도 보존 의무가 있는 정보는 해당 기간 후 파기합니다.\n\n'
        '## 3. 개인정보의 처리 및 보유 기간')
    policy = policy.replace('support@aihaejwo.site', 'aihaejwo@gmail.com')
    if number == 5:
        # Kakao Login supplies account data; it is not a processor for this app.
        policy = policy.replace('- Kakao: 카카오 로그인 인증.\n', '')
        policy = policy.replace('카카오 로그인, Google 광고·알림', 'Google 광고·알림')
        policy = policy.replace('Google, Kakao, TNK, Hostinger', 'Google, TNK, Hostinger')
        policy = policy.replace(f'버전 1.2 · 시행일: {DATE}', '버전 1.3 · 시행일: 2026년 10월 2일')
        assert 'Kakao' not in policy and '회원가입 신청 항목(필수): 카카오계정 전화번호' in policy
    terms = (project / 'store/terms_of_service.md').read_text().replace('support@aihaejwo.site', 'aihaejwo@gmail.com')
    terms = terms.replace('버전 1.1 · 시행일: 2026년 7월 27일', f'버전 1.2 · 시행일: {DATE}')
    terms = terms.replace('## 제 4 조 (회원 및 이용)', '## 제 4 조 (회원 및 이용)\n\n' + PLAN + '\n\n카카오계정 전화번호를 회원가입 필수 항목으로 처리하며, 전화번호가 없거나 제공에 동의하지 않으면 회원가입을 완료하지 않습니다.\n')
    operator = f'<p>운영자: 에이아이해줘(aiHaejwo) · 사업자등록번호: 457-06-03603 · 문의: aihaejwo@gmail.com</p>'
    service = f'''<h1>{name} 서비스 소개 및 회원가입 시나리오</h1>
<p>패키지명: com.ttalkkag.cashloop{number} · 작성일: {DATE}</p>{operator}
<p class="notice">{PLAN} 아래 로그인 화면은 프로젝트의 화면 구성을 바탕으로 작성한 시안이며 실제 이용자 정보는 포함하지 않습니다.</p>
<h2>서비스 기능</h2><p>{name}는 {activity}, 출석체크, 룰렛, 보물찾기, 광고·무료충전소 참여에 따른 포인트 적립 기능을 제공합니다. 포인트 내역과 상품 교환·출금 신청 상태를 확인할 수 있습니다.</p>
<h2>로그인 화면 구성 시안</h2><div class="phone"><h2>{name}</h2><p>{tagline}</p><div class="button">카카오로 로그인</div><div class="button guest">게스트모드</div><p>이용약관 · 개인정보처리방침</p></div>
<h2>이 화면이 회원가입 화면인 이유</h2><p>별도 아이디·비밀번호 가입 없이 카카오로 로그인 버튼에서 신규 계정을 생성합니다. 동일 버튼으로 기존 회원도 로그인합니다. 전화번호 필수 동의는 승인 후 적용할 정책입니다.</p>
<h2>앱 정보</h2><p>앱 이름: {name} · 패키지명: com.ttalkkag.cashloop{number} · 인증 방식: 카카오톡 네이티브 로그인 · 플랫폼: Android</p>
<h2>버튼 선택 후</h2><p>카카오톡 인증 → 필수 제공 동의 확인 → 회원 식별 → 신규 가입 또는 기존 로그인</p>
<h2>리워드 이용 기준</h2><p>게스트모드는 화면 체험용입니다. 실제 서버 포인트 적립·교환·출금 신청은 회원 기능입니다.</p>
<h2>회원가입·기존 로그인 흐름</h2><ol><li>카카오로 로그인: 신규 이용자와 기존 회원 모두 같은 버튼을 선택합니다.</li><li>카카오톡 네이티브 인증: 앱의 카카오 SDK가 카카오톡을 통해 인증을 진행합니다.</li><li>개인정보 제공 필수 동의: 카카오계정 전화번호를 회원가입 필수 항목으로 제공받도록 신청합니다. 승인 후 적용할 정책입니다.</li><li>회원 검증 및 계정 생성: 회원 식별과 기존 계정을 확인하고 신규 회원가입 또는 기존 회원 로그인을 완료합니다.</li><li>필수 동의·미보유 처리: 전화번호가 없거나 필수 제공에 동의하지 않으면 회원가입을 완료하지 않는 정책입니다.</li><li>가입 후 서비스 이용: {activity}·미션·광고 참여에 따른 포인트 적립 및 교환 기능으로 이동합니다.</li></ol>
<p><a href="../../output/pdf/cashloop{number}_kakao_phone_signup_review.pdf">개인정보 없는 카카오 심사용 시나리오 PDF</a></p>'''
    service += f'<h2>상세 서비스 화면 및 이용 시나리오</h2><p class="notice">{SCREEN_NOTE}</p><div class="screens">'
    for filename, title, description in SCREENS[number]:
        source = project / 'store' / filename
        destination = ROOT / f'www/ttalkkag/review_assets/cashloop{number}' / filename
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, destination)
        service += f'<figure><img src="review_assets/cashloop{number}/{filename}" alt="{name} {title} 테스트 화면" loading="lazy"><figcaption>{title}</figcaption><p>{description}</p></figure>'
    service += '</div>'
    folder = ROOT / 'www/ttalkkag'
    for filename, title, body in (
        (f'privacy_policy_loop{number}.html', f'{name} 개인정보처리방침', markdown_html(policy)),
        (f'terms_loop{number}.html', f'{name} 이용약관', operator + markdown_html(terms)),
        (f'service_review_loop{number}.html', f'{name} 서비스 소개·가입 시나리오', service),
    ):
        if scenario_only and not filename.startswith('service_review_'):
            continue
        (folder / filename).write_text(page_html(title, body, number))


def page_number(pdf, page, total):
    # The reused three-page template has a fixed footer; replace only its counter.
    pdf.setFillColor(base.WHITE)
    pdf.rect(base.PAGE_WIDTH - 96, 23, 50, 20, fill=1, stroke=0)
    base.set_font(pdf, 7.4, base.MUTED)
    pdf.drawRightString(base.PAGE_WIDTH - 52, 31, f'{page} / {total}')


def service_screens(pdf, service, number, activity):
    screens = SCREENS[number]
    for page, start in enumerate(range(0, len(screens), 2), 4):
        pdf.showPage()
        base.chrome(pdf, service, page, f'0{page}. 상세 서비스 화면')
        base.heading(pdf, '전화번호 동의항목 심사 보완자료', '서비스 화면 및 이용 시나리오', '가입 후 제공하는 서비스의 주요 화면과 동작', service.accent)
        base.draw_text(pdf, SCREEN_NOTE, x=52, top=665, width=491, size=8.5, color=base.MUTED)
        for column, (filename, title, description) in enumerate(screens[start:start + 2]):
            x = 52 + column * 258
            base.draw_text(pdf, title, x=x, top=617, width=233, size=12, color=service.accent)
            pdf.drawImage(str(ROOT / f'www/ttalkkag/review_assets/cashloop{number}' / filename), x, 197, width=197, height=394, preserveAspectRatio=True, mask='auto')
            base.draw_text(pdf, description, x=x, top=175, width=233, size=9, leading=14)
        if start == 4:
            base.draw_text(pdf, f'신청 화면의 개인정보 입력 값은 첨부하지 않습니다.\n\n화면에 표시되는 금액·포인트는 테스트 캡처의 예시 값입니다. 실제 운영 상품과 신청 조건은 앱의 최신 안내를 기준으로 합니다.\n\n서비스 전체 흐름\n회원가입·로그인 → {activity}·미션 참여 → 포인트 적립 → 목표 확인 → 상점 상품 선택 → 신청·처리 상태 확인', x=310, top=571, width=233, size=10, leading=18)
        page_number(pdf, page, 6)


def build_pdf(number, name, tagline, activity):
    service = base.Service(name, f'CashLoop{number}', f'com.ttalkkag.cashloop{number}',
        f'https://aihaejwo.site/www/ttalkkag/privacy_policy_loop{number}.html',
        f'cashloop{number}_kakao_phone_signup_review.pdf', base.colors.HexColor('#98702B'), DATE)
    output = ROOT / 'output/pdf' / service.output_name
    pdf = canvas.Canvas(str(output), pagesize=base.A4)
    pdf.setTitle(f'{name} 카카오계정 전화번호 필수 회원가입 시나리오')
    pdf.setAuthor(name)
    pdf.setSubject('권한 승인 후 적용할 회원가입 정책 및 개인정보 없는 화면 구성 시안')
    base.chrome(pdf, service, 1, '01. 서비스·로그인 화면 시안')
    base.heading(pdf, '출시 전 심사 제출용 가입 기획안', name, service.package, service.accent)
    base.draw_text(pdf, PLAN, x=52, top=657, width=491, size=9, color=base.MUTED)
    base.panel(pdf, 52, 257, 214, 342, fill=base.colors.HexColor('#171717'))
    base.set_font(pdf, 21, base.WHITE)
    pdf.drawCentredString(159, 526, name)
    base.draw_text(pdf, tagline, x=66, top=488, width=186, size=9, color=base.WHITE)
    base.panel(pdf, 72, 378, 174, 43, fill=base.KAKAO, stroke=base.KAKAO)
    base.set_font(pdf, 12)
    pdf.drawCentredString(159, 393, '카카오로 로그인')
    base.panel(pdf, 72, 317, 174, 43)
    base.set_font(pdf, 11)
    pdf.drawCentredString(159, 334, '게스트모드')
    base.set_font(pdf, 8, base.WHITE)
    pdf.drawCentredString(159, 285, '이용약관 · 개인정보처리방침')
    base.draw_text(pdf, '프로젝트 로그인 화면을 바탕으로 한 구성 시안', x=52, top=238, width=214, size=7.5, color=base.MUTED)
    for y, height, title, body in (
        (469, 142, '이 화면이 회원가입 화면인 이유', '별도 아이디·비밀번호 가입 없이 카카오로 로그인 버튼에서 신규 계정을 생성합니다. 동일 버튼으로 기존 회원도 로그인합니다. 전화번호 필수 동의는 승인 후 적용할 정책입니다.'),
        (362, 96, '앱 정보', f'앱 이름: {name}\n패키지: {service.package}\n인증 방식: 카카오톡 네이티브 로그인\n플랫폼: Android'),
        (252, 99, '버튼 선택 후', '카카오톡 인증 → 필수 제공 동의 확인 → 회원 식별 → 신규 가입 또는 기존 로그인'),
        (156, 85, '리워드 이용 기준', '게스트모드는 화면 체험용입니다. 실제 서버 포인트 적립·교환·출금 신청은 회원 기능입니다.'),
    ):
        base.panel(pdf, 286, y, 257, height, fill=base.PANEL)
        base.draw_text(pdf, title, x=300, top=y + height - 22, width=229, size=10.5, color=service.accent)
        base.draw_text(pdf, body, x=300, top=y + height - 44, width=229, size=8.5, leading=13)
    base.draw_text(pdf, '이 문서에는 실제 이름, 이메일, 전화번호, 계정·계좌 정보가 없습니다.', x=52, top=150, width=491, size=9)
    total = 6
    page_number(pdf, 1, total)
    pdf.showPage()
    base.chrome(pdf, service, 2, '02. 승인 후 회원가입 흐름')
    base.heading(pdf, '카카오계정(전화번호) · 필수', '회원가입 처리 시나리오', '권한 승인 후 적용할 필수 동의·미동의 처리 기준', service.accent)
    steps = (
        ('카카오로 로그인', '신규 이용자와 기존 회원 모두 앱의 카카오로 로그인 버튼을 선택합니다.'),
        ('카카오톡 네이티브 인증', '앱의 카카오 SDK가 카카오톡을 통해 인증을 진행합니다.'),
        ('개인정보 제공 필수 동의', '카카오계정 전화번호를 회원가입 필수 항목으로 제공받도록 신청합니다. 승인 후 적용할 정책입니다.'),
        ('회원 검증 및 계정 생성', '회원 식별과 기존 계정을 확인하고 신규 회원가입 또는 기존 회원 로그인을 완료합니다.'),
        ('필수 동의·미보유 처리', '전화번호가 없거나 필수 제공에 동의하지 않으면 회원가입을 완료하지 않는 정책입니다.'),
        ('가입 후 서비스 이용', f'{activity}·미션·광고 참여에 따른 포인트 적립 및 교환 기능으로 이동합니다.'),
    )
    for index, (title, body) in enumerate(steps, 1):
        base.flow_step(pdf, service, index, 592 - (index - 1) * 84, title, body)
    base.draw_text(pdf, '현재 코드의 전화번호 가입 차단 구현을 증빙하는 문서는 아닙니다.', x=52, top=92, width=491, size=8.5, color=base.MUTED)
    page_number(pdf, 2, total)
    pdf.showPage()
    base.page_three(pdf, service)
    base.draw_text(pdf, '전화번호 항목은 권한 승인 후 적용할 회원가입 정책입니다.', x=52, top=83, width=491, size=8, color=base.MUTED)
    page_number(pdf, 3, total)
    service_screens(pdf, service, number, activity)
    pdf.save()
    reader = PdfReader(output)
    text = '\n'.join(page.extract_text() or '' for page in reader.pages)
    assert len(reader.pages) == total and name in text and service.package in text
    assert all(title in text for _, title, _ in SCREENS[number])
    assert sum(len(page.images) for page in reader.pages) == len(SCREENS[number])
    assert all(f'{index} / {total}' in page.extract_text() for index, page in enumerate(reader.pages, 1))
    assert ('광맥' if number == 6 else '캡슐') not in text, 'Do not mix project-specific scenarios'
    assert '권한 승인 후' in text and '카카오계정(전화번호) · 필수' in text
    assert '걸음' not in text
    assert not re.search(
        r'[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}|(?<!\d)01\d[- ]?\d{3,4}[- ]?\d{4}(?!\d)|(?<!\d)\d{6}-[1-4]\d{6}(?!\d)',
        text + str(reader.metadata),
    ), 'Review PDF must not contain actual contact or identity values'
    return output


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--service', choices=['cashloop5', 'cashloop6'], action='append')
    parser.add_argument('--scenario-only', action='store_true', help='Keep the published privacy policy and terms unchanged.')
    args = parser.parse_args()
    base.register_font()
    for app in APPS:
        if args.service and f'cashloop{app[0]}' not in args.service:
            continue
        build_html(*app, scenario_only=args.scenario_only)
        print(build_pdf(*app))
