document$.subscribe(function () {
  var topic = document.querySelector(".md-header__topic");
  if (topic && !topic.querySelector("a")) {
    var link = document.createElement("a");
    link.href = ".";
    link.style.color = "inherit";
    link.style.textDecoration = "none";
    while (topic.firstChild) link.appendChild(topic.firstChild);
    topic.appendChild(link);
  }
});
