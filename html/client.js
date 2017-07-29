$("#save").click(function() {
  save_settings();
});

//Clear Data
$("#clear").click(function() {
  $.jStorage.flush();
  //clear_all();
  //$('.notice').text('Data cleared');
});


function load_settings() {
  localStorage.gender
    if (localStorage.getItem("gender") === null ) { $('#gender').val(localStorage.gender); }
    if (localStorage.getItem("age") === null ) { $('#age').val(localStorage.age); }
    if (localStorage.getItem("starttime") === null ) { $('#starttime').val(localStorage.starttime); }
    if (localStorage.getItem("endtime") === null ) { $('#endtime').val(localStorage.endtime); }
    if (localStorage.getItem("preferred_activity") === null ) { $("#preferred_activity").val(localStorage.preferred_activity); }
}

function save_settings() {
      localStorage.gender = $('#gender').val();
      localStorage.age = $('#age').val();
      localStorage.starttime = $('#starttime').val();
      localStorage.endttime = $('#endtime').val();
      localStorage.preferred_activity = $("#preferred_activity").val()
}
