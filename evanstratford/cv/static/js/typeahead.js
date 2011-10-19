var DataSource = new Class({
  initialize : function() {
    new Request.JSON({
      url : '/tags',
      method : 'get',
      onSuccess : function(data) {
        this.load(data);
      }.bind(this)
    }).send();
  },
  load : function(data) {
    this.tags = data;
  },
  match : function(value) {
    var matches = [];
    for (tag in this.tags) {
      if (tag.contains(value)) {
        matches.push([tag, this.tags[tag]]);
      }
    }
    matches.sort();
    return matches;
  }
});

var Dropdown = new Class({
  initialize : function(root, source) {
    this.root = root;
    this.source = source;
    this.size = 5;
    this.hide();
  },
  visible : function() {
    return !this.root.hasClass('hidden');
  },
  hide : function() {
    this.root.addClass('hidden');
  },
  show : function() {
    this.root.removeClass('hidden');
  },
  prev : function() {
    if (!this.visible()) return;
    if (this.selected == 0) this.selected = this.matches.length;
    this.selected--;
    this.redraw();
  },
  next : function() {
    if (!this.visible()) return;
    this.selected++;
    if (this.selected == this.matches.length) this.selected = 0;
    this.redraw();
  },
  redraw : function() {
    var start = Math.min(this.matches.length - this.size, this.selected);
    var end = start + this.size;
    for (var i = 0; i < this.matches.length; i++) {
      var elem = this.root.getFirst('#suggestion-' + i);
      if (i == this.selected) {
        elem.addClass('selected');
      } else {
        elem.removeClass('selected');
      }

      if (start <= i && i < end) {
        elem.removeClass('hidden');
      } else {
        elem.addClass('hidden');
      }
    }
  },
  select : function() {
    return this.selectByIndex(this.selected);
  },
  selectByIndex : function(index) {
    this.hide();
    return this.matches[index];
  },
  clear : function() {
    this.root.getChildren('.UITypeaheadSuggestion').each(function(elem) {
      elem.dispose();
    });
  },
  repopulate : function() {
    for (var i = 0; i < this.matches.length; i++) {
      var key = this.matches[i][0];
      var value = this.matches[i][1];
      var elem = new Element('div', {
        class : 'UITypeaheadSuggestion hidden',
        text : key,
        id : 'suggestion-' + i,
        value : value
      }).addEvent('click', function(event) {
        this.selectByIndex(i);
      }.bind(this));
      this.root.grab(elem);
    }
  },
  update : function(value) {
    if (value == '') {
      this.hide();
      return;
    }
    if (value == this.value) return;
    this.value = value;
    this.matches = this.source.match(value);
    if (!this.matches) {
      this.hide();
      return;
    }
    this.clear();
    this.repopulate();
    this.selected = 0;
    this.redraw();
    this.show();
  }
});

var Typeahead = new Class({
  initialize : function(root, source, callback) {
    this.input = root.getElement('.UITypeaheadInput')
    this.dropdown = new Dropdown(
        root.getElement('.UITypeaheadDropdown'), source);
    this.callback = callback;
  },
  listen : function() {
    this.input.addEvents({
      'focus' : function(event) {
        this.input.removeClass('inactive');
        if (this.input.value.contains('enter tag name')) {
          this.input.value = '';
        }
        if (this.input.value != '') {
          this.dropdown.show();
        }
      }.bind(this),
      'blur' : function(event) {
        this.input.addClass('inactive');
        if (this.input.value == '') {
          this.input.value = 'enter tag name';
        }
        this.dropdown.hide();
      }.bind(this),
      'keyup' : function(event) {
        this.dropdown.update(this.input.value);
      }.bind(this),
      'keydown' : function(event) {
        switch (event.key) {
          case 'up':    this.dropdown.prev(); break;
          case 'down':  this.dropdown.next(); break;
          case 'enter':
            var selected = this.dropdown.select();
            this.input.value = selected[0];
            this.callback(selected[1]);
            break;
        }
      }.bind(this)
    });
  },
});

var TypeaheadActor = new Class({
  initialize : function(side, otherSide) {
    this.side = side;
    this.otherSide = otherSide;
    this.cache = {}
  },
  load : function(id) {
    if (id in this.cache) {
      this.act(id);
      return;
    }
    // TODO: this should block the typeahead until it's done...
    new Request.JSON({
      url : '/similar_content/' + id,
      method : 'get',
      onSuccess : function(data) {
        this.cache[id] = data;
        this.act(id);
      }.bind(this)
    }).send();
  },
  act : function(id) {
    var data = this.cache[id];
    $$('.UIActivity').each(function(elem) {
      var activityID = elem.id.substring('activity-'.length);
      var mySimilarity = data.similarity[activityID];
      elem.set('similarity-' + this.side, mySimilarity);
      var otherSimilarity = elem.get('similarity-' + this.otherSide);
      if (otherSimilarity == null) {
        otherSimilarity = 0;
      } else {
        otherSimilarity = parseFloat(otherSimilarity);
      }
      if (mySimilarity > otherSimilarity) {
        elem.removeClass(this.otherSide).addClass(this.side);
      } else {
        elem.removeClass(this.side).addClass(this.otherSide);
      }
    }.bind(this));
  }
});
