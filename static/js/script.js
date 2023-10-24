const body = document.querySelector('body'),
sidebar = body.querySelector('nav'),
toggle = body.querySelector(".toggle"),
modeSwitch = body.querySelector(".toggle-switch"),
modeText = body.querySelector(".mode-text");
toggle.addEventListener("click", () => {
sidebar.classList.toggle("close");
})
modeSwitch.addEventListener("click", () => {
body.classList.toggle("dark");
if (body.classList.contains("dark")) {
  modeText.innerText = "Light mode";
} else {
  modeText.innerText = "Dark mode";
}
});
window.onload = function() {
  var navLinks = document.querySelectorAll('.nav-link a');

  for (var i = 0; i < navLinks.length; i++) {
    navLinks[i].addEventListener('click', function(e) {
      e.preventDefault();

      var currentTab = document.querySelector('.tab-content:not([style*="display: none"])');
      if (currentTab) {
        currentTab.style.display = 'none';
      }

      var newTab = document.getElementById(this.dataset.tab);
      if (newTab) {
        newTab.style.display = 'block';
      }
    });
  }
}
