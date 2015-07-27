var i18n = require('jquery-i18n'),
COOKIE_NAME = 'locale',
DEFAULT_LOCALE = 'en',
LOCALES = {
  'zh-cn': '中文(简体)',
  'en': 'English',
  'id': 'Indonesia'
},
ALL_LOCALES = Object.keys(LOCALES);

var detect = function() { 
  return DEFAULT_LOCALE;
};

i18n.detect = detect;

i18n.locale = detect();

i18n.fetch = function(domain) {
  return $.getJSON("/locales/" + i18n.locale + "/" + domain + ".json", function(res) {
    i18n.load(res);
    return;
  });
};

module.exports = i18n;