function getTags() {
  var tags = document.querySelector(".tag-container");
  return tags.innerText
    .replaceAll("\nx", ",")
    .replaceAll("\n", "")
    .slice(0, -1);
}

const tagContainer = document.querySelector(".tag-container");
const input = document.querySelector(".tag-container input");

let tags = [];

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
  doSearch();
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

function doSearch() {
  $("#results").empty();
  $.ajax({
    method: "post",
    url: "/search/team/api",
    data: { text: $("#input").val(), tags: getTags() },
    success: function (res) {
      var data = "";
      $.each(res, function (index, value) {
        t = value.tags.split(",");
        let tags_string = "";
        for (let i = 0; i < t.length; i++) {
          tags_string += `<div class="tag"><span>${t[i]}</span></div>\n`;
        }
        data += `<div class="team-cont">
                    <a class="nostyle" href="/team/${value.uuid}">
                    <div class="row">
                        <div class="col-2 img-container">
                            <img
                              src="/static/team-pictures/${value.image}"
                              alt="Team Image">
                        </div>
                        <div class="col-10 ">
                        <span class='team-uuid'>${value.uuid.slice(
                          value.uuid.length - 6,
                          value.uuid.length
                        )}</span>
                            <h3 class="">${value.name}</h3>
                            <span class='about'>${value.about}</span>
                            <div class="tag-container">
                               ${tags_string} 
                            </div>
                        </div>
                    </div>
                    </a>
                    </div>`;
      });
      $("#results").html(data);
    },
  });
}

$(document).ready(function () {
  $("#input").on("input", doSearch);
});

doSearch();
