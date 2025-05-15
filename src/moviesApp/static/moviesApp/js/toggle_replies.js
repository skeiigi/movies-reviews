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