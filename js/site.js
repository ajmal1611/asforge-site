/* AS Forge site settings. Edit the values below, nothing else is needed. */
(function () {
  var CONFIG = {
    // Where the Windows installer lives. Now: Google Drive direct link. Later: your GitHub Releases link.
    downloadUrl: "https://github.com/ajmal1611/as-fetchly/releases/latest/download/AS-Fetchly-Setup.exe",    version: "0.8.0",
    whatsapp: "https://wa.me/923211478590",
    email: "hello@asforge.app"
  };
  function each(sel, fn) { Array.prototype.forEach.call(document.querySelectorAll(sel), fn); }
  each("[data-dl]", function (a) { a.href = CONFIG.downloadUrl; a.rel = "noopener"; });
  each("[data-wa]", function (a) { a.href = CONFIG.whatsapp; a.rel = "noopener"; });
  each("[data-mail]", function (a) { a.href = "mailto:" + CONFIG.email; });
  each("[data-ver]", function (s) { s.textContent = CONFIG.version; });
  each("[data-year]", function (s) { s.textContent = new Date().getFullYear(); });
})();
