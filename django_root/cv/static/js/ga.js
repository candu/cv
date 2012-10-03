var _gaq = _gaq || [];
var parentDomain = document.domain.split('.').slice(-2).join('.');
_gaq.push(['_setAccount', 'UA-35288721-1']);
_gaq.push(['_setDomainName', parentDomain]);
_gaq.push(['_trackPageview']);

(function() {
  var ga = document.createElement('script'); ga.type = 'text/javascript'; ga.async = true;
  ga.src = ('https:' == document.location.protocol ? 'https://ssl' : 'http://www') + '.google-analytics.com/ga.js';
  var s = document.getElementsByTagName('script')[0]; s.parentNode.insertBefore(ga, s);
})();
