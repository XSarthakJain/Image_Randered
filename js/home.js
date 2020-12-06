
function readURL(input) {
    //document.getElementById("shareSubmitButton").type="submit";
    if (input.files && input.files[0]) {
      var reader = new FileReader();
      
      reader.onload = function(e) {
        $('#imagePlacedID').attr('src', e.target.result);
      }
      
      reader.readAsDataURL(input.files[0]); // convert to base64 string
    }
  
    
  }
  
  $("#SelectFileId").change(function() {
    readURL(this);
  });
  