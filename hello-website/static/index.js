var btn = document.getElementById("fetch-data");

btn.addEventListener("click", function (event) {
  // 使用fetch来获取数据
  fetch("/fetchData", {
    method: "GET",
  })
    .then((res) => res.json())
    .then((data) => {
      alert(`获取的数据是${data.data}`);
    });
});
