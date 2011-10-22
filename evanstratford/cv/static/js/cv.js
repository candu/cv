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
  },
  toArray : function() {
    var a = [];
    for (k in this.S) {
      a.push(k);
    }
    return a;
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
    var name = tag.text;
    $$('.UIControlsHeader').grab(
        tag.clone().fade('hide').fade('in').addEvent(
        'click', function(event) {
      this.deselectTag(event.target);
    }.bind(this)));
  },
  moveContentToLeft : function(tag) {
    var name = tag.text;
    var elementsAtRight =
        $$('.UIRightRanked')[0].getElements('.UIContent');
    var elementsToMove = elementsAtRight.filter(function(elem) {
      var matchFound = false;
      elem.getElements('.UITag').each(function(elem_tag) {
        if (elem_tag.text == name) {
          matchFound = true;
        }
      });
      return matchFound;
    });
    elementsToMove.each(function(elem) {
      new Fx.Morph(elem, {
        duration : 'short',
        onComplete : function() {
          $$('.UILeftRanked').grab(elem);
          new Fx.Morph(elem, {
            duration : 'short'
          }).start({
            'opacity' : [0.0, 1.0]
          });
        }.bind(this)
      }).start({
        'opacity' : [1.0, 0.0]
      });
    });
  },
  moveContentToRight : function() {
    var elementsAtLeft =
        $$('.UILeftRanked')[0].getElements('.UIContent');
    var elementsToMove = elementsAtLeft.filter(function(elem) {
      var matchFound = false;
      elem.getElements('.UITag').each(function(elem_tag) {
        this.selected_tags.toArray().each(function(selected_tag) {
          if (elem_tag.text == selected_tag) {
            matchFound = true;
          }
        }.bind(this));
      }.bind(this));
      return !matchFound;
    }.bind(this));
    elementsToMove.each(function(elem) {
      new Fx.Morph(elem, {
        duration : 'short',
        onComplete : function() {
          $$('.UIRightRanked').grab(elem);
          new Fx.Morph(elem, {
            duration : 'short'
          }).start({
            'opacity' : [0.0, 1.0]
          });
        }.bind(this)
      }).start({
        'opacity' : [1.0, 0.0]
      });
    });
  },
  showLeftColumn : function() {
    var right = $$('.UIColumn.right')[0];
    right.setStyle('float', 'right');
    new Fx.Morph(right, {
      duration : 'short',
      unit : '%',
    }).start({
      'width' : [100, 50]
    });
    var left = $$('.UIColumn.left')[0];
    new Fx.Morph(left, {
      duration : 'short',
      unit : '%',
      onComplete : function() {
        right.setStyle('float', 'none');
      }
    }).start({
      'width' : [0, 50]
    });
  },
  hideLeftColumn : function() {
    var right = $$('.UIColumn.right')[0];
    right.setStyle('float', 'right');
    new Fx.Morph(right, {
      duration : 'short',
      unit : '%',
    }).start({
      'width' : [50, 100]
    });
    var left = $$('.UIColumn.left')[0];
    new Fx.Morph(left, {
      duration : 'short',
      unit : '%',
      onComplete : function() {
        right.setStyle('float', 'none');
      }
    }).start({
      'width' : [50, 0]
    });
  },
  selectTag : function(tag) {
    var name = tag.text;
    if (this.selected_tags.contains(name)) {
      return;
    }
    this.addTagToBar(tag);
    var tag_id_class = tag.get('class').split(' ')[1];
    $$('.' + tag_id_class).addClass(
        'selected').removeEvents(
        'click').addEvent('click', function(event) {
      this.deselectTag(tag);
    }.bind(this));
    this.moveContentToLeft(tag);
    if (this.selected_tags.empty()) {
      this.showLeftColumn();
    } 
    this.selected_tags.add(name);
  },
  deselectTag : function(tag) {
    var name = tag.text;
    if (!this.selected_tags.contains(name)) {
      return;
    }
    var tag_id_class = tag.get('class').split(' ')[1];
    $$('.UIControlsHeader').getChildren(
        '.' + tag_id_class).each(function(elem) {
      elem.destroy();
    });
    this.selected_tags.remove(name);
    $$('.' + tag_id_class).removeClass(
        'selected').removeEvents(
        'click').addEvent('click', function(event) {
      this.selectTag(tag);
      }.bind(this));  
    this.moveContentToRight();
    if (this.selected_tags.empty()) {
      this.hideLeftColumn();
    }
  }
});

window.addEvent('domready', function(event) {
    new ContentManager();
});
