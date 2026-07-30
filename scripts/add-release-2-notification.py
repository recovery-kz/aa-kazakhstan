from pathlib import Path

app_path = Path('app.js')
app = app_path.read_text(encoding='utf-8')

needle = """        renderLit();
        updateFreshnessDisplay();
        localStorage.setItem('aa_first_run_done_v1', '1');
"""
replacement = """        renderLit();
        updateFreshnessDisplay();

        const releaseNotificationKey = 'release:2.0';
        if (!notificationSeen(releaseNotificationKey)) {
            const releaseTitle = curLang === 'kz'
                ? 'Қазақстан АА қолданбасының 2.0 нұсқасы шықты'
                : 'Вышла версия приложения АА Казахстана 2.0';
            const releaseText = curLang === 'kz'
                ? 'Жаңа навигация, ірі мәтін, топтардың жаңа түймелері, хабарламалар, сақтық көшірме және басқа өзгерістер.'
                : 'Новая навигация, крупный текст, новые кнопки групп, уведомления, резервная копия и другие изменения.';
            const releaseItems = getInternalNotifications();
            releaseItems.unshift({
                key: releaseNotificationKey,
                id: releaseNotificationKey,
                type: 'news',
                icon: '🎉',
                title: releaseTitle,
                text: releaseText,
                tab: 'news',
                createdAt: Date.now(),
                read: false
            });
            saveInternalNotifications(releaseItems);
            markNotificationSeen(releaseNotificationKey);
            localStorage.setItem('aa_last_news_identity', 'release-2-0-ru');
            updateNotificationBadge();
        }

        localStorage.setItem('aa_first_run_done_v1', '1');
"""

if needle not in app:
    raise SystemExit('init insertion point not found')
app = app.replace(needle, replacement, 1)
app_path.write_text(app, encoding='utf-8')

index_path = Path('index.html')
index = index_path.read_text(encoding='utf-8')
index = index.replace('app.js?v=2.0.1', 'app.js?v=2.0.2')
index = index.replace('i18n.js?v=2.0.1', 'i18n.js?v=2.0.2')
index = index.replace('styles.css?v=2.0.1', 'styles.css?v=2.0.2')
index_path.write_text(index, encoding='utf-8')
