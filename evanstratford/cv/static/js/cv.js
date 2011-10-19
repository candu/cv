window.addEvent('domready', function() {
  var leftActor = new TypeaheadActor('left');
  var rightActor = new TypeaheadActor('right');
  // TODO: chain these, since actor should load entire EMIM map
  new Typeahead($$('.UITypeahead')[0], new DataSource(), function(id) {
    leftActor.load(id);
  }).listen();
  new Typeahead($$('.UITypeahead')[1], new DataSource(), function(id) {
    rightActor.load(id);
  }).listen();
  redraw();
});
