#!/usr/bin/env python3
"""Build Cashpiig's public review page and PII-free Kakao review PDF."""
from html import escape
from pathlib import Path
import re
import shutil

from pypdf import PdfReader
from reportlab.pdfgen import canvas
import generate_kakao_phone_signup_review_pdfs as base
from generate_cashloop56_review import page_html, page_number

ROOT = Path(__file__).resolve().parents[1]
PROJECT = Path('/Users/healthmax/Documents/aihaejwo/ttalkkag/cashpiig')
WEB = ROOT / 'www/ttalkkag'
ASSETS = WEB / 'review_assets/cashpiig'
DATE = '2026년 10월 21일'
PLAN = '카카오계정 전화번호 필수 수집과 미동의 가입 제한은 동의항목 권한 승인 후 적용할 회원가입 정책입니다.'
NOTE = '앱 프로젝트의 실제 위젯을 테스트 데이터로 렌더링한 화면입니다. 실제 이용자 정보는 포함하지 않습니다.'
STORE = 'https://play.google.com/store/apps/details?id=com.ttalkkag.cashpiig'
SERVICE = base.Service('캐시돼지', 'Cashpiig', 'com.ttalkkag.cashpiig',
    'https://aihaejwo.site/www/ttalkkag/privacy_cashpiig.html',
    'cashpiig_kakao_phone_signup_review.pdf', base.colors.HexColor('#98702B'), DATE)
SCREENS = (
    ('home.png', '돼지 터치 홈', '홈에서 보유 포인트를 확인하고 돼지를 터치해 리워드 활동에 참여합니다. 광고 완료 및 서버 검증 후 포인트를 적립하며, 출석체크·룰렛·보물찾기로 이동할 수 있습니다.'),
    ('roulette.png', '룰렛 미션', '홈의 룰렛 버튼으로 진입합니다. GO 버튼을 선택해 리워드 미션에 참여하며, 화면에 포인트 보상 구간을 표시합니다.'),
    ('treasure.png', '황금 알 보물찾기', '홈의 보물찾기 버튼으로 진입합니다. 황금 알 중 하나를 선택해 미션에 참여하고 현재 보상 포인트를 확인합니다.'),
    ('store.png', '포인트 상점·출금 신청', '하단 상점 탭에서 보유 포인트, 필요한 포인트와 무료충전소 조건을 확인합니다. 조건 충족 후 현금 출금 등을 신청하며, 접수 후 운영자 확인을 거쳐 처리합니다. 신청 접수만으로 지급이 확정되지 않습니다.'),
)
STEPS = (
    ('카카오로 로그인', '신규 이용자와 기존 회원 모두 로그인 화면의 같은 버튼을 선택합니다.'),
    ('카카오 인증', '카카오톡 또는 카카오계정 인증을 통해 서비스에 로그인합니다.'),
    ('전화번호 필수 동의', '승인 후 카카오계정 전화번호를 회원가입 필수 동의항목으로 제공받는 정책입니다.'),
    ('회원 식별·가입', '회원 식별 및 기존 계정 확인 후 신규 회원가입 또는 기존 회원 로그인을 완료합니다.'),
    ('미동의·미보유 처리', '승인 후 전화번호가 없거나 필수 제공에 동의하지 않으면 회원가입을 완료하지 않는 정책입니다.'),
    ('가입 후 서비스 이용', '돼지 터치·미션·광고 및 무료충전소 참여 → 포인트 적립 → 상점 신청·처리 상태 확인으로 이어집니다.'),
)


def web_page(title, body):
    html = page_html(title, body, 'cashpiig')
    for old, new in (
        ('service_review_loopcashpiig.html', 'service_review_cashpiig.html'),
        ('privacy_policy_loopcashpiig.html', 'privacy_cashpiig.html'),
        ('terms_loopcashpiig.html', 'terms_cashpiig.html'),
    ):
        html = html.replace(old, new)
    return html


def build_web():
    ASSETS.mkdir(parents=True, exist_ok=True)
    operator = '<p>상호: 에이아이해줘(aiHaejwo)<br>사업자등록번호: 457-06-03603<br>개인정보·서비스 문의: <a href="mailto:aihaejwo@gmail.com">aihaejwo@gmail.com</a><br>캐시돼지(Cashpiig)는 에이아이해줘(aiHaejwo)가 운영합니다.</p>'
    body = f'''<h1>캐시돼지 서비스 소개 및 회원가입 시나리오</h1>
<p>Cashpiig · 패키지명: {SERVICE.package} · 작성일: {DATE}</p>
<h2>서비스 운영자 및 사업자 정보</h2>{operator}
<p><a href="{STORE}" target="_blank" rel="noopener">Google Play에서 캐시돼지 보기</a></p>
<h2>어떤 서비스인가요?</h2><p>캐시돼지는 돼지 터치, 출석체크, 룰렛, 황금 알 보물찾기, 광고·무료충전소 참여에 따른 포인트 적립을 제공하는 Android 리워드 앱입니다. 보유 포인트와 조건을 확인하고 상점에서 상품 교환·현금 출금을 신청할 수 있습니다.</p>
<h2>로그인 화면 구성</h2><p>아래는 프로젝트 로그인 화면의 문구와 버튼을 재현한 구성도이며, 실제 캡처가 아닙니다.</p>
<div class="phone"><h2>캐시돼지</h2><p>캐시돼지를 터치하고 포인트를 받아보세요</p><div class="button">카카오로 로그인</div><div class="button guest">게스트 모드로 둘러보기</div><p>이용약관 · 개인정보처리방침</p></div>
<p>별도의 아이디·비밀번호 가입 없이 카카오로 로그인 버튼에서 신규 계정을 생성하며, 기존 회원도 같은 버튼을 사용합니다. 게스트 모드는 체험용이며 실제 서버 포인트 적립·교환·출금 신청은 회원 기능입니다.</p>
<h2>카카오계정 전화번호 필수 회원가입 정책</h2><p class="notice">{PLAN} 현재 배포 앱에서 해당 동의항목 승인 또는 가입 차단 구현이 완료되었다는 증빙은 아닙니다.</p>
<ol>'''
    body += ''.join(f'<li><strong>{title}</strong>: {description}</li>' for title, description in STEPS)
    body += f'''</ol><p>전화번호는 카카오 로그인 동의에 따른 API 제공 정보로 수집하며, 회원가입·계정 관리·중복 및 부정 이용 방지에 이용합니다. 단말 전화 권한으로 번호를 읽거나 직접 입력받는 방식은 사용하지 않습니다.</p>
<h2>가입 후 이용 동선 및 상세 서비스 화면</h2><p class="notice">{NOTE} 포인트·상품·신청 조건은 테스트 예시이며 최신 운영 안내는 앱을 기준으로 합니다.</p><div class="screens">'''
    for filename, title, description in SCREENS:
        shutil.copyfile(PROJECT / 'store/release_20261012/captures' / filename, ASSETS / filename)
        body += f'<figure><img src="review_assets/cashpiig/{filename}" alt="캐시돼지 {escape(title)} 테스트 화면" loading="lazy"><figcaption>{escape(title)}</figcaption><p>{escape(description)}</p></figure>'
    body += '''</div><h2>혜택·무료충전소 이용</h2><p>하단 혜택 탭 → 무료충전소 시작 → 제휴 혜택 선택·참여 → 제휴사 보상 검증 → 포인트 반영 순서로 이용합니다. 상점에서는 누적 무료충전소 포인트와 신청 조건을 별도로 확인합니다.</p>
<p><a href="../../output/pdf/cashpiig_kakao_phone_signup_review.pdf">개인정보 없는 카카오 심사용 시나리오 PDF</a></p>'''
    (WEB / 'service_review_cashpiig.html').write_text(web_page('캐시돼지 서비스 소개·가입 시나리오', body))
    terms = (PROJECT / 'docs/legal/terms.html').read_text()
    terms = terms.replace('./index.html', './service_review_cashpiig.html').replace('./terms.html', './terms_cashpiig.html').replace('./privacy.html', './privacy_cashpiig.html')
    terms = terms.replace('버전 1.1 · 시행일: 2026년 7월 27일', f'버전 1.2 · 시행일: {DATE}').replace('support@aihaejwo.site', 'aihaejwo@gmail.com')
    terms = terms.replace('<h2>제 1 조 (목적)</h2>', '<h2>서비스 운영자 및 사업자 정보</h2>' + operator + '</section><section><h2>제 1 조 (목적)</h2>')
    terms = terms.replace('<h2>제 4 조 (회원 및 이용)</h2>', '<h2>제 4 조 (회원 및 이용)</h2><p>' + PLAN + '</p><p>카카오계정 전화번호를 회원가입 필수 항목으로 처리하며, 전화번호가 없거나 필수 제공에 동의하지 않으면 회원가입을 완료하지 않습니다.</p>')
    (WEB / 'terms_cashpiig.html').write_text(terms)


def build_pdf():
    base.register_font()
    output = ROOT / 'output/pdf' / SERVICE.output_name
    output.parent.mkdir(parents=True, exist_ok=True)
    pdf = canvas.Canvas(str(output), pagesize=base.A4)
    pdf.setTitle('캐시돼지 카카오계정 전화번호 필수 회원가입 시나리오')
    pdf.setAuthor('에이아이해줘(aiHaejwo)')
    pdf.setSubject('권한 승인 후 적용할 가입 정책 및 테스트 데이터 기반 서비스 이용 동선')
    for index, draw in enumerate((base.page_one, base.page_two, base.page_three), 1):
        if index > 1:
            pdf.showPage()
        draw(pdf, SERVICE)
        base.draw_text(pdf, PLAN, x=52, top=681 if index == 2 else 659, width=491, size=8, color=SERVICE.accent)
        if index == 1:
            base.draw_text(pdf, 'Google Play: ' + STORE, x=52, top=140, width=491, size=7.5, color=base.MUTED)
        page_number(pdf, index, 5)
    for page, start in enumerate((0, 2), 4):
        pdf.showPage()
        base.chrome(pdf, SERVICE, page, f'0{page}. 상세 서비스 화면 및 이용 동선')
        base.heading(pdf, '캐시돼지 Android 서비스 화면', '가입 후 서비스 이용 시나리오', '홈 → 리워드·미션 참여 → 포인트 적립 → 상점 신청', SERVICE.accent)
        base.draw_text(pdf, NOTE, x=52, top=662, width=491, size=8, color=base.MUTED)
        base.draw_text(pdf, '금액·포인트·상품 조건은 테스트 예시입니다. 최신 운영 안내는 앱을 기준으로 합니다.', x=52, top=644, width=491, size=8, color=base.MUTED)
        for column, (filename, title, description) in enumerate(SCREENS[start:start + 2]):
            x = 52 + column * 258
            base.draw_text(pdf, title, x=x, top=612, width=233, size=12, color=SERVICE.accent)
            pdf.drawImage(str(ASSETS / filename), x, 225, width=197, height=350.22, preserveAspectRatio=True, mask='auto')
            base.draw_text(pdf, description, x=x, top=203, width=233, size=9, leading=14)
        if page == 4:
            base.draw_text(pdf, '혜택 탭 → 무료충전소 시작 → 제휴 혜택 참여 → 보상 검증 → 포인트 반영', x=52, top=90, width=491, size=8, color=base.MUTED)
        else:
            base.draw_text(pdf, '신청 입력 화면과 실제 이름·전화번호·이메일·계좌 정보는 첨부하지 않습니다.', x=52, top=90, width=491, size=8, color=base.MUTED)
        page_number(pdf, page, 5)
    pdf.save()
    reader = PdfReader(output)
    text = '\n'.join(page.extract_text() or '' for page in reader.pages)
    assert len(reader.pages) == 5 and sum(len(page.images) for page in reader.pages) == 4
    assert all(f'{i} / 5' in page.extract_text() for i, page in enumerate(reader.pages, 1))
    assert all(title in text for _, title, _ in SCREENS)
    assert SERVICE.package in text and PLAN in text and '카카오계정(전화번호) · 필수' in text
    assert not any(other in text for other in ('채굴캐시', '뽑기캐시', 'CashLoop', '걸음'))
    assert not re.search(r'[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}|(?<!\d)01\d[- ]?\d{3,4}[- ]?\d{4}(?!\d)|(?<!\d)\d{6}-[1-4]\d{6}(?!\d)', text + str(reader.metadata))
    print(output)


if __name__ == '__main__':
    build_web()
    build_pdf()
