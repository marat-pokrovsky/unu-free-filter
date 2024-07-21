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

const addBtn = document.getElementById("addBtn");
addBtn.addEventListener("click", () => {
  chrome.tabs.query({ active: true }, function (tabs) {
    var tab = tabs[0];
    if (tab) {
      chrome.scripting.executeScript({
        target: { tabId: tab.id, allFrames: true },
        func: addBtns,
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
const sortTaskBtn = document.getElementById("sortTaskBtn");
sortTaskBtn.addEventListener("click", () => {
  chrome.tabs.query({ active: true }, function (tabs) {
    var tab = tabs[0];
    if (tab) {
      chrome.scripting.executeScript({
        target: { tabId: tab.id, allFrames: true },
        func: sortTask,
        args: [
          document.querySelector("input[name=task_type]:checked")
            .nextElementSibling.textContent,
        ],
      });
    } else {
      alert("There are no active tabs");
    }
  });
});

function loadMore() {
  var steps = 20; // Установите количество шагов
  var delay = 700;
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
  var intervalId = setInterval(clickButton, delay);
}

function sort(isCheckedRadioBtnAsc) {
  let rows = Array.from(
    document.querySelectorAll("#wrapper .search-task__table-row")
  );
  //Фильтруем пустые ряды
  rows = rows.filter((row) => row.querySelector(".task-price"));
  /////////////////////////////////////////////////////////////////////////////////////////
  const uniqueElements = {};

  // Проходимся по каждому элементу и добавляем его в объект, используя id в качестве ключа
  rows.forEach((element) => {
    uniqueElements[element.id] = element;
  });

  // Преобразуем объект обратно в массив
  rows = Object.values(uniqueElements);
  ///////////////////////////////////////////////////////////////////////
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
    return isCheckedRadioBtnAsc ? priceA - priceB : priceB - priceA;
  });

  // Удаляем все ряды из таблицы
  let wrapper = document.querySelector("#wrapper");
  wrapper.innerHTML = "";

  // Добавляем отсортированные ряды обратно в таблицу
  rows.forEach((row) => wrapper.appendChild(row));
}
function sortTask(taskType) {
  let rows = Array.from(
    document.querySelectorAll("#wrapper .search-task__table-row")
  );
  rows = rows.filter((row) => row.querySelector(".task-price"));
  const uniqueElements = {};

  // Проходимся по каждому элементу и добавляем его в объект, используя id в качестве ключа
  rows.forEach((element) => {
    uniqueElements[element.id] = element;
  });

  // Преобразуем объект обратно в массив
  rows = Object.values(uniqueElements);
  filteredRows = rows.filter(
    (row) => row.querySelector(".task-type").textContent == taskType
  );

  unfilteredRows = rows.filter(
    (row) => row.querySelector(".task-type").textContent !== taskType
  );

  // Удаляем все ряды из таблицы
  let wrapper = document.querySelector("#wrapper");
  wrapper.innerHTML = "";

  // Добавляем отсортированные ряды обратно в таблицу
  filteredRows.forEach((row) => wrapper.appendChild(row));
  unfilteredRows.forEach((row) => wrapper.appendChild(row));
}
function addBtns() {
  let rows = Array.from(
    document.querySelectorAll("#wrapper .search-task__table-row")
  );
  rows.forEach((row) => {
    if (row.querySelector(".toggleBtn")) return;
    let btn = document.createElement("button");
    btn.className = "toggleBtn";
    btn.style.cursor = "pointer";
    btn.style.width = "auto";
    btn.style.border = "1px solid red";
    btn.style.backgroundColor = "white";
    btn.style.padding = "5px";
    btn.style.borderRadius = "5px";
    btn.style.marginRight = "50px";
    btn.innerHTML = "toggle";
    btn.addEventListener("click", (btn) => {
      btn.target.closest(".search-task__table-row").classList.toggle("active");
    });
    row.append(btn);
  });
}
