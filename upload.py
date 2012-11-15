from bottle import route, run, template, post, get , request , static_file, os
@route("/")
def welcome():
    return """
	   <form action="/uploadpage" ">
		<input type="submit" value="upload file" />
            </form>
	   <form action="/list" ">
		<input type="submit" value="list uploaded file" />
            </form>
	    """
@route("/uploadpage")
def uploadpage():
    return """
	   <form action="/upload" method="post" enctype="multipart/form-data">
		<input type="text" name="name" />
        	<input type="file" name="data" />
		<input type="submit" value="upload" />
            </form>
	    """

@route('/upload', method='POST')
def do_upload():
	data = request.files.get("data")
	name = data.name
	if name and data.file:
		raw = data.file.read()
		filename = data.filename
		open('/home/jaideep/uploadfiles/%s' % filename, 'wb').write(raw)
		return "Hello! You uploaded "+"<a href='/%s'>%s" % (filename,filename) +"</a> (%d bytes)." % len(raw)
	return "You missed a field"

@route("/list")
def list_myfiles():
    files=os.listdir("/home/jaideep/uploadfiles/")
    my_list= []
    for index, value in enumerate(files):
           my_list.append("%d. <a href='/%s'>%s" % (index+1,value,value) +"</a>"+"<br>")
    print my_list
    return my_list

@route("/<filename>")
def static(filename):
    return static_file(filename, root="/home/jaideep/uploadfiles/")

#@get('/favicon.ico')
#def get_favicon():
#    return static_file('favicon.ico')

run(host="192.168.1.112", port=80, debug=True)
