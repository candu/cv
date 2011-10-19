var DataSource = new Class({
  initialize : function() {
  },
  match : function(value) {
    var a = ['foo'];
    for (var i = 0; i < value.length; i++) {
      a.push(i);
    }
    return a;
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
      var elem = $('suggestion-' + i);
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
    return $('suggestion-' + index).get('text');
  },
  clear : function() {
    this.root.getChildren('.UITypeaheadSuggestion').each(function(elem) {
      elem.dispose();
    });
  },
  repopulate : function() {
    for (var i = 0; i < this.matches.length; i++) {
      var elem = new Element('div', {
        class : 'UITypeaheadSuggestion hidden',
        text : this.matches[i],
        id : 'suggestion-' + i
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
    if (this.matches.length == 0) this.hide();
    this.clear();
    this.repopulate();
    this.selected = 0;
    this.redraw();
    this.show();
  }
});

var Typeahead = new Class({
  initialize : function(root, source) {
    this.input = root.getElement('.UITypeaheadInput')
    this.dropdown = new Dropdown(
        root.getElement('.UITypeaheadDropdown'), source);
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
          case 'enter': this.input.value = this.dropdown.select(); break;
        }
      }.bind(this)
    });
  },
});
