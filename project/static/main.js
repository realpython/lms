$(function() {

  // delete course
  $('.delete-course').on('click', function() {
    var result = confirm('Are you sure?');
    if (result) {
      var courseId = $(this).attr('id');
      console.log(courseId);
      $.ajax({
        method: 'DELETE',
        url: '/admin/course/' + courseId
      })
      .done(function(data) {
        console.log(data);
        location.reload();
      })
      .fail(function(err) {
        console.log(err);  // handle errors
      });
    }
    return false;
  });

});

