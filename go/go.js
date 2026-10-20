// Smart store link: /go/<app>/?src=<channel>
// iPhone/iPad -> App Store campaign link (ct=<src>), Android -> Google Play with utm_source=<src>,
// everything else -> the page itself with both store buttons carrying the same tags.
(function () {
  var script = document.currentScript;
  var params = new URLSearchParams(location.search);
  var src = (params.get('src') || 'direct').toLowerCase().replace(/[^a-z0-9_-]/g, '').slice(0, 40) || 'direct';

  var appStore = script.dataset.appStore + '&ct=' + src;
  var playId = script.dataset.play;
  var play = playId
    ? 'https://play.google.com/store/apps/details?id=' + playId +
      '&referrer=' + encodeURIComponent('utm_source=' + src + '&utm_medium=community')
    : null;

  var ua = navigator.userAgent;
  var isIOS = /iPhone|iPad|iPod/i.test(ua) || (navigator.platform === 'MacIntel' && navigator.maxTouchPoints > 1);
  var isAndroid = /Android/i.test(ua);

  if (isIOS) {
    location.replace(appStore);
    return;
  }
  if (isAndroid && play) {
    location.replace(play);
    return;
  }

  document.addEventListener('DOMContentLoaded', function () {
    document.getElementById('ios-cta').href = appStore;

    var android = document.getElementById('android-cta');
    if (play) {
      android.href = play;
    } else {
      android.hidden = true;
      document.getElementById('android-note').hidden = false;
    }
  });
})();
