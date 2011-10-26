Fx.Multiplex = new Class({
  initialize : function(elements, options) {
    this.elements = elements;
    this.fx = new Fx.Elements(this.elements, options);
  },
  start : function(properties) {
    var obj = {};
    for (var i = 0; i < this.elements.length; i++) {
      obj[i] = properties;
    }
    this.fx.start(obj);
    return this;
  }
});

var EFFECT_DURATION = 200;

var ContentManager = new Class({
  initialize : function() {
    this.selected_tags = {};
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
  getContentDate : function(elem) {
    var s = elem.getElement('.UIContentDate').get('text');
    var t = s.split('to');
    return +(new Date(t[t.length-1]));
  },
  getContentID : function(elem) {
    var s = elem.get('id');
    var n = s.split('-')[1];
    return +n;
  },
  sortContents : function(elems) {
    var elementSort = new Fx.Sort(elems, {
      duration : EFFECT_DURATION,
      onComplete : function() {
        this.rearrangeDOM();
      }
    });
    var sorted = elems.sort(function(e1, e2) {
      var dt = this.getContentDate(e2) - this.getContentDate(e1);
      if (dt != 0) {
        return dt;
      }
      return this.getContentID(e2) - this.getContentID(e1);
    }.bind(this));
    elementSort.sortByElements(sorted);
  },
  moveContentToLeft : function(tag) {
    var name = tag.text;
    var elementsAtRight =
        $$('.UIRightRanked')[0].getElements('.UIContent');
    var elementsToMove = elementsAtRight.filter(function(elem) {
      return elem.getElements('.UITag').some(function(elem_tag) {
        return elem_tag.text == name;
      });
    });
    new Fx.Multiplex(elementsToMove, {
      duration : EFFECT_DURATION,
      onComplete : function() {
        $$('.UILeftRanked').adopt(elementsToMove);
        var elementsAtLeft =
            $$('.UILeftRanked')[0].getElements('.UIContent');
        this.sortContents(elementsAtLeft);
        new Fx.Multiplex(elementsToMove, {
          duration : EFFECT_DURATION
        }).start({
          'opacity' : [0, 1]
        });
      }.bind(this)
    }).start({
      'opacity' : [1, 0]
    });
  },
  moveContentToRight : function() {
    var elementsAtLeft =
        $$('.UILeftRanked')[0].getElements('.UIContent');
    var elementsToMove = elementsAtLeft.filter(function(elem) {
      var selected_tag_array = Object.keys(this.selected_tags);
      return !elem.getElements('.UITag').some(function(elem_tag) {
        return selected_tag_array.some(function(selected_tag) {
          return elem_tag.text == selected_tag;
        });
      });
    }.bind(this));
    new Fx.Multiplex(elementsToMove, {
      duration : EFFECT_DURATION,
      onComplete : function() {
        $$('.UIRightRanked').adopt(elementsToMove);
        var elementsAtRight =
            $$('.UIRightRanked')[0].getElements('.UIContent');
        this.sortContents(elementsAtRight);
        new Fx.Multiplex(elementsToMove, {
          duration : EFFECT_DURATION
        }).start({
          'opacity' : [0, 1]
        });
      }.bind(this)
    }).start({
      'opacity' : [1, 0]
    });
  },
  showLeftColumn : function() {
    var right = $$('.UIColumn.right')[0];
    right.setStyle('float', 'right');
    new Fx.Morph(right, {
      duration : EFFECT_DURATION,
      unit : '%',
    }).start({
      'width' : [100, 50]
    });
    var left = $$('.UIColumn.left')[0];
    new Fx.Morph(left, {
      duration : EFFECT_DURATION,
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
      duration : EFFECT_DURATION,
      unit : '%',
    }).start({
      'width' : [50, 100]
    });
    var left = $$('.UIColumn.left')[0];
    new Fx.Morph(left, {
      duration : EFFECT_DURATION,
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
    if (name in this.selected_tags) {
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
    if (Object.getLength(this.selected_tags) == 0) {
      this.showLeftColumn();
    } 
    this.selected_tags[name] = true;
  },
  deselectTag : function(tag) {
    var name = tag.text;
    if (!(name in this.selected_tags)) {
      return;
    }
    var tag_id_class = tag.get('class').split(' ')[1];
    $$('.UIControlsHeader').getChildren(
        '.' + tag_id_class).each(function(elem) {
      elem.destroy();
    });
    delete this.selected_tags[name];
    $$('.' + tag_id_class).removeClass(
        'selected').removeEvents(
        'click').addEvent('click', function(event) {
      this.selectTag(tag);
      }.bind(this));  
    this.moveContentToRight();
    if (Object.getLength(this.selected_tags) == 0) {
      this.hideLeftColumn();
    }
  }
});

var ContentHider = new Class({
  initialize : function() {
    $$('.UIContentMoreLess').addEvent('click', function(event) {
      var description = event.target.getSiblings('.UIContentDescription')[0];
      if (event.target.get('text') == 'Show more...') {
        description.getChildren('p').reveal();
        event.target.set('text', 'Show less');
      } else {
        description.getChildren('p').dissolve();
        event.target.set('text', 'Show more...');
      }
    });
  }
});

window.addEvent('domready', function(event) {
  new ContentManager();
  new ContentHider();
  $$('a').set('target', '_blank');
});
