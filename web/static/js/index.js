async function markAllAsRead() {
  try {
    await fetch(`/notifications/mark-all-as-read`, {
      method: "PUT",
      headers: {
        "X-CSRFToken": document.querySelector("meta[name='csrf_token']")
          .content,
      },
    });
  } catch (error) {
    console.error("Fetch error:", error);
  }
}

async function markAsRead(id) {
  try {
    const response = await fetch(`/notifications/mark-as-read/${id}`, {
      method: "PUT",
      headers: {
        "X-CSRFToken": document.querySelector("meta[name='csrf_token']")
          .content,
      },
    });
    return response;
  } catch (error) {
    console.error("Fetch error:", error);
  }
}

async function markAsArchived(id) {
  try {
    const response = await fetch(`/notifications/mark-as-archived/${id}`, {
      method: "PUT",
      headers: {
        "X-CSRFToken": document.querySelector("meta[name='csrf_token']")
          .content,
      },
    });
    return response;
  } catch (error) {
    console.error("Fetch error:", error);
  }
}

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

function truncateString(str, maxLength) {
  if (str.length > maxLength) {
    return str.substring(0, maxLength) + "...";
  } else {
    return str;
  }
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

function showNotificationToast(notification, duration = 20000) {
  const notificationToastContainer = document.querySelector(
    "#notificationToastContainer"
  );

  const toastElement = createToastElement(notification);
  notificationToastContainer.appendChild(toastElement);

  setTimeout(() => {
    hideAndRemoveToast(toastElement);
  }, duration);
}

function createToastElement(notification) {
  const toastElement = document.createElement("button");

  toastElement.addEventListener("click", async () => {
    markAsRead(notification.id);
    window.location.href = notification.redirect_url;
  });

  const iconClass = getIconClass(notification.type);
  const isReadClass = notification.is_read ? "text-gray-600" : "font-medium";
  const dateClass = notification.is_read ? "text-gray-400" : "text-primary-500";

  toastElement.innerHTML = `
    <div class="flex bg-white border shadow-md cursor-pointer p-4 max-w-md w-full rounded-lg items-start gap-4">
      <div class="relative h-14 aspect-square">
        <img class="object-cover w-full h-full border rounded-full bg-gray-50"
          src="${notification.notifier_photo_url}"
          alt="user's avatar"
          height="auto"
          width="auto" />
        <div class="absolute flex items-center justify-center w-6 h-6 rounded-full shadow -bottom-1 -right-1 ${iconClass}">
          <i class="text-white text-sm ${getIcon(notification.type)}"></i>
        </div>
      </div>
      <div class="flex flex-col gap-1">
        <p class="whitespace-normal text-left ${isReadClass}">
        ${truncateString(notification.message, 80)}
        </p>
        <p id="notification-date" class="text-sm text-left ${dateClass}">
          ${notification.created_at}
        </p>
      </div>
    </div>
  `;

  return toastElement;
}

function getIconClass(type) {
  const iconClasses = {
    ADOPTION_REQUEST: "bg-primary-500",
    ADOPTION_STATUS_UPDATE: "bg-primary-500",
    ADD_DONATION_MONEY: "bg-green-500",
    ADD_DONATION_IN_KIND: "bg-violet-500",
    EVENT_INVITED: "bg-red-500",
  };

  return iconClasses[type] || "";
}

function getIcon(type) {
  const iconClasses = {
    ADOPTION_REQUEST: "fa-solid fa-file-invoice",
    ADOPTION_STATUS_UPDATE: "fa-solid fa-calendar-days",
    ADD_DONATION_MONEY: "fa-solid fa-money-bill",
    ADD_DONATION_IN_KIND: "fa-solid fa-hand-holding-heart",
    EVENT_INVITED: "fa-solid fa-calendar-day",
  };

  return iconClasses[type] || "";
}

function hideAndRemoveToast(toastElement) {
  toastElement.classList.add("hideMe");
  toastElement.addEventListener("animationend", () => {
    toastElement.remove();
  });
}

const fakeLinks = document.querySelectorAll('[role="link"]');

for (let i = 0; i < fakeLinks.length; i++) {
  fakeLinks[i].addEventListener("click", navigateLink);
  fakeLinks[i].addEventListener("keydown", navigateLink);
}

//handles clicks and keydowns on the link
function navigateLink(e) {
  if (e.type === "click" || e.key === "Enter") {
    const ref = e.target ?? e.srcElement;
    if (ref) {
      window.location.href = ref.getAttribute("data-href");
    }
  }
}

function setSelectedValue(selectElement, value) {
  for (var i = 0; i < selectElement.options.length; i++) {
    if (selectElement.options[i].value == value) {
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

const images = document.querySelectorAll("img[data-can-view='true']");
const imageViewer = document.getElementById("image-viewer");

images.forEach(function (image, index) {
  function setActiveImage(src) {
    const fullImage = document.getElementById("image-preview");
    fullImage.setAttribute("src", src);
  }

  function showPreview() {
    imageViewer.classList.remove("hidden");
    imageViewer.classList.add("flex");
    imageViewer
      .querySelector("button[data-type='close']")
      .addEventListener("click", () => hidePreview());
  }

  function hidePreview() {
    imageViewer.classList.add("hidden");
    imageViewer.classList.remove("flex");
  }

  image.addEventListener("click", function () {
    showPreview();
    setActiveImage(this.getAttribute("src"));

    const smallImages = document.querySelector("#small-images");
    let currentIndex = 0;

    const imageFamily = this.closest("div[data-image-group='true']").children;

    smallImages.innerHTML = "";

    function navigate(direction) {
      currentIndex =
        (currentIndex + direction + imageFamily.length) % imageFamily.length;

      setActiveImage(imageFamily[currentIndex].getAttribute("src"));
      Array.from(smallImages.children).forEach((smallImage, index) => {
        smallImage.setAttribute("data-active", currentIndex == index);
      });
    }

    function onClickSmallImage(currentIndex) {
      setActiveImage(imageFamily[currentIndex].getAttribute("src"));
      Array.from(smallImages.children).forEach((smallImage, index) => {
        smallImage.setAttribute("data-active", currentIndex == index);
      });
    }

    Array.from(imageFamily).forEach((img, i) => {
      const smallImage = document.createElement("img");
      smallImage.classList.add(
        ...[
          "object-cover",
          "w-20",
          "h-20",
          "rounded-lg",
          "aspect-square",
          "cursor-pointer",
        ]
      );

      const isActive = img.getAttribute("src") === this.getAttribute("src");

      if (isActive) {
        currentIndex = i;
      }

      smallImage.setAttribute("id", "small-image");
      smallImage.setAttribute("src", img.getAttribute("src"));
      smallImage.setAttribute("data-index", i);
      smallImage.setAttribute("data-active", isActive);
      smallImage.addEventListener("click", () => {
        currentIndex = i;
        onClickSmallImage(i);
      });
      smallImages.append(smallImage);
    });

    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape") {
        hidePreview();
      }

      if (e.key === "ArrowLeft") {
        navigate(-1);
      }
      if (e.key === "ArrowRight") {
        navigate(1);
      }
    });

    imageViewer
      .querySelector("button[data-type='left']")
      .addEventListener("click", () => navigate(-1));

    imageViewer
      .querySelector("button[data-type='right']")
      .addEventListener("click", () => navigate(1));
  });
});

document.querySelectorAll("button[type='submit']").forEach((button) => {
  button.addEventListener("click", function () {
    this.disabled = true;
    this.innerHTML = '<i class="fa fa-spinner fa-spin"></i> Loading';
    this.closest("form").submit();
  });
});

function getCSRFHeader() {
  return {
    "X-CSRFToken": document.querySelector("meta[name='csrf_token']").content,
  };
}

function formatFileSize(size) {
  const units = ["B", "KB", "MB", "GB", "TB"];

  let unitIndex = 0;
  while (size >= 1024 && unitIndex < units.length - 1) {
    size /= 1024;
    unitIndex++;
  }

  return `${size.toFixed(2)} ${units[unitIndex]}`;
}
