document.addEventListener('DOMContentLoaded', function() {
  var tabItems = document.querySelectorAll('.tab-item');

  tabItems.forEach(function(tab) {
    tab.addEventListener('click', function() {
      var tabId = this.getAttribute('data-tab');
      var content = document.getElementById(tabId);

      // Удаляем активный класс у текущих вкладок и контента
      document.querySelector('.tab-item.active').classList.remove('active');
      document.querySelector('.tab-pane.active').classList.remove('active');

      // Добавляем активный класс для выбранной вкладки и контента
      this.classList.add('active');
      content.classList.add('active');
    });
  });
});