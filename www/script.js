document.addEventListener('DOMContentLoaded', () => {
    // Language Data
    const translations = {
        ko: {
            page_title: "캐시핑 - 간단 터치·돈버는앱 앱테크 리워드",
            nav_features: "주요기능",
            nav_how_to: "소개",
            btn_download: "앱 설치",
            hero_title_html: "캐시가 핑! <span class=\"highlight\">혜택이 핑!</span>\n터치만 해도 포인트가 쌓인다",
            hero_subtitle: "동전을 터치하고 미니게임으로 포인트 적립!\n지금 가입하고 쏟아지는 혜택을 받아보세요.",
            btn_google_play: "Google Play에서 받기",
            features_title_pre: "왜",
            features_title_post: "일까요?",
            features_subtitle: "매일매일 쌓이는 포인트, 확실한 행복",
            feature_1_title: "동전 클릭 & 적립",
            feature_1_desc: "화면의 동전을 터치할 때마다 포인트가 차곡차곡.\n제한 없이 클릭하고 모아보세요.",
            feature_2_title: "즐거운 미니게임",
            feature_2_desc: "동전잡기, 복권긁기, 타이밍 게임 등\n게임을 즐기면서 보너스 포인트를 획득하세요.",
            feature_3_title: "다양한 상품 교환",
            feature_3_desc: "모은 포인트로 네이버페이, 상품권 등\n원하는 상품으로 즉시 교환하세요.",
            how_it_works_title: "누구나 쉽게\n즐기는 앱테크",
            step_1_title: "간편한 시작",
            step_1_desc: "Google 계정으로 3초 만에 가입하고\n바로 포인트 적립을 시작하세요.",
            step_2_title: "매일매일 미션",
            step_2_desc: "출석체크, 퀘스트, 광고 시청으로\n추가 보상까지 챙기세요.",
            step_3_title: "실시간 교환",
            step_3_desc: "쌓인 포인트로 기프티콘, 상품권을\n내 폰 안의 지갑처럼 사용하세요.",
            footer_desc_html: "혁신적인 모바일 앱 서비스를 제공합니다.\n사용자의 일상을 더 편리하고 즐겁게.",
            footer_service: "서비스",
            privacy_policy: "개인정보처리방침"
        },
        en: {
            page_title: "Cashping - Easy Touch & Earn Rewards",
            nav_features: "Features",
            nav_how_to: "About",
            btn_download: "Install",
            hero_title_html: "Tap for Points!\n<span class=\"highlight\">Rewards Ping!</span>",
            hero_subtitle: "Earn points by tapping coins and playing mini-games!\nJoin now and enjoy pouring benefits.",
            btn_google_play: "Get it on Google Play",
            features_title_pre: "Why",
            features_title_post: "?",
            features_subtitle: "Daily points piling up, guaranteed happiness",
            feature_1_title: "Click & Earn",
            feature_1_desc: "Points pile up every time you touch the coin.\nClick without limits and save up.",
            feature_2_title: "Fun Mini-Games",
            feature_2_desc: "Catch coins, scratch cards, timing games.\nEnjoy games and get bonus points.",
            feature_3_title: "Various Exchanges",
            feature_3_desc: "Exchange points for Gift Cards, Naver Pay, etc.\nGet what you want instantly.",
            how_it_works_title: "AppTech Enjoyed\nBy Everyone",
            step_1_title: "Easy Start",
            step_1_desc: "Sign up in 3 seconds with Google\nand start earning points right away.",
            step_2_title: "Daily Missions",
            step_2_desc: "Take attendance, quests, and watch ads\nfor extra rewards.",
            step_3_title: "Real-time Exchange",
            step_3_desc: "Exchange accumulated points instantly\nfor Gift Cards and Coupons.",
            footer_desc_html: "Innovative mobile app services.\nMaking your daily life easier and more fun.",
            footer_service: "Service",
            privacy_policy: "Privacy Policy"
        },
        ja: {
            page_title: "Cashping - ポイント稼ぎ・ポイ活アプリ",
            nav_features: "特徴",
            nav_how_to: "使い方",
            btn_download: "インストール",
            hero_title_html: "タップで<span class=\"highlight\">ポイントGET!</span>\nキャッシュピング",
            hero_subtitle: "コインをタップしたりミニゲームでポイントが貯まる！\n今すぐ参加して特典を受け取りましょう。",
            btn_google_play: "Google Playで手に入れる",
            features_title_pre: "なぜ",
            features_title_post: "なのか？",
            features_subtitle: "毎日貯まるポイント、確実な幸せ",
            feature_1_title: "クリック＆獲得",
            feature_1_desc: "コインをタップするたびにポイントが貯まります。\n制限なくクリックして貯めましょう。",
            feature_2_title: "楽しいミニゲーム",
            feature_2_desc: "コインキャッチ、スクラッチ、タイミングゲームなど\nゲームを楽しみながらボーナスポイントを獲得。",
            feature_3_title: "様々な交換",
            feature_3_desc: "貯まったポイントはPayPayやギフト券など\n好きな商品に即座に交換できます。",
            how_it_works_title: "誰でも簡単\nポイ活アプリ",
            step_1_title: "簡単スタート",
            step_1_desc: "Googleアカウントで3秒で登録し\nすぐにポイント獲得を開始しましょう。",
            step_2_title: "毎日のミッション",
            step_2_desc: "出席チェック、クエスト、広告視聴で\n追加報酬もゲット。",
            step_3_title: "リアルタイム交換",
            step_3_desc: "貯まったポイントはいつでも\nスマホの中の財布のように使えます。",
            footer_desc_html: "革新的なモバイルアプリサービスを提供します。\nユーザーの日常をより便利で楽しく。",
            footer_service: "サービス",
            privacy_policy: "プライバシーポリシー"
        },
        ru: {
            page_title: "Cashping - Легкий заработок и награды",
            nav_features: "Особенности",
            nav_how_to: "Как это работает",
            btn_download: "Установить",
            hero_title_html: "Нажимай и <span class=\"highlight\">Зарабатывай!</span>\nCashping",
            hero_subtitle: "Зарабатывайте очки, нажимая на монеты и играя в мини-игры!\nПрисоединяйтесь сейчас и получайте бонусы.",
            btn_google_play: "Скачать в Google Play",
            features_title_pre: "Почему",
            features_title_post: "?",
            features_subtitle: "Ежедневные очки, гарантированная радость",
            feature_1_title: "Кликай и Зарабатывай",
            feature_1_desc: "Очки накапливаются с каждым нажатием на монету.\nКликайте без ограничений и копите.",
            feature_2_title: "Веселые Мини-игры",
            feature_2_desc: "Ловля монет, скретч-карты, игры на тайминг.\nНаслаждайтесь играми и получайте бонусы.",
            feature_3_title: "Различные Обмены",
            feature_3_desc: "Обменивайте очки на подарочные карты и многое другое.\nПолучайте то, что хотите, мгновенно.",
            how_it_works_title: "Заработок\nДля Всех",
            step_1_title: "Легкий Старт",
            step_1_desc: "Регистрация за 3 секунды через Google\nи начните зарабатывать очки сразу.",
            step_2_title: "Ежедневные Миссии",
            step_2_desc: "Отмечайтесь, выполняйте квесты и смотрите рекламу\nдля получения дополнительных наград.",
            step_3_title: "Мгновенный Обмен",
            step_3_desc: "Используйте накопленные очки в любое время\nкак кошелек в вашем телефоне.",
            footer_desc_html: "Инновационные мобильные приложения.\nДелаем вашу повседневную жизнь проще и веселее.",
            footer_service: "Сервис",
            privacy_policy: "Политика конфиденциальности"
        }
    };

    // Language Switcher Logic
    const langBtn = document.getElementById('lang-btn');
    const langDropdown = document.querySelector('.lang-dropdown');
    const currentLangSpan = document.getElementById('current-lang');

    // Toggle Dropdown
    if (langBtn) {
        langBtn.addEventListener('click', (e) => {
            e.stopPropagation();
            langDropdown.classList.toggle('show');
        });
    }

    // Close Dropdown when clicking outside
    document.addEventListener('click', () => {
        if (langDropdown) langDropdown.classList.remove('show');
    });

    // Change Language
    document.querySelectorAll('.lang-dropdown li').forEach(item => {
        item.addEventListener('click', () => {
            const lang = item.getAttribute('data-lang');
            setLanguage(lang);
        });
    });

    function setLanguage(lang) {
        // Update Text
        document.querySelectorAll('[data-i18n]').forEach(element => {
            const key = element.getAttribute('data-i18n');
            if (translations[lang][key]) {
                if (key.includes('html')) {
                    element.innerHTML = translations[lang][key].replace(/\n/g, '<br>'); // Simple replace for newlines if needed, or rely on white-space: pre-line in CSS
                } else {
                    element.textContent = translations[lang][key];
                }
            }
        });

        // Update Button Text
        if (currentLangSpan) currentLangSpan.textContent = lang.toUpperCase();

        // Update HTML lang attribute
        document.documentElement.lang = lang;
    }

    // Initialize
    // setLanguage('ko');

    // Scroll Observer for Fade-in effects
    const observerOptions = {
        root: null,
        rootMargin: '0px',
        threshold: 0.1
    };

    const observer = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('is-visible');
                observer.unobserve(entry.target); // Only animate once
            }
        });
    }, observerOptions);

    const scrollElements = document.querySelectorAll('[data-scroll]');
    scrollElements.forEach(el => observer.observe(el));

    // Smooth Scrolling for Anchor Links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const targetId = this.getAttribute('href');
            if (targetId === '#') return;
            const target = document.querySelector(targetId);
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth'
                });
            }
        });
    });

    // Header Background on Scroll
    const header = document.getElementById('navbar');
    window.addEventListener('scroll', () => {
        if (window.scrollY > 50) {
            header.style.boxShadow = '0 5px 20px rgba(0,0,0,0.3)';
            header.style.background = 'rgba(18, 18, 18, 0.98)';
        } else {
            header.style.boxShadow = 'none';
            header.style.background = 'rgba(18, 18, 18, 0.95)';
        }
    });
});
