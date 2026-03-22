import streamlit as st

def show_landing():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@400;600;700&family=Inter:wght@300;400;500;600&display=swap');

    .landing-wrapper {
        font-family: 'Inter', sans-serif;
        color: #e0e0e0;
    }

    /* Animated background particles */
    .hero-section {
        min-height: 100vh;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        text-align: center;
        padding: 60px 20px;
        position: relative;
        background: radial-gradient(ellipse at top, #1a1200 0%, #0a0a0a 60%);
        overflow: hidden;
    }

    .hero-section::before {
        content: '';
        position: absolute;
        width: 600px;
        height: 600px;
        background: radial-gradient(circle, #FFD70015 0%, transparent 70%);
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        animation: breathe 4s ease-in-out infinite;
        pointer-events: none;
    }

    @keyframes breathe {
        0%, 100% { transform: translate(-50%, -50%) scale(1); opacity: 0.5; }
        50% { transform: translate(-50%, -50%) scale(1.3); opacity: 1; }
    }

    .hero-badge {
        display: inline-block;
        background: #FFD70015;
        border: 1px solid #FFD70044;
        border-radius: 50px;
        padding: 6px 18px;
        font-size: 0.8rem;
        color: #FFD700;
        letter-spacing: 2px;
        text-transform: uppercase;
        margin-bottom: 24px;
        animation: fadeInDown 0.8s ease;
    }

    @keyframes fadeInDown {
        from { opacity: 0; transform: translateY(-20px); }
        to { opacity: 1; transform: translateY(0); }
    }

    .hero-title {
        font-family: 'Rajdhani', sans-serif;
        font-size: clamp(3rem, 8vw, 6rem);
        font-weight: 700;
        line-height: 1.1;
        margin-bottom: 8px;
        animation: fadeInUp 0.8s ease 0.2s both;
    }

    .hero-title .white { color: #ffffff; }
    .hero-title .gold {
        background: linear-gradient(90deg, #FFD700, #FFA500, #FFD700);
        background-size: 200% auto;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: shine 3s linear infinite, fadeInUp 0.8s ease 0.2s both;
    }

    @keyframes shine {
        to { background-position: 200% center; }
    }

    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(30px); }
        to { opacity: 1; transform: translateY(0); }
    }

    .hero-subtitle {
        font-size: clamp(1rem, 2.5vw, 1.25rem);
        color: #888;
        max-width: 500px;
        margin: 16px auto 40px;
        line-height: 1.8;
        animation: fadeInUp 0.8s ease 0.4s both;
    }

    .hero-cta {
        display: inline-block;
        background: linear-gradient(135deg, #FFD700, #FFA500);
        color: #000 !important;
        font-family: 'Rajdhani', sans-serif;
        font-size: 1.1rem;
        font-weight: 700;
        letter-spacing: 2px;
        padding: 16px 48px;
        border-radius: 50px;
        text-decoration: none;
        cursor: pointer;
        border: none;
        box-shadow: 0 0 30px #FFD70044;
        animation: fadeInUp 0.8s ease 0.6s both, glowPulse 2s ease-in-out infinite;
        transition: transform 0.2s ease;
    }

    .hero-cta:hover {
        transform: translateY(-3px);
        box-shadow: 0 0 50px #FFD70077;
    }

    @keyframes glowPulse {
        0%, 100% { box-shadow: 0 0 30px #FFD70044; }
        50% { box-shadow: 0 0 50px #FFD70088; }
    }

    .hero-stats {
        display: flex;
        gap: 40px;
        justify-content: center;
        margin-top: 60px;
        animation: fadeInUp 0.8s ease 0.8s both;
        flex-wrap: wrap;
    }

    .hero-stat-item {
        text-align: center;
    }

    .hero-stat-item .stat-number {
        font-family: 'Rajdhani', sans-serif;
        font-size: 2.5rem;
        font-weight: 700;
        color: #FFD700;
        line-height: 1;
    }

    .hero-stat-item .stat-label {
        font-size: 0.75rem;
        color: #555;
        text-transform: uppercase;
        letter-spacing: 2px;
        margin-top: 4px;
    }

    .stat-divider {
        width: 1px;
        background: #222;
        align-self: stretch;
    }

    /* Features Section */
    .features-section {
        padding: 100px 20px;
        background: #0a0a0a;
        text-align: center;
    }

    .section-label {
        font-size: 0.75rem;
        color: #FFD700;
        letter-spacing: 3px;
        text-transform: uppercase;
        margin-bottom: 16px;
    }

    .section-title {
        font-family: 'Rajdhani', sans-serif;
        font-size: clamp(2rem, 5vw, 3rem);
        font-weight: 700;
        color: #fff;
        margin-bottom: 60px;
    }

    .features-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
        gap: 24px;
        max-width: 1100px;
        margin: 0 auto;
    }

    .feature-card {
        background: #111;
        border: 1px solid #1e1e1e;
        border-radius: 20px;
        padding: 36px 28px;
        text-align: left;
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }

    .feature-card::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 2px;
        background: linear-gradient(90deg, transparent, #FFD700, transparent);
        opacity: 0;
        transition: opacity 0.3s ease;
    }

    .feature-card:hover {
        border-color: #FFD70033;
        transform: translateY(-5px);
        box-shadow: 0 20px 40px #00000066;
    }

    .feature-card:hover::before {
        opacity: 1;
    }

    .feature-icon {
        font-size: 2.5rem;
        margin-bottom: 20px;
        display: block;
    }

    .feature-title {
        font-family: 'Rajdhani', sans-serif;
        font-size: 1.3rem;
        font-weight: 700;
        color: #fff;
        margin-bottom: 12px;
        letter-spacing: 1px;
    }

    .feature-desc {
        font-size: 0.9rem;
        color: #666;
        line-height: 1.7;
    }

    /* Nav */
    .nav-bar {
        position: fixed;
        top: 0; left: 0; right: 0;
        z-index: 999;
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 16px 40px;
        background: #0a0a0acc;
        backdrop-filter: blur(10px);
        border-bottom: 1px solid #ffffff08;
    }

    .nav-logo {
        font-family: 'Rajdhani', sans-serif;
        font-size: 1.3rem;
        font-weight: 700;
        color: #FFD700;
        letter-spacing: 1px;
    }

    .nav-login {
        background: transparent;
        border: 1px solid #FFD70044;
        border-radius: 8px;
        padding: 8px 24px;
        color: #FFD700;
        font-family: 'Rajdhani', sans-serif;
        font-size: 0.95rem;
        font-weight: 600;
        letter-spacing: 1px;
        cursor: pointer;
        transition: all 0.2s ease;
        text-decoration: none;
    }

    .nav-login:hover {
        background: #FFD70015;
        border-color: #FFD700;
    }

    /* Floating orbs */
    .orb {
        position: absolute;
        border-radius: 50%;
        filter: blur(60px);
        opacity: 0.15;
        pointer-events: none;
    }

    .orb-1 {
        width: 300px; height: 300px;
        background: #FFD700;
        top: 10%; left: 10%;
        animation: float1 8s ease-in-out infinite;
    }

    .orb-2 {
        width: 200px; height: 200px;
        background: #FFA500;
        bottom: 20%; right: 15%;
        animation: float2 10s ease-in-out infinite;
    }

    @keyframes float1 {
        0%, 100% { transform: translate(0, 0); }
        50% { transform: translate(30px, -30px); }
    }

    @keyframes float2 {
        0%, 100% { transform: translate(0, 0); }
        50% { transform: translate(-20px, 20px); }
    }

    /* Scrollbar */
    ::-webkit-scrollbar { width: 4px; }
    ::-webkit-scrollbar-track { background: #0a0a0a; }
    ::-webkit-scrollbar-thumb { background: #FFD70044; border-radius: 2px; }
    </style>

    <div class="landing-wrapper">

        <!-- NAV -->
        <div class="nav-bar">
            <div class="nav-logo">🏋️ IRONIQ</div>
            <a class="nav-login" id="nav-login-btn" onclick="window.location.href='?page=login'">Login / Sign Up</a>
        </div>

        <!-- HERO -->
        <div class="hero-section">
            <div class="orb orb-1"></div>
            <div class="orb orb-2"></div>

            <div class="hero-badge">🇮🇳 Built for Indian Athletes</div>

            <div class="hero-title">
                <span class="white">FORGE YOUR</span><br>
                <span class="gold">STRENGTH</span>
            </div>

            <p class="hero-subtitle">
                India's first AI powerlifting coach. Personalized programs, Indian diet plans, real progress tracking.
            </p>

            <div id="cta-area"></div>

            <div class="hero-stats">
                <div class="hero-stat-item">
                    <div class="stat-number">4</div>
                    <div class="stat-label">Week Program</div>
                </div>
                <div class="stat-divider"></div>
                <div class="hero-stat-item">
                    <div class="stat-number">AI</div>
                    <div class="stat-label">Personalized</div>
                </div>
                <div class="stat-divider"></div>
                <div class="hero-stat-item">
                    <div class="stat-number">100%</div>
                    <div class="stat-label">Free</div>
                </div>
                <div class="stat-divider"></div>
                <div class="hero-stat-item">
                    <div class="stat-number">🍛</div>
                    <div class="stat-label">Indian Diet</div>
                </div>
            </div>
        </div>

        <!-- FEATURES -->
        <div class="features-section">
            <div class="section-label">What You Get</div>
            <div class="section-title">Everything You Need To Get Strong</div>

            <div class="features-grid">
                <div class="feature-card">
                    <span class="feature-icon">🤖</span>
                    <div class="feature-title">AI PROGRAM BUILDER</div>
                    <div class="feature-desc">Enter your current maxes and get a fully personalized 4-week powerlifting program built specifically for your level and goals.</div>
                </div>
                <div class="feature-card">
                    <span class="feature-icon">🍛</span>
                    <div class="feature-title">INDIAN DIET PLAN</div>
                    <div class="feature-desc">No more chicken and broccoli. Get macro-optimized meal plans using dal, paneer, roti, rice — foods you actually eat.</div>
                </div>
                <div class="feature-card">
                    <span class="feature-icon">📊</span>
                    <div class="feature-title">PROGRESS TRACKING</div>
                    <div class="feature-desc">Log every session, track your lifts over time, and watch your squat, bench and deadlift numbers climb week by week.</div>
                </div>
                <div class="feature-card">
                    <span class="feature-icon">🏆</span>
                    <div class="feature-title">DAILY SCORE SYSTEM</div>
                    <div class="feature-desc">Earn points for every workout. The more consistent you are, the higher your score. Gamified fitness that keeps you coming back.</div>
                </div>
                <div class="feature-card">
                    <span class="feature-icon">💡</span>
                    <div class="feature-title">BEGINNER FRIENDLY</div>
                    <div class="feature-desc">Never heard of RPE or RDL? Every exercise comes with plain English explanations so you always know exactly what to do.</div>
                </div>
                <div class="feature-card">
                    <span class="feature-icon">🔄</span>
                    <div class="feature-title">ENDLESS PROGRAMS</div>
                    <div class="feature-desc">Finish your 4 weeks? Generate a new program instantly. Your history is always saved so you can track long term progress.</div>
                </div>
            </div>
        </div>

    </div>
    """, unsafe_allow_html=True)

    # CTA Button using Streamlit
    st.markdown("<div style='text-align:center; margin-top:-80vh; padding-bottom: 60vh;'>", unsafe_allow_html=True)
    if st.button("🚀 GET STARTED FREE", use_container_width=False, key="cta_btn"):
        st.session_state["page"] = "login"
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)