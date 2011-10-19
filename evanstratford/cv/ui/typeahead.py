from xhpy.pylib import *

class :ui:typeahead(:x:element):
  def render(self):
    return \
    <div class="UITypeahead">
      <input class="UITypeaheadInput inactive" value="enter tag name" autocomplete="off" />
      <div class="UITypeaheadDropdown hidden">
        <div class="UITypeaheadSuggestions" />
        <div class="UITypeaheadSuggestionCount" />
      </div>
    </div>
