var _flaskProfileBackupOriginalHtml;

$(document).ready(function() {
  $('#_profileContent table.tablesorter')
    .tablesorter()
    .bind('sortStart', function() {
      $(this).find('tbody tr')
        .removeClass('profileContentTrEven')
        .removeClass('profileContentTrOdd');
    })
    .bind('sortEnd', function() {
      $(this).find('tbody tr').each(function(idx, elem) {
        var even = idx % 2 == 0;
        $(elem)
          .toggleClass('profileContentTrEven', even)
          .toggleClass('profileContentTrOdd', !even);
      });
    });

  $('#flaskShowProfileButton').click(function() {
    $('#_profileContentWrapper').toggle();
    return false;
  });
});
