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

    showQrCode(location.origin + location.pathname + '?src=' + src);
  });

  // Desktop only: a QR of this same link, so a phone scan lands in the right store with the tag.
  // The ~56 KB generator (qrcode-generator, MIT) is loaded here, never on phones.
  function showQrCode(url) {
    var lib = document.createElement('script');
    lib.src = '/go/qrcode.js';
    lib.onload = function () {
      var qr = qrcode(0, 'M');
      qr.addData(url);
      qr.make();

      document.getElementById('qr-code').innerHTML = qr.createSvgTag({ cellSize: 4, margin: 0, scalable: true });
      document.getElementById('qr').hidden = false;
    };
    document.head.appendChild(lib);
  }
})();
