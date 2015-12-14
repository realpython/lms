$(function() {

  // delete course
  $('.delete-course').on('click', function() {
    var self = $(this);
    var result = confirm('Are you sure?');
    if (result) {
      var courseId = self.attr('id');
      $.ajax({
        method: 'DELETE',
        url: '/admin/course/' + courseId
      })
      .done(function(data) {
        self.parent().parent().remove();
        location.reload();
      })
      .fail(function(err) {
        console.log(err);  // handle errors
      });
    }
    return false;
  });

  // delete student
  $('.delete-student').on('click', function() {
    var self = $(this);
    var result = confirm('Are you sure?');
    if (result) {
      var studentId = self.attr('id');
      $.ajax({
        method: 'DELETE',
        url: '/admin/student/' + studentId
      })
      .done(function(data) {
        self.parent().parent().remove();
        location.reload();
      })
      .fail(function(err) {
        console.log(err);  // handle errors
      });
    }
    return false;
  });

  // delete teacher
  $('.delete-teacher').on('click', function() {
    var self = $(this);
    var result = confirm('Are you sure?');
    if (result) {
      var teacherId = self.attr('id');
      $.ajax({
        method: 'DELETE',
        url: '/admin/teacher/' + teacherId
      })
      .done(function(data) {
        self.parent().parent().remove();
        location.reload();
      })
      .fail(function(err) {
        console.log(err);  // handle errors
      });
    }
    return false;
  });

});
