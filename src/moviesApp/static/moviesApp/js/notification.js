document.addEventListener("DOMContentLoaded", function(){
    const bell = document.getElementById("notification-icon");
    const dropdown = document.getElementById("notification-dropdown");
    const list = document.getElementById("notification-list");

    bell.addEventListener("click", function (e) {
        e.preventDefault();
        dropdown.style.display = dropdown.style.display === "none" ? "block" : "none";

        if (dropdown.style.display === "block") {
            fetch("/notifications/", {
                headers: {
                    "X-Requested-With": "XMLHttpRequest"
                }
                })
                .then(response => {
                if (response.status === 403) {
                    return "Требуется авторизация для просмотра уведомлений.";
                }
                return response.text();
                })
                .then(data => {
                document.getElementById("notification-list").innerHTML = data;
                const count = document.getElementById("notification-count");
                if (count) count.style.display = "none";
                })
                .catch(error => {
                document.getElementById("notification-list").innerHTML = "Ошибка при загрузке уведомлений.";
                });

        }
    });

    document.addEventListener("click", function (event) {
    if (!dropdown.contains(event.target) && !bell.contains(event.target)) {
      dropdown.style.display = "none";
    }
    });
});

//ОЧИСТКА УВЕДОМЛЕНИЙ
document.addEventListener('click', function(e) {
  if (e.target.id === 'clear-notifications') {
    fetch('/notifications/clear/', {
      method: 'POST',
      headers: {
        'X-CSRFToken': getCookie('csrftoken'),
      },
    })
    .then(response => response.json())
    .then(data => {
      if (data.success) {
        document.getElementById('notification-list').innerHTML = "<p>Уведомления очищены.</p>";
      }
    });
  }
});

function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}
