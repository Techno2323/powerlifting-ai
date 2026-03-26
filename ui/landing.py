import streamlit as st

def show_landing():
    st.markdown("""
    <style>
    /* ── Hide Streamlit anchor links on headings ── */
    h1 a, h2 a, h3 a,
    [data-testid="stMarkdownContainer"] a[href^="#"] { display: none !important; }

    .lp-logo {
        font-family: 'Rajdhani', sans-serif;
        font-size: 1.5rem; font-weight: 700;
        color: #FFD700; letter-spacing: 3px;
        margin: 0; padding: 6px 0;
    }
    /* NAV outlined button */
    .lp-nav-btn .stButton > button {
        background: transparent !important;
        border: 1px solid #FFD70033 !important;
        color: #FFD700 !important;
        box-shadow: none !important;
        padding: 10px 22px !important;
        font-size: 0.88rem !important; letter-spacing: 1px !important;
    }
    .lp-nav-btn .stButton > button:hover {
        background: #FFD70010 !important; border-color: #FFD70066 !important;
        transform: none !important; box-shadow: none !important;
    }

    /* ── HERO ── */
    .lp-hero { text-align: center; padding: clamp(40px,8vw,96px) 20px clamp(20px,4vw,48px); }

    .lp-badge {
        display: inline-block;
        background: #FFD70012; border: 1px solid #FFD70033;
        border-radius: 50px; padding: 6px 20px;
        font-size: 0.72rem; color: #FFD700;
        letter-spacing: 3px; text-transform: uppercase;
        margin-bottom: 28px; animation: fadeDown 0.8s ease both;
    }
    @keyframes fadeDown {
        from { opacity: 0; transform: translateY(-16px); }
        to   { opacity: 1; transform: translateY(0); }
    }

    /* Use div instead of h1 to prevent Streamlit adding anchor links */
    .lp-headline {
        font-family: 'Rajdhani', sans-serif;
        font-size: clamp(3.2rem, 10vw, 7rem);
        font-weight: 700; line-height: 0.95;
        margin-bottom: 24px; color: #fff !important;
        animation: fadeUp 0.8s ease 0.2s both;
        text-align: center; letter-spacing: -1px;
    }
    .lp-gold-text {
        background: linear-gradient(90deg, #FFD700, #FFA500, #FFD700);
        background-size: 200% auto;
        -webkit-background-clip: text; background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: textShine 3s linear infinite;
        display: inline-block;
    }
    @keyframes textShine { to { background-position: 200% center; } }
    @keyframes fadeUp {
        from { opacity: 0; transform: translateY(24px); }
        to   { opacity: 1; transform: translateY(0); }
    }

    .lp-sub {
        color: #555;
        font-size: clamp(0.95rem, 2.5vw, 1.15rem);
        line-height: 1.85; max-width: 520px;
        margin: 0 auto 16px; text-align: center !important;
        animation: fadeUp 0.8s ease 0.4s both;
        display: block;
    }

    /* ── ANIMATED BARBELL in hero ── */
    .lp-barbell-wrap {
        display: flex; align-items: center; justify-content: center;
        gap: 0; margin: 32px auto 0; opacity: 0.12;
        animation: fadeUp 0.8s ease 0.6s both;
    }
    .lp-plate {
        width: 22px; height: 60px;
        background: linear-gradient(135deg, #FFD700, #B8860B);
        border-radius: 4px;
        box-shadow: 0 0 10px #FFD70044;
        animation: platePulse 3s ease-in-out infinite;
    }
    .lp-plate.sm { width: 14px; height: 46px; animation-delay: 0.4s; }
    .lp-plate.xs { width: 10px; height: 36px; animation-delay: 0.8s; }
    .lp-bar {
        width: clamp(140px, 30vw, 260px); height: 8px;
        background: linear-gradient(90deg, #888, #ccc, #888);
        border-radius: 4px;
    }
    .lp-collar {
        width: 10px; height: 20px;
        background: #888; border-radius: 2px;
    }
    @keyframes platePulse {
        0%,100% { box-shadow: 0 0 8px #FFD70033; }
        50%      { box-shadow: 0 0 22px #FFD70099; transform: scaleY(1.04); }
    }

    /* ── SCROLLING MARQUEE BELT ── */
    .lp-marquee-wrap {
        overflow: hidden;
        border-top: 1px solid #141414;
        border-bottom: 1px solid #141414;
        padding: 14px 0; margin: 48px 0 0;
        animation: fadeUp 0.8s ease 1s both;
    }
    .lp-marquee-track {
        display: flex; white-space: nowrap;
        animation: marqueeScroll 28s linear infinite;
    }
    .lp-marquee-track:hover { animation-play-state: paused; }
    .lp-marquee-item {
        font-family: 'Rajdhani', sans-serif;
        font-size: 0.8rem; letter-spacing: 4px;
        text-transform: uppercase; padding: 0 32px;
        color: #2a2a2a; flex-shrink: 0;
    }
    .lp-marquee-item.gold { color: #FFD70055; }
    @keyframes marqueeScroll {
        from { transform: translateX(0); }
        to   { transform: translateX(-50%); }
    }

    /* ── STATS ── */
    .lp-stats {
        display: flex; justify-content: center;
        align-items: center;
        gap: clamp(24px, 5vw, 72px); flex-wrap: wrap;
        padding: clamp(24px,4vw,40px) 20px;
        border-top: 1px solid #111;
        border-bottom: 1px solid #111;
        animation: fadeUp 0.8s ease 0.8s both;
    }
    .lp-stat-num {
        font-family: 'Rajdhani', sans-serif;
        font-size: clamp(1.8rem, 4vw, 2.8rem);
        font-weight: 700; color: #FFD700; line-height: 1;
        text-align: center;
    }
    .lp-stat-lbl {
        font-size: 0.68rem; color: #333;
        text-transform: uppercase; letter-spacing: 2px;
        margin-top: 5px; text-align: center;
    }
    .lp-divider { width: 1px; height: 40px; background: #1e1e1e; flex-shrink: 0; }

    /* ── SECTIONS ── */
    .lp-section {
        padding: clamp(60px,8vw,120px) clamp(16px,4vw,40px);
        max-width: 1100px; margin: 0 auto;
    }
    .lp-section-tag {
        text-align: center; font-size: 0.68rem;
        color: #FFD700; letter-spacing: 4px;
        text-transform: uppercase; margin-bottom: 12px;
    }
    .lp-section-title {
        font-family: 'Rajdhani', sans-serif;
        font-size: clamp(1.8rem, 4vw, 2.8rem);
        font-weight: 700; color: #fff;
        text-align: center; margin-bottom: 56px; line-height: 1.1;
    }

    /* ── FEATURE CARDS ── */
    .lp-features {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(290px, 1fr));
        gap: 20px;
    }
    .lp-feature {
        background: #0c0c0c; border: 1px solid #161616;
        border-radius: 20px; padding: 36px 28px;
        transition: transform 0.3s, border-color 0.3s, box-shadow 0.3s;
        position: relative; overflow: hidden;
    }
    .lp-feature::after {
        content: ''; position: absolute;
        top: 0; left: 0; right: 0; height: 2px;
        background: linear-gradient(90deg, transparent, #FFD700, transparent);
        opacity: 0; transition: opacity 0.3s;
    }
    .lp-feature:hover { transform: translateY(-6px); border-color: #FFD70022; box-shadow: 0 20px 48px #00000099; }
    .lp-feature:hover::after { opacity: 1; }
    .lp-feature-icon { font-size: 2.6rem; display: block; margin-bottom: 18px; }
    .lp-feature-title { font-family: 'Rajdhani', sans-serif; font-size: 1.1rem; font-weight: 700; color: #e0e0e0; letter-spacing: 1px; margin-bottom: 10px; }
    .lp-feature-desc { font-size: 0.875rem; color: #484848; line-height: 1.75; }

    /* ── HOW IT WORKS ── */
    .lp-steps { display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 24px; }
    .lp-step {
        text-align: center; padding: 36px 24px;
        background: #0c0c0c; border: 1px solid #161616;
        border-radius: 20px; transition: transform 0.3s, border-color 0.3s;
    }
    .lp-step:hover { transform: translateY(-4px); border-color: #FFD70022; }
    .lp-step-num {
        width: 52px; height: 52px;
        background: linear-gradient(135deg, #FFD700, #FFA500);
        border-radius: 50%; display: flex; align-items: center; justify-content: center;
        font-family: 'Rajdhani', sans-serif; font-size: 1.4rem; font-weight: 700; color: #000;
        margin: 0 auto 20px; box-shadow: 0 4px 20px #FFD70033;
    }
    .lp-step-title { font-family: 'Rajdhani', sans-serif; font-size: 1.1rem; font-weight: 700; color: #e0e0e0; margin-bottom: 10px; letter-spacing: 1px; }
    .lp-step-desc { font-size: 0.875rem; color: #484848; line-height: 1.65; }

    /* ── FINAL CTA ── */
    .lp-cta-wrap {
        background: linear-gradient(135deg, #0f0f0f, #0a0a0a);
        border: 1px solid #FFD70015; border-radius: 24px;
        text-align: center; padding: clamp(48px,8vw,96px) 24px;
        position: relative; overflow: hidden;
    }
    .lp-cta-wrap::before {
        content: ''; position: absolute;
        top: 50%; left: 50%; transform: translate(-50%, -50%);
        width: 500px; height: 300px;
        background: radial-gradient(ellipse, #FFD70012, transparent 70%);
        pointer-events: none; animation: heroGlow 6s ease-in-out infinite;
    }
    @keyframes heroGlow { 0%,100% { opacity:0.5; transform:translate(-50%,-50%) scale(1); } 50% { opacity:1; transform:translate(-50%,-50%) scale(1.1); } }
    .lp-cta-title { font-family: 'Rajdhani', sans-serif; font-size: clamp(2rem,5vw,3.2rem); color: #fff; font-weight: 700; margin-bottom: 12px; position: relative; }
    .lp-cta-sub { color: #444; font-size: 0.95rem; margin-bottom: 40px; position: relative; }

    /* ── FOOTER ── */
    .lp-footer { text-align: center; padding: 40px 20px; border-top: 1px solid #0f0f0f; color: #252525; font-size: 0.8rem; }
    .lp-footer span { color: #FFD70033; }

    @media (max-width: 640px) {
        .lp-hero { padding: 32px 12px 16px; }
        .lp-stats { gap: 20px; padding: 24px 12px; }
        .lp-divider { display: none; }
        .lp-section { padding: 48px 12px; }
        .lp-features { grid-template-columns: 1fr; }
        .lp-steps { grid-template-columns: 1fr; }
        .lp-cta-wrap { padding: 48px 16px; border-radius: 16px; }
        .lp-plate { display: none; }
        .lp-bar { width: 120px; }
    }
    </style>
    """, unsafe_allow_html=True)

    # ── NAV ──
    c_logo, c_space, c_btn = st.columns([4, 3, 1])
    with c_logo:
        st.markdown('<p class="lp-logo">🏋️ IRONIQ</p>', unsafe_allow_html=True)
    with c_btn:
        st.markdown('<div class="lp-nav-btn">', unsafe_allow_html=True)
        if st.button("Login →", use_container_width=True, key="nav_login"):
            st.session_state["page"] = "login"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    # ── HERO ──
    st.markdown("""
    <div class="lp-hero">
        <div class="lp-badge">🇮🇳 Built for Indian Athletes</div>
        <div class="lp-headline">
            FORGE YOUR<br>
            <span class="lp-gold-text">STRENGTH</span>
        </div>
        <span class="lp-sub">
            India's first AI powerlifting coach. Personalized 4-week programs,
            Indian diet plans, and real progress tracking.
        </span>

        <!-- Animated CSS Barbell -->
        <div class="lp-barbell-wrap">
            <div class="lp-plate xs"></div>
            <div class="lp-plate sm"></div>
            <div class="lp-plate"></div>
            <div class="lp-collar"></div>
            <div class="lp-bar"></div>
            <div class="lp-collar"></div>
            <div class="lp-plate"></div>
            <div class="lp-plate sm"></div>
            <div class="lp-plate xs"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── HERO CTA ──
    c1, c2, c3 = st.columns([2, 1, 2])
    with c2:
        if st.button("🚀 GET STARTED FREE", use_container_width=True, key="hero_cta"):
            st.session_state["page"] = "login"
            st.rerun()

    # ── SCROLLING MARQUEE ──
    marquee_items = (
        '<span class="lp-marquee-item gold">🏋️</span>'
        '<span class="lp-marquee-item">SQUAT</span>'
        '<span class="lp-marquee-item gold">·</span>'
        '<span class="lp-marquee-item">BENCH PRESS</span>'
        '<span class="lp-marquee-item gold">·</span>'
        '<span class="lp-marquee-item">DEADLIFT</span>'
        '<span class="lp-marquee-item gold">⚡</span>'
        '<span class="lp-marquee-item">POWERED BY AI</span>'
        '<span class="lp-marquee-item gold">·</span>'
        '<span class="lp-marquee-item">INDIAN DIET PLANS</span>'
        '<span class="lp-marquee-item gold">·</span>'
        '<span class="lp-marquee-item">4 WEEK PROGRAM</span>'
        '<span class="lp-marquee-item gold">🇮🇳</span>'
        '<span class="lp-marquee-item">BUILT FOR INDIA</span>'
        '<span class="lp-marquee-item gold">·</span>'
        '<span class="lp-marquee-item">DAILY SCORE SYSTEM</span>'
        '<span class="lp-marquee-item gold">·</span>'
        '<span class="lp-marquee-item">FORGE YOUR STRENGTH</span>'
        '<span class="lp-marquee-item gold">🏋️</span>'
    )
    st.markdown(f"""
    <div class="lp-marquee-wrap">
        <div class="lp-marquee-track">
            {marquee_items}
            {marquee_items}
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── STATS ──
    st.markdown("""
    <div class="lp-stats">
        <div>
            <div class="lp-stat-num">4</div>
            <div class="lp-stat-lbl">Week Program</div>
        </div>
        <div class="lp-divider"></div>
        <div>
            <div class="lp-stat-num">AI</div>
            <div class="lp-stat-lbl">Personalized</div>
        </div>
        <div class="lp-divider"></div>
        <div>
            <div class="lp-stat-num">3</div>
            <div class="lp-stat-lbl">Big Lifts Tracked</div>
        </div>
        <div class="lp-divider"></div>
        <div>
            <div class="lp-stat-num">🍛</div>
            <div class="lp-stat-lbl">Indian Diet</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── FEATURES ──
    st.markdown("""
    <div class="lp-section">
        <div class="lp-section-tag">What You Get</div>
        <div class="lp-section-title">Everything You Need To Get Strong</div>
        <div class="lp-features">
            <div class="lp-feature">
                <span class="lp-feature-icon">🤖</span>
                <div class="lp-feature-title">AI PROGRAM BUILDER</div>
                <div class="lp-feature-desc">Enter your current maxes and get a fully personalized 4-week powerlifting program built specifically for your level and goals.</div>
            </div>
            <div class="lp-feature">
                <span class="lp-feature-icon">🍛</span>
                <div class="lp-feature-title">INDIAN DIET PLAN</div>
                <div class="lp-feature-desc">No more chicken and broccoli. Get macro-optimized meal plans using dal, paneer, roti, rice — foods you actually eat.</div>
            </div>
            <div class="lp-feature">
                <span class="lp-feature-icon">📊</span>
                <div class="lp-feature-title">PROGRESS TRACKING</div>
                <div class="lp-feature-desc">Log every session, track your lifts over time, and watch your squat, bench and deadlift numbers climb week by week.</div>
            </div>
            <div class="lp-feature">
                <span class="lp-feature-icon">🏆</span>
                <div class="lp-feature-title">DAILY SCORE SYSTEM</div>
                <div class="lp-feature-desc">Earn points for every workout. The more consistent you are, the higher your score. Gamified fitness that keeps you coming back.</div>
            </div>
            <div class="lp-feature">
                <span class="lp-feature-icon">💡</span>
                <div class="lp-feature-title">BEGINNER FRIENDLY</div>
                <div class="lp-feature-desc">Never heard of RPE or RDL? Every exercise comes with plain English explanations so you always know exactly what to do.</div>
            </div>
            <div class="lp-feature">
                <span class="lp-feature-icon">🔄</span>
                <div class="lp-feature-title">ENDLESS PROGRAMS</div>
                <div class="lp-feature-desc">Finish your 4 weeks? Generate a new program instantly. Your history is always saved so you can track long term progress.</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── HOW IT WORKS ──
    st.markdown("""
    <div class="lp-section" style="padding-top:0">
        <div class="lp-section-tag">How It Works</div>
        <div class="lp-section-title">Three Steps to Your Program</div>
        <div class="lp-steps">
            <div class="lp-step">
                <div class="lp-step-num">1</div>
                <div class="lp-step-title">ENTER YOUR MAXES</div>
                <div class="lp-step-desc">Tell us your current squat, bench, and deadlift 1-rep maxes, your bodyweight, age, and training goal.</div>
            </div>
            <div class="lp-step">
                <div class="lp-step-num">2</div>
                <div class="lp-step-title">AI BUILDS YOUR PLAN</div>
                <div class="lp-step-desc">Gemini AI generates a complete 4-week program with exact weights, sets, reps and a full Indian diet plan in seconds.</div>
            </div>
            <div class="lp-step">
                <div class="lp-step-num">3</div>
                <div class="lp-step-title">TRAIN &amp; TRACK</div>
                <div class="lp-step-desc">Log each session, earn score points, and watch your lifts climb week over week. Generate new programs forever.</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── FINAL CTA ──
    st.markdown("""
    <div class="lp-section" style="padding-top:0; padding-bottom:32px;">
        <div class="lp-cta-wrap">
            <div class="lp-cta-title">Ready to Forge Your Strength?</div>
            <div class="lp-cta-sub">Zero cost. No credit card. Just lift.</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3 = st.columns([2, 1, 2])
    with c2:
        if st.button("🚀 START FOR FREE", use_container_width=True, key="bottom_cta"):
            st.session_state["page"] = "login"
            st.rerun()

    # ── FOOTER ──
    st.markdown("""
    <div class="lp-footer">
        <p>Built with ❤️ for Indian powerlifters &nbsp;·&nbsp; <span>IRONIQ</span> © 2026</p>
    </div>
    """, unsafe_allow_html=True)
