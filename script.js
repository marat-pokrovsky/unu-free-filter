//https://habr.com/ru/articles/703330/
let isCheckedRadioBtnAsc = document.getElementById("radio_asc");

const sortBtn = document.getElementById("sortBtn");
sortBtn.addEventListener("click", () => {
  chrome.tabs.query({ active: true }, function (tabs) {
    var tab = tabs[0];
    if (tab) {
      chrome.scripting.executeScript({
        target: { tabId: tab.id, allFrames: true },
        func: sort,
        args: [isCheckedRadioBtnAsc.checked],
      });
    } else {
      alert("There are no active tabs");
    }
  });
});
const loadMoreBtn = document.getElementById("loadMoreBtn");
loadMoreBtn.addEventListener("click", () => {
  chrome.tabs.query({ active: true }, function (tabs) {
    var tab = tabs[0];
    if (tab) {
      chrome.scripting.executeScript({
        target: { tabId: tab.id, allFrames: true },
        func: loadMore,
      });
    } else {
      alert("There are no active tabs");
    }
  });
});

var dropdowns = document.getElementsByClassName("dropdown-btn");
for (var i = 0; i < dropdowns.length; i++) {
  dropdowns[i].addEventListener("click", function () {
    var container = this.nextElementSibling;
    if (container.style.display === "block") {
      container.style.display = "none";
    } else {
      container.style.display = "block";
    }
  });
}

function loadMore() {
  (function () {
    var steps = 20; // Установите количество шагов
    var currentStep = 0;

    function clickButton() {
      if (currentStep < steps) {
        var button = document.getElementById("show_more_button");
        if (button) {
          button.click();
          currentStep++;
          console.log("Button clicked. Step: " + currentStep);
        } else {
          console.log('Button with ID "show_more_button" not found.');
          clearInterval(intervalId);
        }
      } else {
        console.log("Completed " + steps + " steps.");
        clearInterval(intervalId);
      }
    }

    var intervalId = setInterval(clickButton, 500);
  })();
}

function sort(isCheckedRadioBtnAsc) {
  let rows = Array.from(
    document.querySelectorAll("#wrapper .search-task__table-row")
  );
  rows = rows.filter((row) => row.querySelector(".task-price"));

  // Сортируем ряды по содержимому task-price
  rows.sort((a, b) => {
    // Получаем цены из .task-price
    let priceA = parseFloat(
      a.querySelector(".task-price").innerText.replace(/[^\d.-]/g, "")
    );
    let priceB = parseFloat(
      b.querySelector(".task-price").innerText.replace(/[^\d.-]/g, "")
    );

    // Сравниваем цены
    return priceB <= priceA && isCheckedRadioBtnAsc ? 1 : -1;
  });

  // Удаляем все ряды из таблицы
  let wrapper = document.querySelector("#wrapper");
  wrapper.innerHTML = "";

  // Добавляем отсортированные ряды обратно в таблицу
  rows.forEach((row) => wrapper.appendChild(row));
}
