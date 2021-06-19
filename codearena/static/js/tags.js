const tagContainer = document.querySelector(".tag-container");
const input = document.querySelector(".tag-container input");

let element = document.querySelector("#initial-tags");
let tags = [];

if (element) {
  tags = element.innerText.trim().slice(0, -1).split(",");
}

var btn = document.querySelector("#update-btn");

function createTag(label) {
  const div = document.createElement("div");
  div.setAttribute("class", "tag");
  const span = document.createElement("span");
  span.innerHTML = label;
  const closeIcon = document.createElement("i");
  closeIcon.innerHTML = " x";
  closeIcon.style.marginLeft = "5px";
  closeIcon.setAttribute("class", "material-icons");
  closeIcon.setAttribute("data-item", label);
  div.appendChild(span);
  div.appendChild(closeIcon);
  return div;
}

function clearTags() {
  document.querySelectorAll(".tag").forEach((tag) => {
    tag.parentElement.removeChild(tag);
  });
}

function addTags() {
  clearTags();
  tags
    .slice()
    .reverse()
    .forEach((tag) => {
      tagContainer.prepend(createTag(tag));
    });
}

function onButtonClick() {
  var form = document.querySelector("form");
  var tags = document.querySelector(".tag-container");
  var input = document.querySelector(".tag-container input");

  input.value = tags.innerText
    .replaceAll("\nx", ",")
    .replaceAll("\n", "")
    .slice(0, -1);
  form.submit();
}

input.addEventListener("keyup", (e) => {
  if (e.key === " ") {
    e.target.value.split(",").forEach((tag) => {
      tags.push(tag);
    });

    addTags();
    input.value = "";
  }
});
document.addEventListener("click", (e) => {
  console.log(e.target.tagName);
  if (e.target.tagName === "I") {
    const tagLabel = e.target.getAttribute("data-item");
    const index = tags.indexOf(tagLabel);
    tags = [...tags.slice(0, index), ...tags.slice(index + 1)];
    addTags();
  }
});

btn.onclick = onButtonClick;
addTags();
