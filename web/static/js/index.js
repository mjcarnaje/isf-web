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

const socket = io();

socket.on("notification", () => {
  showToast("success", "new notification", 15000);
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
