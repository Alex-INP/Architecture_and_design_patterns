class ReadableObject:
	def __init__(self, data):
		self.data = data

	def read(self, unused_data_length):
		return self.data.encode()

environ_content = [
	{
	"CONTENT_LENGTH": False,
	"wsgi.input": ReadableObject("a=im&b=wsgi&c=data"),
	"PATH_INFO": "/index",
	"REQUEST_METHOD": "GET"
},
{
	"CONTENT_LENGTH": False,
	"wsgi.input": ReadableObject("a=im&b=wsgi&c=data&d=second"),
	"PATH_INFO": "/aboutus",
	"REQUEST_METHOD": "GET"
},
{
	"CONTENT_LENGTH": False,
	"wsgi.input": ReadableObject("a=im&b=wsgi&c=data&d=third"),
	"PATH_INFO": "/contacts",
	"REQUEST_METHOD": "GET"
},
{
	"CONTENT_LENGTH": 2,
	"wsgi.input": ReadableObject("a=im&b=wsgi&c=data&d=fourth"),
	"PATH_INFO": "/contacts",
	"REQUEST_METHOD": "POST"
},
{
	"CONTENT_LENGTH": 2,
	"wsgi.input": ReadableObject("a=im&b=wsgi&c=data&d=fifth"),
	"PATH_INFO": "/aboutus",
	"REQUEST_METHOD": "POST"
}
]

def start_response(*args, **kwargs):
	print(f"***Start_response called with\nargs: {args}\nkwargs: {kwargs}\n")

