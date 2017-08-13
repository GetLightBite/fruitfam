import json

def get_cur_image_urls():
  k = open('../test_svm/test_images.json', 'r')
  o = k.read()
  k.close()
  return json.loads(o)

def component_to_html(comp_name, images):
  html = '<h1>%s</h1>\n' % comp_name
  html += '<br />\n'
  for image in images:
    if image != None:
      html += '<img src="%s" style="width:200px">\n' % image
  html += '<br />\n'
  html += '<br />\n'
  return html


# Put in some fancy jquery
html = """
<!DOCTYPE html>
<html>
<head>
<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.1.1/jquery.min.js"></script>
<script>
  $(document).ready(function() {
    selectedImgsArr = new Array();
     $("img").click(function() {
        if($(this).hasClass("selected-image")) {
            var index = selectedImgsArr.indexOf($(this).attr('src'));
            selectedImgsArr.splice(index, 1);
            $(this).removeClass("selected-image");
            $(this).css("border", "");
        } else {
            console.log($(this).attr('src'));
            selectedImgsArr.push($(this).attr('src'));
            $(this).addClass("selected-image");
            $(this).css("border", "1px solid red");
        }
     });
  });
  
  function download() {
    var array = selectedImgsArr
    var a = document.body.appendChild(
        document.createElement("a")
    );
    a.download = "export.txt";
    a.href = "data:text/plain;base64," + btoa(JSON.stringify(array));
    a.innerHTML = "download example text";
  }
  
  
</script>
</head>
<body>
"""

image_urls = get_cur_image_urls()
i = 0
for comp_name in image_urls:
  i += 1
  images = image_urls[comp_name]
  html += component_to_html(comp_name, images)
  # if i == 3:
  #   break


html += """
</body>
</html>
"""

k = open('images_to_filter.html', 'w')
k.write(html)
k.close()