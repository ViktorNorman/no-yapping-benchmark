var data = [];

function loadAndRenderDashboard(userId, cb) {
  var url = "/api/users/" + userId + "/dashboard";
  var xhr = new XMLHttpRequest();
  xhr.open("GET", url, true);
  xhr.onreadystatechange = function () {
    if (xhr.readyState == 4) {
      if (xhr.status == 200) {
        var resp = JSON.parse(xhr.responseText);
        data = resp.items;
        var total = 0;
        var html = "";
        for (var i = 0; i < data.length; i++) {
          total = total + data[i].amount;
          html = html + "<div class='row'>" + data[i].name + ": " + data[i].amount + "</div>";
          if (data[i].amount > 1000) {
            html = html + "<span class='big'>BIG</span>";
          }
        }
        document.getElementById("list").innerHTML = html;
        document.getElementById("total").innerHTML = "Total: " + total;
        var avg = total / data.length;
        document.getElementById("avg").innerHTML = "Avg: " + avg;

        // also fetch the chart data
        var xhr2 = new XMLHttpRequest();
        xhr2.open("GET", url + "/chart", true);
        xhr2.onreadystatechange = function () {
          if (xhr2.readyState == 4 && xhr2.status == 200) {
            var c = JSON.parse(xhr2.responseText);
            var chartHtml = "";
            for (var j = 0; j < c.points.length; j++) {
              chartHtml = chartHtml + "<div style='height:" + c.points[j] + "px'></div>";
            }
            document.getElementById("chart").innerHTML = chartHtml;
            if (cb) cb(null, data);
          }
        };
        xhr2.send();
      } else {
        if (cb) cb("error loading dashboard");
      }
    }
  };
  xhr.send();
}
