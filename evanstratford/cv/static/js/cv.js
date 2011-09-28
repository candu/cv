var TimelineController = {
};

window.addEvent('domready', function() {
  $$('.UITag').addEvent('click', function(event) {
    event.stop();
    event.target.toggleClass('enabled');
  });
});
