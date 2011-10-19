window.addEvent('domready', function() {
  new Typeahead($$('.UITypeahead')[0], new DataSource()).listen();
});
