const comment_status_update_form = document.querySelector("form[name=update_complite_homeworks_status]");

function updateCommentEvrntList() {
  const homework_comments = document.querySelectorAll("section.homework__comment");

  for (var i = 0; i < homework_comments.length; i++) {
    const save_comment_btn = homework_comments[i].querySelector('#save_complite_homework_comment');
    const delete_comment_btn = homework_comments[i].querySelector('#delete_complite_homework_comment');

    const comment_update_form = homework_comments[i].querySelector("form[name=updata_complite_homework_comment]");
    const comment_delete_form = homework_comments[i].querySelector("form[name=delete_complite_homework_comment]");

    save_comment_btn.addEventListener('click', function() {
      comment_update_form.submit();
    });

    delete_comment_btn.addEventListener('click', function() {
      comment_delete_form.submit()
    });

    comment_update_form.addEventListener('submit', function () {
      ajaxSendForm(this)
    });
    comment_delete_form.addEventListener('submit', function () {
      ajaxSendForm(this)
    });
  };
};
updateCommentEvrntList();


function change_status(form, checkbox) {
  const is_change_status = confirm("Are you sure you want to update status")
  if (is_change_status) {
    form.submit()
  }
  else
  {
    checkbox.checked = !checkbox.checked
  }
}
