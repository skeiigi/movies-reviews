document.addEventListener("DOMContentLoaded", function () {
    const toggleButtons = document.querySelectorAll(".toggle-replies");

    toggleButtons.forEach((button) => {
      button.addEventListener("click", function () {
        const commentId = button.getAttribute("data-comment-id");
        const repliesContainer = document.getElementById("replies-" + commentId);
        
        if (repliesContainer.style.display === "none") {
          repliesContainer.style.display = "block";
          button.textContent = "Скрыть ответы";
        } else {
          repliesContainer.style.display = "none";
          button.textContent = "Показать ответы";
        }
      });
    });
  });

document.addEventListener("DOMContentLoaded", function () {
  // Получаем ID якоря из URL, если он есть
  const hash = window.location.hash;
  if (hash && hash.startsWith("#comment-")) {
    const comment = document.querySelector(hash);
    if (comment) {
      // Прокручиваем к нужному комментарию и подсвечиваем
      comment.scrollIntoView({ behavior: "smooth", block: "center" });
      comment.classList.add("highlighted-comment");

      // Убираем подсветку через 3 секунды
      setTimeout(() => {
        comment.classList.remove("highlighted-comment");
      }, 3000);
    }
  }
});