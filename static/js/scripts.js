function msg() {
  alert("called from msg() function");
  console.log("inside msg function");
  return;
}

function todaysDate() {
  var today = new Date();
  var dd = String(today.getDate()).padStart(2, "0");
  var mmmm = today.toLocaleString("default", { month: "long" });
  var yyyy = today.getFullYear();

  today = mmmm + " " + dd + ", " + yyyy;
  return today;
}

/*
window.onload = function () {
    var btn = document.getElementById("testing");
    btn.addEventListener("click", function () {
      var ourRequest = new XMLHttpRequest();
      ourRequest.open("GET", "https://learnwebcode.github.io/json-example/animals-1.json");
      ourRequest.onload = function () {
        alert("called from Request function");
        var ourData = JSON.parse(ourRequest.responseText);
        console.log("Is this working?");
        console.log(ourData[0]);
        renderHTML(ourData);
      };
      ourRequest.send();
    });
  };

function renderHTML(data) {
  var animalContainer = document.getElementById("animal");
  var x = "blah blah blah";
  animalContainer.insertAdjacentHTML("beforeend", x);
}

$(function () {
  $("#mybutton").click(function (event) {
    $.getJSON("/get_usa_chart/", {}, function (data) {});
    return false;
  });
});


function chart(){
    var graph_usa_cases = {{graphJSON_usa_cases | safe}};
var layout = {
      title: 'Cases in the United States',
          xaxis: {
title: 'Date',
showgrid: false,
zeroline: false
},
yaxis: {
title: 'Cases',
showline: false
}
};
Plotly.newPlot('usa',graph_usa_cases,layout);
Plotly.newPlot('usa2',graph_usa_cases,layout);


}
*/
