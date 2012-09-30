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
    for (var i = 0; i < path_tags.length; i++) {
      var name = path_tags[i];
      var tag = this.getTagByName(name);
      if (tag == null) {
        continue;
      }
      if (!this.selected_tags.contains(name)) {
        this.selected_tags.push(name);
      }
      this.addTag(tag);
    }
  },
  stableNow : +(new Date()),
  dateCache : {},
  getContentDate : function(elem) {
    var elem_id = elem.get('id');
    if (!(elem_id in this.dateCache)) {
      var s = elem.getElement('.UIContentDate').get('text');
      var t = s.split(' to ');
      var started = +(new Date(t[0]));
      if (t.length == 1) {
        this.dateCache[elem_id] = [started, started];
      } else if (t[1] == 'present') {
        this.dateCache[elem_id] = [started, this.stableNow];
      } else {
        var finished = +(new Date(t[1]));
        this.dateCache[elem_id] = [started, finished];
      }
    }
    return this.dateCache[elem_id];
  },
  sortContents : function(elems) {
    var elementSort = new Fx.Sort(elems, {
      duration : EFFECT_DURATION,
      onComplete : function() {
        this.rearrangeDOM();
      }
    });
    var sorted = elems.sort(function(e1, e2) {
      var date1 = this.getContentDate(e1);
      var date2 = this.getContentDate(e2);
      date1.push(e1.get('id'));
      date2.push(e2.get('id'));
      if (date2 < date1) {
        return -1;
      }
      if (date2 > date1) {
        return 1;
      }
      return 0;
    }.bind(this));
    elementSort.sortByElements(sorted);
  },
  moveContentToTop : function(tag) {
    var name = tag.text;
    var elementsAtBottom =
        $$('.UIBottomRanked')[0].getElements('.UIContent');
    var elementsToMove = elementsAtBottom.filter(function(elem) {
      return elem.getElements('.UITag').some(function(elem_tag) {
        return elem_tag.text == name;
      });
    });
    new Fx.Multiplex(elementsToMove, {
      duration : EFFECT_DURATION,
      onComplete : function() {
        $$('.UITopRanked').adopt(elementsToMove);
        var elementsAtTop =
            $$('.UITopRanked')[0].getElements('.UIContent');
        this.sortContents(elementsAtTop);
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
  moveContentToBottom : function() {
    var elementsAtTop =
        $$('.UITopRanked')[0].getElements('.UIContent');
    var elementsToMove = elementsAtTop.filter(function(elem) {
      return !elem.getElements('.UITag').some(function(elem_tag) {
        return this.selected_tags.some(function(selected_tag) {
          return elem_tag.text == selected_tag;
        });
      }.bind(this));
    }.bind(this));
    new Fx.Multiplex(elementsToMove, {
      duration : EFFECT_DURATION,
      onComplete : function() {
        $$('.UIBottomRanked').adopt(elementsToMove);
        var elementsAtBottom =
            $$('.UIBottomRanked')[0].getElements('.UIContent');
        this.sortContents(elementsAtBottom);
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
    this.moveContentToTop(tag);
  },
  removeTag : function(tag) {
    var tag_id_class = tag.get('class').split(' ')[1];
    $$('.' + tag_id_class).removeClass(
        'selected').removeEvents(
        'click').addEvent('click', function(event) {
      this.selectTag(tag);
      }.bind(this));  
    this.moveContentToBottom();
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
});

})(window);
