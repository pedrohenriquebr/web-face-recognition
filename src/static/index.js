var canvas = null;
var ctx = null;
var default_scale = 1;
var json_result = null;
var array_obj = null;
var img_tag = null;
var big_picture = false;
size = 19;
var msg = null;
var img_width = 0;
var img_height = 0;
var n_persons = 0;
var img_url = null;
var searchButton = null;

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
  img_tag = document.getElementById('canvasImg');;
  msg = $('#mensagem');
  img_url = $("#imageURL")[0];
  searchButton = $("#searchButton")[0];

  n_persons = 0;
  ctx = canvas.getContext('2d');
  imageLoader.addEventListener('change', handleImage, false);
  searchButton.addEventListener('click', handleImageURL, false);
});

function handleImage(e) {
  var reader = new FileReader();
  clear_all();
  reader.onload = function (event) {
    var img = new Image();
    img.onload = function () {
      // se a a altura for maior do que 345px
      canvas.width = img.width;
      canvas.height = img.height;
      img_width = img.width;
      img_height = img.height;

      if (img.height > 345) {
        console.log('foto grande');
        big_picture = true;
      } else {
        big_picture = false;
        console.log('foto dentro das margens');
      }

      ctx.drawImage(img, 0, 0);
    }
    img.src = event.target.result;
  }
  msg.html('aguarde um momento por favor...');
  reader.readAsDataURL(e.target.files[0]);
  sendImage(e.target.files[0]);

}

async function downloadImage(url) {
  return await fetch(url, {
    headers: {
      'accept': 'image/jpeg'
    },
    method: 'GET'
  }
  ).then(d => d.blob()).then(d => d);
}

function handleImageURL(e) {
  var reader = new FileReader();
  clear_all();
  reader.onload = function (event) {
    var img = new Image();
    img.onload = function () {
      // se a a altura for maior do que 345px
      canvas.width = img.width;
      canvas.height = img.height;
      img_width = img.width;
      img_height = img.height;

      if (img.height > 345) {
        console.log('foto grande');
        big_picture = true;
      } else {
        big_picture = false;
        console.log('foto dentro das margens');
      }

      ctx.drawImage(img, 0, 0);
    }
    img.src = event.target.result;
  }
  msg.html('aguarde um momento por favor...');

  downloadImage(img_url.value).then(blob_file => {
    reader.readAsDataURL(blob_file);
    sendImage(new File([blob_file],'img.jpeg'));
  });
}



function clear_all() {
  $("#resultado").html(""); ""
  msg.html("");
  n_persons = 0;
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  update_img_tag();
  array_obj = null;
  json_result = null;
}

function update_img_tag() {
  var dataURL = canvas.toDataURL();
  img_tag.src = dataURL;
}

function sendImage(img) {
  var formData = new FormData();
  formData.append('file', img);


  fetch('/api/recognition/svm', {
    method: 'post',
    body: formData
  })
    .then(d => d.json())
    .then(function (result) {
      array_obj = result;
      json_result = JSON.stringify(result);
      console.log('Typeof: ' + typeof (array_obj));
      $("#resultado").html(JSON_PRETTY(json_result));
      drawFaceLocation(array_obj);
      update_img_tag();
      n_persons = array_obj.length;
      msg.html('tem ' + n_persons + (n_persons > 1 ? ' pessoas' : ' pessoa'));
    });

}

function drawFaceLocation(array) {

  size = 19;
  if (big_picture) {
    size = 19 * (img_height / 345);
  }
  console.log('size: ' + size);
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
    ctx.font = size + 'px Arial';
    ctx.fillStyle = 'red';
    ctx.textAlign = 'center';
    ctx.fillText(name, left_ + (ctx.measureText(name).width / 2), (bottom_ + size));
    ctx.closePath();
    ctx.stroke();

  }

}