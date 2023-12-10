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

function showToast(category, message) {
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
  }, 3000);
}

function setSelectedValue(selectElement, value) {
  for (var i = 0; i < selectElement.options.length; i++) {
    if (selectElement.options[i].text == value) {
      selectElement.options[i].selected = true;
      return;
    }
  }
}

const getRange = (start: number, end: number) => {
  return Array(end - start + 1)
    .fill(0)
    .map((v, i) => i + start);
};

const pagination = (currentPage: number, pageCount: number) => {
  let delta: number;
  if (pageCount <= 7) {
    // delta === 7: [1 2 3 4 5 6 7]
    delta = 7;
  } else {
    // delta === 2: [1 ... 4 5 6 ... 10]
    // delta === 4: [1 2 3 4 5 ... 10]
    delta = currentPage > 4 && currentPage < pageCount - 3 ? 2 : 4;
  }

  const range = {
    start: Math.round(currentPage - delta / 2),
    end: Math.round(currentPage + delta / 2),
  };

  if (range.start - 1 === 1 || range.end + 1 === pageCount) {
    range.start += 1;
    range.end += 1;
  }

  let pages: any =
    currentPage > delta
      ? getRange(
          Math.min(range.start, pageCount - delta),
          Math.min(range.end, pageCount)
        )
      : getRange(1, Math.min(pageCount, delta + 1));

  const withDots = (value, pair) =>
    pages.length + 1 !== pageCount ? pair : [value];

  if (pages[0] !== 1) {
    pages = withDots(1, [1, "..."]).concat(pages);
  }

  if (pages[pages.length - 1] < pageCount) {
    pages = pages.concat(withDots(pageCount, ["...", pageCount]));
  }

  return pages;
};
