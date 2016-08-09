/* Common JS/JQuery functions */

// Swap icon
function toggleIcon(id, toggleA, toggleB) {
  if ($(id).hasClass(toggleA)) {
    $(id).removeClass(toggleA).addClass(toggleB);
  } else if ($(id).hasClass(toggleB)) {
    $(id).removeClass(toggleB).addClass(toggleA);
  };
}

function toggleFromList(id, fromClassList, toClass) {
  for (i=0; i < fromClassList.length; i++) {
    fromClass = fromClassList[i];
    if (fromClass != toClass) {
      if ($(id).hasClass(fromClass)) {
        $(id).removeClass(fromClass).addClass(toClass);
      };
    };
  };
}

/* Common click control configurations */
// GET url only
function buttonControlBasic(id) {
  $(id).click(function() {
    var url = this.href;
    console.log(url);
    $.get(url);
    return false;
  });
}

// GET url and toggle icon
function buttonControlToggle(id, iconA, iconB) {
  $(id).click(function() {
    var url = this.href;
    var icon = $(this).find('.fa')
    console.log(url);
    $.get(url, function() {
      toggleIcon(icon, iconA, iconB);
    });
    return false;
  });
}

function statusButtonToggle(config, icon, button) {
  var fromIconList = ['fa-question-circle', 'fa-refresh fa-spin', 'fa-exclamation-circle', 'fa-check'];
  var fromButtonList = ['btn-danger','btn-warning','btn-success','btn-primary'];
  if(config == 0) {
    // Unknown (initial value)
    toggleFromList(icon, fromIconList, 'fa-question-circle');
    toggleFromList(button, fromButtonList, 'btn-primary');
  }
  if(config == 1) {
    // Success
    toggleFromList(icon, fromIconList, 'fa-check');
    toggleFromList(button, fromButtonList, 'btn-success');
  }
  else if(config == 2) {
    // Pending
    toggleFromList(icon, fromIconList, 'fa-refresh fa-spin');
    toggleFromList(button, fromButtonList, 'btn-warning');
  }
  else if(config == 3) {
    // Fail
    toggleFromList(icon, fromIconList, 'fa-exclamation-circle');
    toggleFromList(button, fromButtonList, 'btn-danger');
  }
}
