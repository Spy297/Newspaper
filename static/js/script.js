function showDropdown() {
  var dropdownMenu = document.querySelector(".dropdown-menu");
  dropdownMenu.classList.add("show");
}

function hideDropdown() {
  var dropdownMenu = document.querySelector(".dropdown-menu");
  dropdownMenu.classList.remove("show");
}

url = window.location.href;
var parts = url.split("/");
console.log(parts[3].length);
if (parts[3].length === 0) {
  var word = "general";
} else {
  var word = parts[3];
}
console.log(word);
document
  .querySelector(`#${word}-recent-btn`)
  .addEventListener("click", function (event) {
    var recentBtnId = event.target.id;
    var category_filter = recentBtnId.split("-")[0];
    loadPosts("recent", category_filter);
    console.log(recentBtnId);
  });

document
  .querySelector(`#${word}-popular-btn`)
  .addEventListener("click", function (event) {
    var popularBtnId = event.target.id;
    var category_filter = popularBtnId.split("-")[0];
    loadPosts("popular", category_filter);
    console.log(popularBtnId);
  });

function loadPosts(topic, category_filter) {
  var xhr = new XMLHttpRequest();
  xhr.open(
    "GET",
    `/sidebar_posts?topic=${topic}&category=${category_filter}`,
    true
  );
  xhr.onload = function () {
    if (xhr.status >= 200 && xhr.status < 400) {
      var JsonResponse = JSON.parse(xhr.responseText);
      var response = JsonResponse.response;
      let index = 0;
      // đi qua mỗi hàng trong sidebar_post
      var sidebar_rows = document.querySelectorAll(".sidebar-row");
      // thiết lập ảnh, tiêu đề và nội dung cho hàng hiện tại
      sidebar_rows.forEach(function (row) {
        row.querySelector(".sidebar-post-image").src =
          response[index]["sidebar-post-image"];
        var sidebar_post_title = row.querySelector(".sidebar-post-title");
        sidebar_post_title.textContent = response[index]["sidebar-post-title"];
        var category = response[index]["sidebar-post-category"];
        var id = response[index]["sidebar-post-id"];
        sidebar_post_title.href = `http://127.0.0.1:8000/${category}/${id}/?category=${category}&post_id=${id}`;
        index++;
      });
    } else {
      console.error("Request failed with status", xhr.status);
    }
  };

  xhr.onerror = function () {
    console.error("Request failed");
  };

  xhr.send();
}

document.addEventListener("DOMContentLoaded", async function () {
  function delay(ms) {
    return new Promise((resolve) => setTimeout(resolve, ms));
  }

  console.log("Before delay");
  await delay(2000); // Delay for 2000 milliseconds (2 seconds)
  console.log("After delay");

  loadPosts("recent", word);
});

function displayForm() {
  var commentForm = document.querySelector("#comment-form");
  console.log(commentForm);
  commentForm.style.display = "block";
}
