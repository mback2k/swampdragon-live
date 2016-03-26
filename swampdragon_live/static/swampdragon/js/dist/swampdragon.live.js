swampdragon.open(function () {
  var nl = document.getElementsByClassName('swampdragon-live');
  for (var i = 0; i < nl.length; i++) {
    var n = nl[i];
    for (var j = 0; j < n.classList.length; j++) {
      var c = n.classList[j];
      if (c.lastIndexOf('swampdragon-live-', 0) === 0) {
        swampdragon.subscribe('swampdragon-live', c, {'key': c}, function (context, data) {
          swampdragon.onChannelMessage(function (channels, message) {
            for (var k = 0; k < channels.length; k++) {
              var c = channels[k];
              var ml = document.getElementsByClassName(c);
              for (var l = 0; l < ml.length; l++) {
                var m = ml[l];
                m.innerHTML = message.data;
              };
            };
          });
        }, function (context, data) {});
      };
    };
  };
});
