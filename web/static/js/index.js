const scroller = document.querySelector(".scroller");
const scrollerInner = document.querySelector(".scroller__inner");

if (scrollerInner) {
  const scrollerContent = Array.from(scrollerInner.children);

  scrollerContent.forEach((item) => {
    const duplicatedItem = item.cloneNode(true);
    duplicatedItem.setAttribute("aria-hidden", true);
    scrollerInner.append(duplicatedItem);
  });
}

function showToast(category, message, duration = 3000) {
  const toastContainer = document.querySelector("#toastContainer");

  const toastElement = document.createElement("div");
  toastElement.className =
    "p-4 min-w-[232px] flex justify-center items-center shadow rounded-lg";

  switch (category) {
    case "error":
      toastElement.className += " bg-error";
      break;
    case "success":
      toastElement.className += " bg-success";
      break;
    default:
      toastElement.className += " bg-info";
  }

  toastElement.innerHTML = `<span class="font-medium text-white">${message}</span>`;

  toastContainer.appendChild(toastElement);

  setTimeout(() => {
    toastElement.classList.add("hideMe");
    toastElement.addEventListener("animationend", () => {
      toastElement.remove();
    });
  }, duration);
}

function setSelectedValue(selectElement, value) {
  for (var i = 0; i < selectElement.options.length; i++) {
    if (selectElement.options[i].text == value) {
      selectElement.options[i].selected = true;
      return;
    }
  }
}

document.addEventListener("click", (e) => {
  const isDropdownButton = e.target.matches("[data-dropdown-button]");

  let currentDropdown;

  if (isDropdownButton) {
    currentDropdown = e.target.closest("[data-dropdown]");
    currentDropdown.classList.toggle("active");
  }

  document.querySelectorAll("[data-dropdown].active").forEach((element) => {
    if (element == currentDropdown) return;
    element.classList.remove("active");
  });
});

const socket = io();

socket.on("notification", () => {
  showToast("success", "new notification", 15000);
});
