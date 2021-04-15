window.Superlists = {}; // в явном виде объявляем объект свойством глобальной переменной window
window.Superlists.initialize = function() {
  $('input[name="text"]').on('keypress', function() {
    $('.has-error').hide(); // делаем функцию initialize атрибутом объекта Superlists
  });
};
