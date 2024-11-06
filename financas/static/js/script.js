
document.addEventListener("DOMContentLoaded", function() {
  console.log("JavaScript carregado!");

  function toggleDropdown() {
    const dropdown = document.getElementById("dropdownContent");
    dropdown.style.display = dropdown.style.display === "none" ? "block" : "none";
  }

  function toggleExpand() {
    const component = document.getElementById("contasCartoesComponent");
    const icon = document.getElementById("buttonIcon");
    component.classList.toggle("expanded");
    icon.classList.toggle("rotated");
  }

  window.toggleDropdown = toggleDropdown;
  window.toggleExpand = toggleExpand;
});
