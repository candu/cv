function toggle_tag(tag) {

}

window.addEvent('domready', function() {
  $$('.UITag').addEvent('click', function(event) {
    event.stop();
    event.target.toggleClass('enabled');
  });
  $$('.UITagGroup').addEvent('click', function(event) {
    event.stop();
    var group = event.target;
    if (group.hasClass('UITagGroupName')) {
      group = group.getParent();
    }
    group.getElements('.UITag').toggleClass('enabled');
  });
});
