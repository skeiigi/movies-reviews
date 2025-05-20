document.addEventListener('DOMContentLoaded', () => {
    // Удаление
    document.querySelectorAll('.delete-comment-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            const commentId = btn.dataset.id;
            if (!confirm("Удалить комментарий?")) return;

            fetch(`/movie-comment/${commentId}/delete/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken')
                }
            }).then(response => response.json())
              .then(data => {
                  if (data.success) {
                      document.getElementById(`comment-${commentId}`).remove();
                  }
              });
        });
    });

    // Редактирование
    document.querySelectorAll('.edit-comment-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            const commentId = btn.dataset.id;

            fetch(`/movie-comment/${commentId}/edit/`)
                .then(response => response.json())
                .then(data => {
                    document.getElementById('edit-comment-modal').innerHTML = data.html;
                    document.getElementById('edit-comment-modal').style.display = 'block';

                    document.querySelector('.edit-movie-comment-form').addEventListener('submit', (e) => {
                        e.preventDefault();

                        const formData = new FormData(e.target);
                        fetch(`/movie-comment/${commentId}/edit/`, {
                            method: 'POST',
                            body: formData,
                            headers: {
                                'X-CSRFToken': getCookie('csrftoken')
                            }
                        }).then(res => res.json())
                          .then(data => {
                              if (data.success) {
                                  document.querySelector(`#comment-${commentId} .comment-content`).textContent = data.new_content;
                                  document.getElementById('edit-comment-modal').style.display = 'none';
                              }
                          });
                    });
                });
        });
    });

    function getCookie(name) {
        const value = `; ${document.cookie}`;
        const parts = value.split(`; ${name}=`);
        if (parts.length === 2) return parts.pop().split(';').shift();
    }
});
