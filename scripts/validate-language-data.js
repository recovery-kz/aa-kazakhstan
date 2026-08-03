const fs = require('fs');
const vm = require('vm');

const context = { window: {} };
vm.createContext(context);

for (const file of ['i18n.js', 'principles.js']) {
    vm.runInContext(fs.readFileSync(file, 'utf8'), context, { filename: file });
}

const languages = ['ru', 'kz', 'en'];
const i18n = context.window.AA_I18N;
const principles = context.window.AA_PRINCIPLES;
const errors = [];

for (const language of languages) {
    if (!i18n || !i18n[language]) errors.push(`missing interface language: ${language}`);
    if (!principles || !principles[language]) errors.push(`missing principles language: ${language}`);
}

if (i18n && i18n.ru) {
    const requiredKeys = Object.keys(i18n.ru);
    for (const language of languages.slice(1)) {
        const data = i18n[language] || {};
        for (const key of requiredKeys) {
            if (!(key in data)) errors.push(`${language}: missing interface label: ${key}`);
        }
    }
}

for (const language of languages) {
    const data = principles && principles[language];
    if (!data) continue;
    for (const section of ['steps', 'traditions', 'concepts']) {
        if (!data[section] || !Array.isArray(data[section].items)) {
            errors.push(`${language}: missing ${section}`);
            continue;
        }
        if (data[section].items.length !== 12) {
            errors.push(`${language}: ${section} has ${data[section].items.length} items instead of 12`);
        }
    }
}

if (errors.length) {
    console.error(errors.map(error => `ERROR: ${error}`).join('\n'));
    process.exit(1);
}

console.log('OK: required labels and 36 AA principles exist in ru, kz and en');
