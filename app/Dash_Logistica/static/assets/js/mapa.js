//Troca de Estados
var elements = document.getElementsByClassName("estado");
for (var i = 0; i < elements.length; i++) {
  elements[i].onclick = function () {
    var el = elements[0];
    while (el) {
      if (el.tagName === "a") {
        el.classList.remove("ativo");
      }
      el = el.nextSibling;
    }
    this.classList.add("ativo");
  };
}

//Box Responsivo
let viewport_meta = document.getElementsByClassName("node");
let svgmap_meta = document.getElementById("svg-map");
let viewport_set = function () {
  for (var i = 0; i < viewport_meta.length; i++) {
    if (screen.width > 768) {
      viewport_meta[i].setAttribute("x", "500");
      viewport_meta[i].setAttribute("y", "22");
      svgmap_meta.setAttribute("viewBox", "0 0 700 450");
    } else {
      viewport_meta[i].setAttribute("x", "22");
      viewport_meta[i].setAttribute("y", "500");
      svgmap_meta.setAttribute("viewBox", "0 0 450 700");
    }
  }
};
viewport_set();

window.onresize = function () {
  viewport_set();
};