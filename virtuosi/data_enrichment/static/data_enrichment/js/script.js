let change = () => {
  document.getElementById("overback").style.display = "block";
  document.getElementById("space").style.display = "block";
}
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
      const cookies = document.cookie.split(';');
      for (let i = 0; i < cookies.length; i++) {
          const cookie = cookies[i].trim();
          if (cookie.substring(0, name.length + 1) === (name + '=')) {
              cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
              break;
          }
      }
  }
  return cookieValue;
}

let next = () => {
  var a_11 = document.getElementById("rulename").value;
  var a_12 = document.getElementById("ruledesc").value;
  var csrftoken = getCookie('csrftoken');
  $.ajax({
    url: '/save_rule/',
    method: 'POST',
    data: {'a_11': a_11, 'a_12': a_12},
    beforeSend: function (xhr) {
      xhr.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
      xhr.setRequestHeader('X-CSRFToken', csrftoken);
    },
    success: function (response) {
      document.getElementById("input_0").value = response;
    }
  });

  document.getElementById("addrule").style.display = "block";
  document.getElementById("ruleset").style.display = "none";
  document.getElementsByClassName('font-weight-bold')[1].classList.remove('font-weight-bold');
  document.getElementsByClassName('block-title ')[1].classList.add('font-weight-bold');
}
let next_1 = () => {
  var a_0 = document.getElementById("input_0").value;
  var a_1 = document.getElementById("input_1").value;
  var a_2 = document.getElementById("input_2").value;
  var a_3 = document.getElementById("input_3").value;
  var a_4 = document.getElementById("input_4").value;
  var csrftoken = getCookie('csrftoken');
  $.ajax({
    url: '/save_rule_condition/',
    method: 'POST',
    data: {'a_0': a_0, 'a_1': a_1, 'a_2':  a_2, 'a_3': a_3, 'a_4': a_4},
    beforeSend: function (xhr) {
      xhr.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
      xhr.setRequestHeader('X-CSRFToken', csrftoken);
    },
    success: function (response) {
      var res = JSON.parse(response);
      var data = res.data;
      var ul = document.createElement("ul");
      ul.className += "list-group";
      for (var i = 0; i < data.length; i++) {
        console.log(data[i]);
        var li = document.createElement("li");
        li.className += "list-group-item";
        li.appendChild(document.createTextNode(data[i].tag));
        ul.appendChild(li);
      }
      document.getElementById("rule_cond_block").appendChild(ul);
      document.getElementById("addrule").style.display = "block";
      document.getElementById("input_1").value = '';
      document.getElementById("input_2").value = '';
      document.getElementById("input_3").value = '';
      document.getElementById("input_4").value = '';
    }
  });
}
