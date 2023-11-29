const scroller = document.querySelector(".scroller");
const scrollerInner = document.querySelector(".scroller__inner");
const scrollerContent = Array.from(scrollerInner.children);

scrollerContent.forEach((item) => {
  const duplicatedItem = item.cloneNode(true);
  duplicatedItem.setAttribute("aria-hidden", true);
  scrollerInner.append(duplicatedItem);
});
