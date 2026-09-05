import re

file_path = "/Users/macbook_uz/Documents/mirzo_yusuf_masjidi/admin.html"
with open(file_path, "r", encoding="utf-8") as f:
    html = f.read()

# 1. Update CSS
css_old = "@media(max-width:768px) { .sidebar{width:100%;height:auto;position:relative;} .main-content{margin-left:0;padding:16px;} }"
css_new = """    .sidebar-overlay { display: none; position: fixed; inset: 0; background: rgba(0,0,0,0.6); z-index: 1000; opacity: 0; transition: opacity 0.3s ease; pointer-events: none; backdrop-filter: blur(2px); }
    .sidebar-overlay.open { opacity: 1; pointer-events: auto; }
    .top-bar-mobile { display: none; align-items: center; justify-content: space-between; background: var(--surface); padding: 12px 16px; position: fixed; top: 0; left: 0; right: 0; z-index: 900; border-bottom: 1px solid rgba(212,160,23,0.1); }
    .hamburger { cursor: pointer; color: var(--gold); background: none; border: none; display: flex; flex-direction: column; gap: 4px; padding: 4px; }
    .hamburger span { width: 24px; height: 2px; background: currentColor; border-radius: 2px; }
    .mobile-brand { font-size: 0.9rem; font-weight: 800; color: var(--gold); display: flex; align-items: center; gap: 6px; }
    @media(max-width:768px) {
      .sidebar { transform: translateX(-100%); transition: transform 0.3s ease; box-shadow: 4px 0 20px rgba(0,0,0,0.8); z-index: 1001; }
      .sidebar.open { transform: translateX(0); }
      .main-content { margin-left: 0; padding: 16px; padding-top: 70px; }
      .top-bar-mobile { display: flex; }
      @media(max-width:768px) { .sidebar-overlay { display: block; } }
    }"""
html = html.replace(css_old, css_new)

# 2. Add Mobile Top Bar and Overlay right after <div id="admin-layout">
layout_old = '<div id="admin-layout">\n  <aside class="sidebar">'
layout_new = """<div id="admin-layout">
  <div class="sidebar-overlay" onclick="toggleSidebar()"></div>
  <div class="top-bar-mobile">
    <div class="mobile-brand">
      <span class="material-symbols-outlined" style="font-size:20px;">mosque</span>
      MIRZA YUSUF
    </div>
    <button class="hamburger" onclick="toggleSidebar()">
      <span></span><span></span><span></span>
    </button>
  </div>
  <aside class="sidebar" id="sidebar">"""
html = html.replace(layout_old, layout_new)

# 3. Add toggleSidebar() to scripts
script_insertion = """</script>
<script>
function toggleSidebar() {
  const sb = document.getElementById('sidebar');
  const ov = document.querySelector('.sidebar-overlay');
  sb.classList.toggle('open');
  ov.classList.toggle('open');
}
"""
html = html.replace("</script>", script_insertion, 1) # Only first occurrence, wait, not good.
# Let's insert at the very beginning of the script block
script_start = "<script>\n"
html = html.replace(script_start, script_start + """
function toggleSidebar() {
  const sb = document.getElementById('sidebar');
  const ov = document.querySelector('.sidebar-overlay');
  if(sb) sb.classList.toggle('open');
  if(ov) ov.classList.toggle('open');
}
""", 1)


# 4. Update Login Card HTML
login_old = """    <div class="card" id="login-card">
      <div class="logo">
        <span class="material-symbols-outlined">mosque</span>
        <h1>MIRZA YUSUF MASJIDI</h1>
        <p>Admin boshqaruv paneli — faqat vakolatli xodimlar</p>
      </div>
      <label>PAROL</label>
      <input type="password" id="login-password" placeholder="••••••••" autocomplete="current-password" onkeydown="if(event.key==='Enter') doLogin()">
      <button class="btn" id="login-btn" onclick="doLogin()">
        <span class="material-symbols-outlined">login</span> Kirish
      </button>
      <div class="msg error" id="login-err"><span class="material-symbols-outlined">error</span> Parol noto'g'ri.</div>
    </div>"""

login_new = """    <div class="card" id="login-card">
      <div class="logo">
        <span class="material-symbols-outlined">mosque</span>
        <h1>MIRZA YUSUF MASJIDI</h1>
        <p>Admin boshqaruv paneli — faqat vakolatli xodimlar</p>
      </div>
      
      <div id="step1">
        <label>USERNAME</label>
        <input type="text" id="username" placeholder="Admin username..." onkeydown="if(event.key==='Enter') doLogin()">
        <button class="btn" id="login-btn" onclick="doLogin()">
          <span class="material-symbols-outlined">login</span> Davom etish
        </button>
      </div>

      <div id="step2" style="display:none">
        <label>TASDIQLASH KODI (TG)</label>
        <input type="number" id="tgcode" placeholder="4 xonali kod..." onkeydown="if(event.key==='Enter') verifyCode()">
        <button class="btn" onclick="verifyCode()">
          <span class="material-symbols-outlined">check_circle</span> Tasdiqlash va Kirish
        </button>
      </div>

      <div class="msg error" id="login-err"><span class="material-symbols-outlined">error</span> Xato username yoki kod.</div>
    </div>"""

html = html.replace(login_old, login_new)


# 5. Replace doLogin() JS logic
js_login_old = """// ================= LOGIN =================
function doLogin() {
  const p = document.getElementById('login-password').value;
  if(p === 'masjid2026') {
    localStorage.setItem('admin_session', 'ok');
    document.getElementById('login-screen').style.display = 'none';
    document.getElementById('admin-layout').style.display = 'flex';
    initAdmin();
  } else {
    document.getElementById('login-err').classList.add('show');
    setTimeout(()=>document.getElementById('login-err').classList.remove('show'),3000);
  }
}
if(localStorage.getItem('admin_session') === 'ok') {
  document.getElementById('login-screen').style.display = 'none';
  document.getElementById('admin-layout').style.display = 'flex';
  initAdmin();
}"""

js_login_new = """// ================= LOGIN & 2FA =================
const ADMIN_USERS = {
  'azizbek': '822033965' // Telegram ID. Kerak bo'lsa shunga qo'shib ketaverasiz
};

let generatedTgCode = null;
let tgCodeTimeout = null;

function doLogin() {
  const un = document.getElementById('username').value.trim().toLowerCase();
  const chatId = ADMIN_USERS[un];
  
  const errEl = document.getElementById('login-err');
  
  if (chatId) {
    generatedTgCode = Math.floor(1000 + Math.random() * 9000).toString();
    // Bot token
    const token = window.MIRZO_YUSUF_BOT_TOKEN;
    const tgText = `🔐 Mirza Yusuf Admin paneliga kirish uchun tasdiqlash kodi: ${generatedTgCode}\\n\\nAgar bu siz bo\`lmasangiz, e'tibor bermang.`;
    
    fetch(`https://api.telegram.org/bot${token}/sendMessage`, {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({ chat_id: chatId, text: tgText })
    }).catch(e => console.error("TG Send Error:", e));

    if (tgCodeTimeout) clearTimeout(tgCodeTimeout);
    tgCodeTimeout = setTimeout(() => { generatedTgCode = null; document.getElementById('tgcode').value = ''; }, 120000);

    document.getElementById('step1').style.display = 'none';
    document.getElementById('step2').style.display = 'block';
    errEl.classList.remove('show');
  } else {
    errEl.innerHTML = '<span class="material-symbols-outlined">error</span> Noto`g`ri username!';
    errEl.classList.add('show');
  }
}

function verifyCode() {
  const errEl = document.getElementById('login-err');
  if (!generatedTgCode) {
    errEl.innerHTML = '<span class="material-symbols-outlined">error</span> Kod muddati tugagan!';
    errEl.classList.add('show');
    return;
  }
  if (document.getElementById('tgcode').value === generatedTgCode) {
    if (tgCodeTimeout) clearTimeout(tgCodeTimeout);
    generatedTgCode = null;
    const sessionToken = Date.now() + '.' + Math.random().toString(36).substring(2, 10);
    localStorage.setItem('admin_session', sessionToken);
    
    document.getElementById('login-screen').style.display = 'none';
    document.getElementById('admin-layout').style.display = 'flex';
    initAdmin();
  } else {
    errEl.innerHTML = '<span class="material-symbols-outlined">error</span> Noto`g`ri kod!';
    errEl.classList.add('show');
  }
}

// Check session
const session = localStorage.getItem('admin_session');
if (session && session.includes('.')) {
  const ts = parseInt(session.split('.')[0]);
  if (!isNaN(ts) && Date.now() - ts < 24 * 60 * 60 * 1000) {
    document.getElementById('login-screen').style.display = 'none';
    document.getElementById('admin-layout').style.display = 'flex';
    initAdmin();
  } else {
    localStorage.removeItem('admin_session');
  }
}"""

html = html.replace(js_login_old, js_login_new)

# Add auto-close sidebar logic when a nav link is clicked on mobile
nav_links_old = "document.querySelectorAll('.sidebar-nav .nav-item').forEach(btn => {"
nav_links_new = """document.querySelectorAll('.sidebar-nav .nav-item').forEach(btn => {
    btn.addEventListener('click', () => {
      if(window.innerWidth <= 768) {
         document.getElementById('sidebar').classList.remove('open');
         document.querySelector('.sidebar-overlay').classList.remove('open');
      }
    });"""
html = html.replace(nav_links_old, nav_links_new)


with open(file_path, "w", encoding="utf-8") as f:
    f.write(html)
print("Changes applied successfully!")
