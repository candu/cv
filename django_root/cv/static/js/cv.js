(function(window, undefined) {

var History = window.History;

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
    if (!History.enabled) {
      throw 'History not enabled in this browser';
    }

    this.selected_tags = [];

    $$('.UITag').addEvent('click', function(event) {
      this.selectTag(event.target);
    }.bind(this));

    History.Adapter.bind(window, 'statechange', function() {
      var state = History.getState();
      var added_tags = state.data.tags.filter(function(name) {
        return !this.selected_tags.contains(name);
      }.bind(this));
      var removed_tags = this.selected_tags.filter(function(name) {
        return !state.data.tags.contains(name);
      });
      this.selected_tags = state.data.tags;
      added_tags.each(function(name) {
        this.addTag(this.getTagByName(name));
      }.bind(this));
      removed_tags.each(function(name) {
        this.removeTag(this.getTagByName(name));
      }.bind(this));
    }.bind(this));

    var path = document.location.pathname;
    var path_tags = path.substr(1).split('/');
    console.log(path_tags);
    for (var i = 0; i < path_tags.length; i++) {
      var name = path_tags[i];
      var tag = this.getTagByName(name);
      console.log(tag);
      if (tag == null) {
        continue;
      }
      if (!this.selected_tags.contains(name)) {
        this.selected_tags.push(name);
      }
      this.addTag(tag);
    }
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
      return !elem.getElements('.UITag').some(function(elem_tag) {
        return this.selected_tags.some(function(selected_tag) {
          return elem_tag.text == selected_tag;
        });
      }.bind(this));
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
  getTagByName : function(name) {
    var tag = $(document).getElement('.UITag:contains("' + name + '")');
    return tag;
  },
  addTag : function(tag) {
    var tag_id_class = tag.get('class').split(' ')[1];
    $$('.' + tag_id_class).addClass(
        'selected').removeEvents(
        'click').addEvent('click', function(event) {
      this.deselectTag(tag);
    }.bind(this));
    this.moveContentToLeft(tag);
    if (this.selected_tags.length > 0) {
      this.showLeftColumn();
    } 
  },
  removeTag : function(tag) {
    var tag_id_class = tag.get('class').split(' ')[1];
    $$('.' + tag_id_class).removeClass(
        'selected').removeEvents(
        'click').addEvent('click', function(event) {
      this.selectTag(tag);
      }.bind(this));  
    this.moveContentToRight();
    if (this.selected_tags.length == 0) {
      this.hideLeftColumn();
    }
  },
  pushState : function(new_tags) {
    History.pushState({ tags : new_tags }, '', '/' + new_tags.join('/'));
  },
  selectTag : function(tag) {
    var name = tag.text;
    if (this.selected_tags.contains(name)) {
      return;
    }
    var new_tags = Array.clone(this.selected_tags);
    new_tags.push(name);
    this.pushState(new_tags);
  },
  deselectTag : function(tag) {
    var name = tag.text;
    if (!this.selected_tags.contains(name)) {
      return;
    }
    var new_tags = Array.clone(this.selected_tags);
    new_tags.erase(name);
    this.pushState(new_tags);
  }
});

window.addEvent('domready', function(event) {
  new ContentManager();
  $$('a').set('target', '_blank');
});

})(window);
