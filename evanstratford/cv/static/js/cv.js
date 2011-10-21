var TagSet = new Class({
  initialize : function() {
    this.S = {};
    this.n = 0;
  },
  add : function(k) {
    if (k in this.S) {
      return;
    }
    this.S[k] = true;
    this.n++;
  },
  remove : function(k) {
    if (k in this.S) {
      delete this.S[k];
      this.n--;
    }
  },
  contains : function(k) {
    return k in this.S;
  },
  size : function() {
    return this.n;
  },
  empty : function() {
    return this.n == 0;
  }
});

var ContentManager = new Class({
  initialize : function() {
    this.selected_tags = new TagSet();
    $$('.UITag').addEvent('click', function(event) {
      this.selectTag(event.target);
    }.bind(this));
  },
  addTagToBar : function(tag) {
    $$('.UIControlsHeader').grab(
        tag.clone().fade('hide').fade('in').addEvent(
        'click', function(event) {
      this.deselectTag(event.target);
    }.bind(this)));
  },
  selectTag : function(tag) {
    var name = tag.text;
    console.log(tag);
    if (this.selected_tags.contains(name)) {
      return;
    }
    if (this.selected_tags.empty()) {
      var header = $$('.UIControlsHeader')[0];
      new Fx.Morph(header, {
        duration : 'short',
        onComplete : function() {
          this.addTagToBar(tag)
        }.bind(this)
      }).start({
        'height' : [0, 19]
      });
    } else {
      this.addTagToBar(tag);
    }
    this.selected_tags.add(name);
  },
  deselectTag : function(tag) {
    var name = tag.text;
    if (!this.selected_tags.contains(name)) {
      return;
    }
    this.selected_tags.remove(name);
    tag.fade('out').destroy();
    if (this.selected_tags.empty()) {
      var header = $$('.UIControlsHeader')[0];
      new Fx.Morph(header, {
        duration : 'short'
      }).start({
        'height' : [19, 0]
      });
    }
  }
});

window.addEvent('domready', function(event) {
    new ContentManager();
});
