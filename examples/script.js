
$(function() {
  // Hide all lists except the outermost.
  $('ul.tree ul').hide();

  $('.tree li > ul').each(function(i) {
    var $subUl = $(this);
    var $parentLi = $subUl.parent('li');
    var $toggleIcon = '<i class="js-toggle-icon">+</i>';

    $parentLi.addClass('has-children');
    
    $parentLi.prepend( $toggleIcon ).find('.js-toggle-icon').on('click', function() {
      $(this).text( $(this).text() == '+' ? '-' : '+' );
      $subUl.slideToggle('fast');
    });
  });
});
