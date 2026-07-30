from pathlib import Path
import re

path = Path('index.html')
text = path.read_text(encoding='utf-8')

# Keep only two quick actions: today and favorites.
text = re.sub(
    r'<div class="today-actions" id="today-actions">.*?</div>\s*<div class="card nearest-card" id="nearest-meeting-card"></div>\s*<div class="ornament-divider"></div>',
    '''<div class="today-actions" id="today-actions">
            <button class="today-action" type="button" data-today-action="today"><span class="today-action-icon">📅</span><span id="quick-today-text">Найти собрание сегодня</span></button>
            <button class="today-action" type="button" data-today-action="favorites"><span class="today-action-icon">★</span><span id="quick-favorites-text">Мои группы</span></button>
        </div>''',
    text,
    count=1,
    flags=re.S,
)

# Two equal columns on the home screen.
text = text.replace('grid-template-columns:repeat(2,minmax(0,1fr)); gap:10px;', 'grid-template-columns:repeat(2,minmax(0,1fr)); gap:10px;', 1)

# Remove now-unused first-time modal markup.
text = re.sub(r'<div class="info-modal" id="first-time-modal".*?</div>\s*</div>\s*', '', text, count=1, flags=re.S)

# Remove first-time modal functions.
text = re.sub(r'\n    function openFirstTimeInfo\(\) \{.*?\n    \}\n\n    function closeFirstTimeInfo\(\) \{.*?\n    \}\n', '\n', text, count=1, flags=re.S)

# Remove references to deleted quick-action labels and nearest card.
for line in [
    "        document.getElementById('quick-call-text').innerText = d.quickCall;\n",
    "        document.getElementById('quick-first-text').innerText = d.quickFirst;\n",
    "        renderNearestMeeting();\n",
]:
    text = text.replace(line, '')

# Remove nearest-card event listener block.
text = re.sub(r"\n        document\.getElementById\('nearest-meeting-card'\)\.addEventListener\('click', event => \{.*?\n        \}\);", '', text, count=1, flags=re.S)

# Remove first-time action handling and call tracking.
text = text.replace("            if (action.dataset.todayAction === 'first') openFirstTimeInfo();\n", '')
text = text.replace("            if (action.dataset.todayAction === 'call') trackEvent('call', 'quick_aa_phone');\n", '')

# Remove first-time modal event listeners if present.
text = re.sub(r"\n        document\.getElementById\('first-time-modal-close'\).*?;", '', text)
text = re.sub(r"\n        document\.getElementById\('first-time-modal'\).*?;", '', text)
text = text.replace("document.addEventListener('keydown', event => { if (event.key === 'Escape') { closeNotificationCenter(); closeFirstTimeInfo(); } });", "document.addEventListener('keydown', event => { if (event.key === 'Escape') closeNotificationCenter(); });")

# Remove obsolete nearest-meeting functions.
text = re.sub(r'\n    function getUpcomingMeetings\(\) \{.*?\n    \}\n\n    function renderNearestMeeting\(\) \{.*?\n    \}\n', '\n', text, count=1, flags=re.S)

# Saving city no longer needs to render a removed card.
text = text.replace('        renderNearestMeeting();\n', '')

# Force service worker refresh.
text = re.sub(r"register\('sw\.js\?v=\d+'", "register('sw.js?v=5'", text, count=1)

path.write_text(text, encoding='utf-8')
