var canvas = null;
var ctx = null;
var default_scale = 1;

var JSON_PRETTY = function (string) {

  var pretty = {
    "parse": function (member) {
      return this[(member == undefined) ? 'null' : member.constructor.name.toLowerCase()](member);
    },

    "null": function (value) {
      return this['value']('null', 'null');
    },
    "array": function (value) {
      var results = '';
      for (var x = 0; x < value.length; x++) {
        results += '<li>' + this['parse'](value[x]) + '</li>';
      }
      return '[ ' + ((results.length > 0) ? '<ul class="array">' + results + '</ul>' : '') + ' ]';
    },
    "object": function (value) {
      var results = '';
      for (member in value) {
        results += '<li>' + this['value']('object', member) + ': ' + this['parse'](value[member]) + '</li>';
      }
      return '{ ' + ((results.length > 0) ? '<ul class="object">' + results + '</ul>' : '') + ' }';
    },
    "number": function (value) {
      return this['value']('number', value);
    },
    "string": function (value) {
      return this['value']('string', value);
    },
    "boolean": function (value) {
      return this['value']('boolean', value);
    },

    "value": function (type, value) {
      if (/^(http|https):\/\/[^\s]+$/.test(value)) {
        return this['value'](type, '<a href="' + value + '" target="_blank">' + value + '</a>');
      }
      return '<span class="' + type + '">' + value + '</span>';
    }
  };

  var parse = {
    "error": function (error) {
      return '<h1>Unable to parse JSON.</h1><p><h2>Error Message:</h2><textarea>' + error + '</textarea><br /><br /><h2>Response:</h2><textarea>' + string + '</textarea></p>';
    }
  }

  try {
    var output = pretty.parse(eval('(' + string + ')'));
  }
  catch (error) {
    var output = parse.error(error);
  }

  return output;
};

$(function () {
  //http://jsfiddle.net/influenztial/qy7h5/
  //https://developer.mozilla.org/en-US/docs/Web/API/Canvas_API/Tutorial/Using_images
  //https://www.w3schools.com/tags/canvas_rect.asp
  //https://www.w3schools.com/tags/canvas_drawimage.asp
  var imageLoader = $('#imageLoader')[0];
  canvas = document.getElementById('imageCanvas');
  ctx = canvas.getContext('2d');
  imageLoader.addEventListener('change', handleImage, false);
});

function handleImage(e) {
  var reader = new FileReader();
  clear_all();
  sendImage();
  reader.onload = function (event) {
    var img = new Image();
    img.onload = function () {
      // se a a altura for maior do que 345px
      canvas.width = img.width;
      canvas.height = img.height;

      if (img.height > 345) {
        default_scale = 1.5;
      } else {
        default_scale = 1;
      }

      ctx.drawImage(img, 0, 0);
    }
    img.src = event.target.result;
  }
  reader.readAsDataURL(e.target.files[0]);
}


function clear_all() {
  $("#resultado").html("");
  ctx.clearRect(0, 0, canvas.width, canvas.height);
}

function sendImage() {
  var formData = new FormData();
  var img = document.getElementById('imageLoader').files[0];
  formData.append('file', img);
  $.ajax({
    url: "/api/recognition", // url where to submit the request
    type: "POST", // type of action POST || GET
    dataType: 'json', // data type
    data: formData, // post data || get data,
    processData: false,
    contentType: false,
    success: function (result) {
      var array = result;
      var json = JSON.stringify(result);
      console.log('Typeof: ' + typeof (array));
      $("#resultado").html(JSON_PRETTY(json));
      drawFaceLocation(array);
      var dataURL = canvas.toDataURL();
      document.getElementById('canvasImg').src = dataURL;
    },
    error: function (xhr, resp, text) {
      console.log(xhr, resp, text);
    }
  });
}

function drawFaceLocation(array) {
  for (n in array) {
    var persons = array[n];
    var name = persons[0];
    var face_location = persons[1];
    top_ = face_location[0];
    right_ = face_location[1];
    bottom_ = face_location[2];
    left_ = face_location[3];
    width = (left_ - right_);
    height = (top_ - bottom_);
    console.log('top: ' + top_);
    console.log('right: ' + right_);
    console.log('bottom: ' + bottom_);
    console.log('left: ' + left_);
    console.log('name: ' + name);
    ctx.beginPath();
    ctx.lineWidth = "3";
    ctx.rect(right_, bottom_, width, height);
    ctx.closePath();
    ctx.stroke();
    ctx.beginPath();
    size = 18 * default_scale;
    ctx.font = size + 'px Arial';
    ctx.fillStyle = 'red';
    ctx.textAlign = 'center';
    ctx.fillText(name, left_ + (ctx.measureText(name).width / 2), (bottom_ + size));
    ctx.closePath();
    ctx.stroke();

  }

}