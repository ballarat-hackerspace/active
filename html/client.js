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
    if (localStorage.gender <> '') { $('#gender').val(localStorage.gender); }
    $('#age').val(localStorage.age);
    $('#starttime').val(localStorage.starttime);
    $('#endtime').val(localStorage.endtime);
    if (localStorage.preferred_activity <> '') { $("#preferred_activity").val(localStorage.preferred_activity); }
}

function save_settings() {
      localStorage.gender = $('#gender').val();
      localStorage.age = $('#age').val();
      localStorage.starttime = $('#starttime').val();
      localStorage.endttime = $('#endtime').val();
      localStorage.preferred_activity = $("#preferred_activity").val()
}
