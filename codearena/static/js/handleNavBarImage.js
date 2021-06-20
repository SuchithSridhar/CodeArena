function onResize() {
  var w = document.documentElement.clientWidth;
  var h = document.documentElement.clientHeight;

  var mobile = document.querySelectorAll(".mobile-content");
  var desktop = document.querySelectorAll(".desktop-content");

  if (w <= 991) {
    for (var i = 0; i < mobile.length; i++) {
      mobile[i].style.display = "block";
    }
    for (var i = 0; i < desktop.length; i++) {
      desktop[i].style.display = "none";
    }
  } else {
    for (var i = 0; i < mobile.length; i++) {
      mobile[i].style.display = "none";
    }
    for (var i = 0; i < desktop.length; i++) {
      desktop[i].style.display = "block";
    }
  }
}

window.addEventListener("resize", onResize);
onResize();

var notifications = document.querySelectorAll(".notification");
for (var i = 0; i < notifications.length; i++) {
  notifications[i].onclick = (e) => {
    e.target.style.display = "none";
  };
}
