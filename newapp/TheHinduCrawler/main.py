
import sys
sys.path.insert(0, 'libs')
import webapp2
import requests
from bs4 import BeautifulSoup
import jinja2
import string
import nltk
import nltk.data
# jinja_environment = jinja2.Environment(autoescape=True,
	# loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__), 'templates')))
class DateHandler(webapp2.RequestHandler):
	def get(self):
		links1="""
		<head>
		<title>Home</title>
		 <link rel="stylesheet" href="http://code.jquery.com/ui/1.10.3/themes/smoothness/jquery-ui.css" />
	
			<!-- Load jQuery JS -->
			<script src="http://code.jquery.com/jquery-1.9.1.js"></script>
			<!-- Load jQuery UI Main JS  -->
			<script src="http://code.jquery.com/ui/1.10.3/jquery-ui.js"></script>
			
			<!-- Load SCRIPT.JS which will create datepicker for input field  -->

			
			<style>
			
		
		.myButton {
			moz-box-shadow: 0px 1px 0px 0px #1c1b18;	webkit-box-shadow: 0px 1px 0px 0px #1c1b18;	box-shadow: 0px 1px 0px 0px #1c1b18;	background:-webkit-gradient(linear, left top, left bottom, color-stop(0.05, #eae0c2), color-stop(1, #ccc2a6));	background:-moz-linear-gradient(top, #eae0c2 5%, #ccc2a6 100%);	background:-webkit-linear-gradient(top, #eae0c2 5%, #ccc2a6 100%);	background:-o-linear-gradient(top, #eae0c2 5%, #ccc2a6 100%);	background:-ms-linear-gradient(top, #eae0c2 5%, #ccc2a6 100%);	background:linear-gradient(to bottom, #eae0c2 5%, #ccc2a6 100%);	filter:progid:DXImageTransform.Microsoft.gradient(startColorstr='#eae0c2', endColorstr='#ccc2a6',GradientType=0);	background-color:#eae0c2;	moz-border-radius:15px;	webkit-border-radius:15px;	border-radius:15px;	border:2px solid #333029;	display:inline-block;	cursor:pointer;	color:#505739;	font-family:arial;	font-size:14px;	font-weight:bold;	padding:12px 16px;text-decoration:none;text-shadow:0px 1px 0px #ffffff;
		}
		.myButton:hover {
			background:-webkit-gradient(linear, left top, left bottom, color-stop(0.05, #ccc2a6), color-stop(1, #eae0c2));
			background:-moz-linear-gradient(top, #ccc2a6 5%, #eae0c2 100%);
			background:-webkit-linear-gradient(top, #ccc2a6 5%, #eae0c2 100%);
			background:-o-linear-gradient(top, #ccc2a6 5%, #eae0c2 100%);
			background:-ms-linear-gradient(top, #ccc2a6 5%, #eae0c2 100%);
			background:linear-gradient(to bottom, #ccc2a6 5%, #eae0c2 100%);
			filter:progid:DXImageTransform.Microsoft.gradient(startColorstr='#ccc2a6', endColorstr='#eae0c2',GradientType=0);
			background-color:#ccc2a6;
		}
		.myButton:active {
			position:relative;
			top:1px;
		}
		</style>
		</head>
		<body bgcolor='	#A3A6A6'>
		<div align='center'><button style="width:500px" class="myButton"><h3>Today's Headlines</h3><h5>articles and summaries</h5></button><br><br>
		<input style="width:300px" onchange="headlines(this)" class="myButton" placeholder="Pick Date(MM/DD/YYY)" type="text" id="datepicker" /></p>
		</div>
				 <script>
				function headlines(item)
				{
					text=$(item).val()
					if(text=="")
						return false
					var dateSelected = new Date(text)
					var today=new Date()
					if(dateSelected.getFullYear()<2012)
					{
							alert("Selected a date after 31st December,2011")
							return false
						}
					ds=(dateSelected.getMonth() + 1) + '/' + dateSelected.getDate() + '/' +  dateSelected.getFullYear()
					td=(today.getMonth() + 1) + '/' + today.getDate() + '/' +  today.getFullYear()
					if(dateSelected>today)
						{
							alert("You cannot select a future date")
							return false
						}
					//	console.log(ds)
					//	console.log(td)
					
					var re = new RegExp("/", 'g');
					text=text.replace(re,"-")
					str=text.split("-");
					text=str[2]+"-"+str[0]+"-"+str[1]
					//console.log(text)
					//return false
					if(ds==td)
					window.location.assign("/category")
					else
					window.location.assign("/pastNews?date="+text)
				}

			$(document).ready(
		  
		  /* This is the function that will get executed after the DOM is fully loaded */
		  function () {
			$( "#datepicker" ).datepicker({
			  changeMonth: true,//this option for allowing user to select month
			  changeYear: true //this option for allowing user to select from year range
			});
		  }

		);
			</script>
		</body>
		"""
		self.response.write(links1)


class MainHandler(webapp2.RequestHandler):
	def get(self):

		# url="http://www.thehindu.com/todays-paper/"
		# source_code=requests.get(url)
		# html=source_code.text
		# soup = BeautifulSoup(html,'html.parser')
		# jinja_environment=jinja2.Environment(autoescape=True, loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__),'templates')))
   		
		links1="""
		<head>
		<title>Categories</title>
		<style>
		.myButton {
			moz-box-shadow: 0px 1px 0px 0px #1c1b18;	webkit-box-shadow: 0px 1px 0px 0px #1c1b18;	box-shadow: 0px 1px 0px 0px #1c1b18;	background:-webkit-gradient(linear, left top, left bottom, color-stop(0.05, #eae0c2), color-stop(1, #ccc2a6));	background:-moz-linear-gradient(top, #eae0c2 5%, #ccc2a6 100%);	background:-webkit-linear-gradient(top, #eae0c2 5%, #ccc2a6 100%);	background:-o-linear-gradient(top, #eae0c2 5%, #ccc2a6 100%);	background:-ms-linear-gradient(top, #eae0c2 5%, #ccc2a6 100%);	background:linear-gradient(to bottom, #eae0c2 5%, #ccc2a6 100%);	filter:progid:DXImageTransform.Microsoft.gradient(startColorstr='#eae0c2', endColorstr='#ccc2a6',GradientType=0);	background-color:#eae0c2;	moz-border-radius:15px;	webkit-border-radius:15px;	border-radius:15px;	border:2px solid #333029;	display:inline-block;	cursor:pointer;	color:#505739;	font-family:arial;	font-size:14px;	font-weight:bold;	padding:12px 16px;text-decoration:none;text-shadow:0px 1px 0px #ffffff;
		}
		.myButton:hover {
			background:-webkit-gradient(linear, left top, left bottom, color-stop(0.05, #ccc2a6), color-stop(1, #eae0c2));
			background:-moz-linear-gradient(top, #ccc2a6 5%, #eae0c2 100%);
			background:-webkit-linear-gradient(top, #ccc2a6 5%, #eae0c2 100%);
			background:-o-linear-gradient(top, #ccc2a6 5%, #eae0c2 100%);
			background:-ms-linear-gradient(top, #ccc2a6 5%, #eae0c2 100%);
			background:linear-gradient(to bottom, #ccc2a6 5%, #eae0c2 100%);
			filter:progid:DXImageTransform.Microsoft.gradient(startColorstr='#ccc2a6', endColorstr='#eae0c2',GradientType=0);
			background-color:#ccc2a6;
		}
		.myButton:active {
			position:relative;
			top:1px;
		}
		</style>
		</head>
		<body bgcolor='	#A3A6A6'>
		<div align='center'><button style="width:500px" class="myButton"><h3>Today's Headlines</h3><h5>articles and summaries</h5></button><br><br>
		<a style="width:300px" class="myButton" href='/headlines?req=home'>Front Page</a> <br><br>
		<a style="width:300px" class="myButton" href='/headlines?req=national'>National</a> <br><br>
		<a style="width:300px" class="myButton" href='/headlines?req=international'>International</a> <br><br>
		<a style="width:300px" class="myButton" href='/headlines?req=opinion'>Opinion</a><br><br>
		<a style="width:300px" class="myButton" href='/headlines?req=business'>Business</a><br><br>
		<a style="width:300px" class="myButton" href='/headlines?req=sports'>Sports</a><br><br>
		</div>
		</body>
		"""
		
		self.response.write(links1)

class PastHandler(webapp2.RequestHandler):
	def get(self):
		date=self.request.get('date')
		
		url="http://www.thehindu.com/todays-paper/tp-index/?date="+date
			
		source_code=requests.get(url)
		html=source_code.text
		soup = BeautifulSoup(html,'html.parser')
		links="""
		<head>
		<title>Headlines for """+date+"""</title>
		<style>
		.myButton {
			moz-box-shadow: 0px 1px 0px 0px #1c1b18;	webkit-box-shadow: 0px 1px 0px 0px #1c1b18;	box-shadow: 0px 1px 0px 0px #1c1b18;	background:-webkit-gradient(linear, left top, left bottom, color-stop(0.05, #eae0c2), color-stop(1, #ccc2a6));	background:-moz-linear-gradient(top, #eae0c2 5%, #ccc2a6 100%);	background:-webkit-linear-gradient(top, #eae0c2 5%, #ccc2a6 100%);	background:-o-linear-gradient(top, #eae0c2 5%, #ccc2a6 100%);	background:-ms-linear-gradient(top, #eae0c2 5%, #ccc2a6 100%);	background:linear-gradient(to bottom, #eae0c2 5%, #ccc2a6 100%);	filter:progid:DXImageTransform.Microsoft.gradient(startColorstr='#eae0c2', endColorstr='#ccc2a6',GradientType=0);	background-color:#eae0c2;	moz-border-radius:15px;	webkit-border-radius:15px;	border-radius:15px;	border:2px solid #333029;	display:inline-block;	cursor:pointer;	color:#505739;	font-family:arial;	font-size:14px;	font-weight:bold;	padding:12px 16px;text-decoration:none;text-shadow:0px 1px 0px #ffffff;
		}
		.myButton:hover {
			background:-webkit-gradient(linear, left top, left bottom, color-stop(0.05, #ccc2a6), color-stop(1, #eae0c2));
			background:-moz-linear-gradient(top, #ccc2a6 5%, #eae0c2 100%);
			background:-webkit-linear-gradient(top, #ccc2a6 5%, #eae0c2 100%);
			background:-o-linear-gradient(top, #ccc2a6 5%, #eae0c2 100%);
			background:-ms-linear-gradient(top, #ccc2a6 5%, #eae0c2 100%);
			background:linear-gradient(to bottom, #ccc2a6 5%, #eae0c2 100%);
			filter:progid:DXImageTransform.Microsoft.gradient(startColorstr='#ccc2a6', endColorstr='#eae0c2',GradientType=0);
			background-color:#ccc2a6;
		}
		.myButton:active {
			position:relative;
			top:1px;
		}
		</style>
		</head>
		<body bgcolor='	#A3A6A6'>
		<div align='center'><a style="width:500px" class="myButton" href='/'><h3>Headlines for """+date+"""</h3><h5>articles and summaries</h5></a><br><br>
		"""
		for link in soup.findAll('div',{'class':'tpaper'}):
			try:
				article_title=link.find('a').text.encode("utf-8")
				article_link=link.find('a').get("href").encode("utf-8")
				btn="""<a style="width:500px" class="myButton" href='/article?date="""+date+"""&a="""+article_link+"""&title="""+article_title+"""' >"""+article_title+"""</a>
				<a style="width:300px" href='"""+article_link+"""' class="myButton" target="_blank">View Full Article from Source</a>
				<a style="width:300px" class="myButton" href='/summary?date="""+date+"""&a="""+article_link+"""&title="""+article_title+"""'>View Summary</a>
				<br><br>
				"""
				links=links+btn
			except Exception,e:
				pass	
		links=links+"</div></body>"
		self.response.write(links)


class Headlines(webapp2.RequestHandler):
	def get(self):
		req=self.request.get('req')
		
		if req=='home':
			url="http://www.thehindu.com/todays-paper/"
		if req=='national':
			url="http://www.thehindu.com/todays-paper/tp-national/"
		if req=='international':
			url="http://www.thehindu.com/todays-paper/tp-international/"
		if req=='opinion':
			url="http://www.thehindu.com/todays-paper/tp-opinion/"
		if req=='business':
			url="http://www.thehindu.com/todays-paper/tp-business/"
		if req=='sports':
			url="http://www.thehindu.com/todays-paper/tp-sports/"
	
		source_code=requests.get(url)
		html=source_code.text
		soup = BeautifulSoup(html,'html.parser')
		links="""
		<head>
		<title>Today's Headlines</title>
		<style>
		.myButton {
			moz-box-shadow: 0px 1px 0px 0px #1c1b18;	webkit-box-shadow: 0px 1px 0px 0px #1c1b18;	box-shadow: 0px 1px 0px 0px #1c1b18;	background:-webkit-gradient(linear, left top, left bottom, color-stop(0.05, #eae0c2), color-stop(1, #ccc2a6));	background:-moz-linear-gradient(top, #eae0c2 5%, #ccc2a6 100%);	background:-webkit-linear-gradient(top, #eae0c2 5%, #ccc2a6 100%);	background:-o-linear-gradient(top, #eae0c2 5%, #ccc2a6 100%);	background:-ms-linear-gradient(top, #eae0c2 5%, #ccc2a6 100%);	background:linear-gradient(to bottom, #eae0c2 5%, #ccc2a6 100%);	filter:progid:DXImageTransform.Microsoft.gradient(startColorstr='#eae0c2', endColorstr='#ccc2a6',GradientType=0);	background-color:#eae0c2;	moz-border-radius:15px;	webkit-border-radius:15px;	border-radius:15px;	border:2px solid #333029;	display:inline-block;	cursor:pointer;	color:#505739;	font-family:arial;	font-size:14px;	font-weight:bold;	padding:12px 16px;text-decoration:none;text-shadow:0px 1px 0px #ffffff;
		}
		.myButton:hover {
			background:-webkit-gradient(linear, left top, left bottom, color-stop(0.05, #ccc2a6), color-stop(1, #eae0c2));
			background:-moz-linear-gradient(top, #ccc2a6 5%, #eae0c2 100%);
			background:-webkit-linear-gradient(top, #ccc2a6 5%, #eae0c2 100%);
			background:-o-linear-gradient(top, #ccc2a6 5%, #eae0c2 100%);
			background:-ms-linear-gradient(top, #ccc2a6 5%, #eae0c2 100%);
			background:linear-gradient(to bottom, #ccc2a6 5%, #eae0c2 100%);
			filter:progid:DXImageTransform.Microsoft.gradient(startColorstr='#ccc2a6', endColorstr='#eae0c2',GradientType=0);
			background-color:#ccc2a6;
		}
		.myButton:active {
			position:relative;
			top:1px;
		}
		</style>
		</head>
		<body bgcolor='	#A3A6A6'>
		<div align='center'><a style="width:500px" class="myButton" href='/'><h3>Today's Headlines</h3><h5>articles and summaries</h5></a><br><br>
		<a style="width:150px" class="myButton" href='/headlines?req=home'>Front Page</a>
		<a style="width:150px" class="myButton" href='/headlines?req=national'>National</a>
		<a style="width:150px" class="myButton" href='/headlines?req=international'>International</a>
		<a style="width:150px" class="myButton" href='/headlines?req=opinion'>Opinion</a>
		<a style="width:150px" class="myButton" href='/headlines?req=business'>Business</a>
		<a style="width:150px" class="myButton" href='/headlines?req=sports'>Sports</a><br><br>
		"""
		for link in soup.findAll('div',{'class':'tpaper'}):
			article_title=link.find('a').text.encode("utf-8")
			article_link=link.find('a').get("href").encode("utf-8")
			btn="""<a style="width:500px" class="myButton" href='/article?date=&a="""+article_link+"""&req="""+req.encode('utf-8')+"""&title="""+article_title+"""' >"""+article_title+"""</a>
			<a style="width:300px" href='"""+article_link+"""' class="myButton" target="_blank">View Full Article from Source</a>
			<a style="width:300px" class="myButton" href='/summary?date=&a="""+article_link+"""&req="""+req.encode('utf-8')+"""&title="""+article_title+"""'>View Summary</a>
			<br><br>
			"""
			links=links+btn
	
		links=links+"</div></body>"
		self.response.write(links)

class Articles_Text(webapp2.RequestHandler):
	def get(self):
		url=self.request.get('a')
		req=(self.request.get('req')).encode('utf-8')
		title=self.request.get('title')
		date=self.request.get('date')
		# url="http://www.thehindu.com/todays-paper/handle-trivandrum/article6495436.ece"
		source_code=requests.get(url)
		html=source_code.text
		soup = BeautifulSoup(html,'html.parser')
		art=soup.find('div',{'class':'article-body'})
		article_text=""
		article_head=soup.find('h1',{'class':'detail-title'}).text.encode("utf-8")
		if art!=None:
			for pp in art.findAll('p',{'class':'body'}):
				article_text=article_text+(pp.text).encode("utf-8")
		else:
			art=soup.find('div',{'class':'article-text'})
			for pp in art.findAll('p',{'class':'body'}):
				article_text=article_text+(pp.text).encode("utf-8")
		# print article_head
		# print article_text

		if article_text.strip()=="":
			article_text="No Body To Display"

		if date=='':
			hrf='/headlines?req='+req
		else:
			hrf='/pastNews?date='+date.encode('utf-8')

		links="""
		<head>
		<title>Article: """+article_head+"""</title>
		<style>
		.myButton {
			moz-box-shadow: 0px 1px 0px 0px #1c1b18;	webkit-box-shadow: 0px 1px 0px 0px #1c1b18;	box-shadow: 0px 1px 0px 0px #1c1b18;	background:-webkit-gradient(linear, left top, left bottom, color-stop(0.05, #eae0c2), color-stop(1, #ccc2a6));	background:-moz-linear-gradient(top, #eae0c2 5%, #ccc2a6 100%);	background:-webkit-linear-gradient(top, #eae0c2 5%, #ccc2a6 100%);	background:-o-linear-gradient(top, #eae0c2 5%, #ccc2a6 100%);	background:-ms-linear-gradient(top, #eae0c2 5%, #ccc2a6 100%);	background:linear-gradient(to bottom, #eae0c2 5%, #ccc2a6 100%);	filter:progid:DXImageTransform.Microsoft.gradient(startColorstr='#eae0c2', endColorstr='#ccc2a6',GradientType=0);	background-color:#eae0c2;	moz-border-radius:15px;	webkit-border-radius:15px;	border-radius:15px;	border:2px solid #333029;	display:inline-block;	cursor:pointer;	color:#505739;	font-family:arial;	font-size:14px;	font-weight:bold;	padding:12px 16px;text-decoration:none;text-shadow:0px 1px 0px #ffffff;
		}
		.myButton:hover {
			background:-webkit-gradient(linear, left top, left bottom, color-stop(0.05, #ccc2a6), color-stop(1, #eae0c2));
			background:-moz-linear-gradient(top, #ccc2a6 5%, #eae0c2 100%);
			background:-webkit-linear-gradient(top, #ccc2a6 5%, #eae0c2 100%);
			background:-o-linear-gradient(top, #ccc2a6 5%, #eae0c2 100%);
			background:-ms-linear-gradient(top, #ccc2a6 5%, #eae0c2 100%);
			background:linear-gradient(to bottom, #ccc2a6 5%, #eae0c2 100%);
			filter:progid:DXImageTransform.Microsoft.gradient(startColorstr='#ccc2a6', endColorstr='#eae0c2',GradientType=0);
			background-color:#ccc2a6;
		}
		.myButton:active {
			position:relative;
			top:1px;
		}
		</style>
		</head>
		<body bgcolor='	#A3A6A6'>
		<div align='center'><button style="width:1000px" class="myButton"><h2>"""+article_head+"""</h2><h4>"""+article_text+"""</h4></button><br><br>
		<a style="width:300px" class="myButton"  href='"""+hrf+"""'>Go Back To Headlines</a>
		</div></body>
		"""
		# links=links+"</div>"
		self.response.write(links)

class Summary(webapp2.RequestHandler):
	def median(self,score):
		array=[]
		for s in score:
			array.append(s)
		for c in range(len(array)):
			for d in range(len(array)-c-1):
				if array[d] > array[d+1]:
					swap       = array[d];
					array[d]   = array[d+1];
					array[d+1] = swap;
		med=array[int(len(array)/2)]
		high=array[len(array)-1]
		return [med,high]
	def get(self):
		prep=["a","about",  "above",   "across",  "afore",  "after",   "along",  "alongside",   "among",  "amongst",  "an",  "anenst",  "apropos",  "apud",  "around",  "as",  "aside",  "astride",  "at",   "atop",   "before",  "behind",  "below",  "beneath",  "beside",  "besides",  "between",  "beyond",  "but",  "by",  "circa",  "concerning",  "despite",  "down",  "during",  "for",   "from",  "given",  "in",  "including",  "inside",  "into",  "lest",  "like", "if", "is",  "mid",  "midst",  "minus",  "modulo",  "near",  "next",  "notwithstanding",  "of",  "off",  "on",  "onto",  "opposite",  "out",  "outside",  "over",  "pace",  "past",  "per",  "plus",  "pro",   "regarding",  "round",  "sans",  "save",  "since",  "than",  "through",  "throughout",  "till",  "times",  "to",   "under", "unlike",  "until",  "unto",  "up",  "upon",  "vice",  "with", "within", "without", "am","is","i","m","are","the","that","this","there","here","their","were","those","ebben","negl","dere","otro","noista","dazu","auf","otra","aus","under","aux","dela","dele","dell","algunos","tinham","olisimme","haben","upp","fuera","esos","zonder","fece","varit","n","ellas","feci","ebbi","nem","avranno","nei","emilyen","ned","tuolta","while","ebbe","kun","estuvo","above","estuve","ekkor","facevi","starei","med","meg","daha","wezen","men","facesse","here","meu","met","nicht","mes","hers","amolyan","sidan","jolta","gli","aki","vosostras","della","esteve","desselben","erais","sarai","estive","heille","niin","einiges","fussions","loro","seraient","einigem","einigen","wollen","until","seja","facemmo","abbiamo","quale","me","olet","fossimo","ma","avremo","mi","minuun","mu","mellett","era","olen","ero","akik","avaient","tuvieses","gegen","eussent","tuoksi","auraient","dykk","want","tuviesen","anderer","anderes","hoe","end","enn","how","dieselben","hos","anderen","anderem","facesti","sanki","after","las","hasta","sentid","einmal","vart","vars","aient","over","hubiese","nostra","vara","nostre","ezzel","nostri","before","begge","hon","then","them","sinulta","deinem","deinen","deines","deiner","they","mucho","pelas","wenn","hubieran","l","each","damit","seriez","diye","mikor","facevamo","aurais","aurait","diesen","dieser","dieses","suyas","werde","icke","elle","inom","noille","noilla","ist","att","staranno","hennar","einer","eines","avrebbe","tuoi","tuon","einen","hogyan","ingen","tot","toi","ton","too","tuossa","hiszen","estavam","minun","verte","fussent","sille","etter","minua","varje","haya","hemos","minut","habidos","este","esta","esto","mine","vagyok","korso","mint","tiveram","fosti","foste","deres","derer","houveremos","ohne","erano","the","somme","fusse","don","majd","m","dog","yours","dov","yani","fussiez","sentidos","och","wirst","dessen","sarebbero","olivat","avrete","do","meget","sobre","di","de","da","geen","du","furent","stiamo","sentida","nichts","estados","sentido","iets","blev","sugl","skulle","tenham","nur","nun","nuo","num","blei","inni","egyes","staremmo","weiter","estiveram","we","legyen","diese","wo","soyons","were","anche","queste","uns","questa","estuviera","ill","questo","questi","against","una","und","une","veel","com","col","uno","foram","durante","niye","fra","been","estaban","estabas","noen","tenemos","joiden","jossa","nagyon","aies","zich","hvilken","stavano","suas","mivel","avessimo","aqueles","auras","ait","avrei","seras","egyik","dello","serai","vagy","aie","delle","aurai","faremmo","unos","is","it","ik","im","il","io","in","if","manchem","manchen","manches","mancher","manche","ella","jetzt","kim","hans","kvarhelst","depois","ihrem","ihren","stettero","ihres","avrebbero","noihin","andere","just","anderm","andern","ikkje","anderr","anders","estiverem","farei","hai","antes","ezen","ham","han","kell","hab","ela","had","estuvieron","ele","hay","har","has","hat","opp","unter","mis","d","stavate","mykje","szemben","ole","kunne","oli","facendo","sinussa","ich","for","valaki","muito","uma","tuviese","foi","annak","unse","dette","estuvieran","hvordan","eravate","estuvieras","tenidas","zur","theirs","o","algo","kellett","einiger","zum","aber","sok","som","erre","son","down","sou","stavamo","soy","jene","avait","kven","keille","avais","minusta","wat","was","war","suyos","ellos","uten","veya","fora","avions","abbiate","tuviste","muss","tengan","nerde","azt","tengas","facevano","efter","abbiano","ni","no","na","tivemos","when","somt","til","jona","nu","tuyas","kva","dies","havemos","kvi","siente","joita","josta","thi","oss","sollte","aurions","selbst","sejam","habidas","quienes","ved","vem","fuiste","ert","ihnen","houveria","hatten","belki","din","did","die","warst","dig","meille","somos","dit","dir","ville","hvem","hver","mely","facessi","joilla","joille","sareste","saresti","serait","negli","semmi","my","geweest","amely","nel","melyek","nereye","pero","abban","teljes","vous","auront","aurons","ook","siate","jag","seremos","can","tuviera","ihre","fossem","mintha","noch","hayamos","noita","nyt","till","tengamos","mas","habremos","tuyos","aos","such","lhes","dove","man","poikki","su","benne","si","so","sa","se","sejamos","hende","hubierais","stia","mais","avessi","facciate","estuviese","joihin","coi","non","noi","noe","nog","aquilo","not","qu","now","nor","nos","avons","olit","hanno","olin","kann","el","en","ei","ej","ennek","ed","eg","ez","eu","et","es","er","stiano","dort","hajam","poco","bli","ble","voltunk","denselben","tienen","farebbero","auch","tienes","starebbe","noiden","zal","noget","yourself","amelyekben","ons","tenhamos","degl","ont","jenem","jenen","ikke","cikkek","jenes","jener","vilka","that","hun","lhe","qual","hur","egyetlen","than","amikor","werd","avevano","and","alles","aller","sull","himself","allen","allem","miksi","any","estamos","zou","lehetett","wird","amit","dykkar","ahogy","joksi","saremo","lenni","solche","lenne","seria","estejam","elas","estoy","estos","estou","ayants","daar","serais","dich","only","ayante","olimme","toch","ehhez","nell","dasselbe","avendo","siihen","leur","where","seas","volna","kvifor","olisivat","sean","facessimo","hvorfor","estad","tuolla","estar","estas","between","nostro","tiverem","ju","tus","mellan","jo","como","tuo","tua","come","ja","koska","estivermos","s","aura","vuestro","hva","avevamo","por","je","ante","maga","siete","oder","tue","hepsi","houverem","those","houverei","myself","eit","these","minulle","fuisteis","minulla","vaikka","ein","eran","eram","soit","teille","sois","par","pas","sentidas","same","hvilke","ya","eri","hvis","staresti","eitt","olleet","quien","fecero","stareste","tenha","defa","hebben","tenho","estivessem","tivessem","machen","noka","soient","deze","being","ne","quella","avesti","aveste","quello","lett","ami","ditt","ama","serei","mot","moi","mon","tanto","serez","vosostros","mod","aurez","eussiez","t","nosotras","avrai","korleis","ezt","eddig","naar","havde","eurer","sommes","jobban","meinen","meinem","meiner","meines","kenen","sarebbe","aveva","seine","kenet","habe","on","om","og","of","ob","neden","ou","os","or","op","houvera","habiendo","esses","tuvisteis","your","het","welches","welcher","hep","her","there","los","starete","eues","euer","hem","welchem","hei","welchen","gibi","mich","with","vere","keine","ad","af","vors","am","al","ao","an","as","saremmo","au","uit","av","az","tenga","vore","again","pedig","you","avessero","olitte","hubiste","etwas","sullo","sulla","sulle","unsen","unsem","eusse","u","unser","unses","estuviste","all","noilta","diesem","noissa","alt","als","tu","to","niiden","derselbe","ti","kvar","te","ta","estando","estaba","very","sono","fai","sont","tuvimos","minden","worden","sinulla","hendes","joista","sinulle","tem","altijd","haar","kunnen","further","tes","teu","what","sua","suo","sul","sui","sus","sur","deles","jede","iemand","farete","hadde","toen","ahhoz","eras","avesse","stava","durch","vid","vil","otros","hogy","fueras","tutto","minussa","tutti","varte","houver","dieselbe","fueran","sondern","more","mellom","door","fusses","hubieras","nerede","der","des","det","dei","minhas","del","dem","den","tuas","deg","wieder","avemmo","mesmo","voltam","voltak","nagyobb","fu","tuvieseis","notre","tuona","numa","a","egy","kein","ise","through","itt","its","zelf","alle","alla","allo","joissa","sinusta","allt","hvor","nossos","musste","yo","ces","ilyenkor","tuvieran","denne","heihin","denna","vannak","stemmo","hubieseis","nossa","ugyanis","todo","nosso","einem","tenida","serions","tenido","suoi","jolle","jolla","estaremos","lehet","mukaan","nokre","estada","voor","nosotros","estejamos","tivesse","mindenki","hubiera","dina","nach","tuvieras","tendremos","jer","kom","kon","esas","avec","avez","contra","jeg","seamos","contro","para","sera","tive","sta","aan","dans","dann","teve","teriam","tiver","faccio","noiksi","estuvieses","euch","faccia","henne","also","estuviesen","todos","nuestras","selv","szinte","tuve","estivesse","tuvo","kan","essa","most","esse","tivera","minha","meine","ki","hubieses","fossi","hubiesen","stessimo","fosse","ezek","tened","olyan","quem","mina","faresti","fareste","valami","joiksi","porque","steste","his","mein","esteja","stesti","stando","during","hij","him","hin","houveriam","vilket","vissza","seu","sto","ses","fuesen","seg","fueses","egyre","bare","are","sea","sen","sem","sei","ingi","inkje","sonst","dein","deim","soll","dalla","jeden","jedem","dalle","dallo","ison","estivemos","jedes","jeder","both","c","quelle","olisi","quelli","samma","samme","olla","auriez","hajamos","fummo","estuvisteis","teus","whom","ollut","dus","amelyeket","johon","estuvierais","fut","fus","mindig","fue","fui","alatt","vom","voi","itself","vor","vos","acaba","fueron","estes","nokon","keiden","zwar","eure","cikkeket","nokor","entre","eles","y","stesse","estadas","stessi","skal","nuestra","nuestro","bliver","olisin","vagyis","olisit","keihin","cui","bin","hennes","bij","aviez","hayan","habida","hayas","biz","bis","habido","facciamo","houveram","jota","valamint","een","sokkal","mycket","ihrer","sue","some","hinter","ilyen","aquele","ourselves","aquela","minulta","terei","per","algunas","pelo","pela","be","nello","nella","nelle","bu","mutta","weil","by","von","bist","fomos","saranno","yli","inte","teniendo","into","keneen","gewesen","kanssa","vaan","neki","heeft","degli","fossero","keneksi","avremmo","suis","deira","dessa","azok","kunde","azon","ut","uw","up","cikk","um","un","tuolle","ud","nogle","noko","elles","eller","wollte","nas","ellen","hanem","cuando","siden","temos","avevo","avevi","eures","dall","starai","derselben","dos","euren","eurem","agl","e","muchos","having","once","sitta","essas","ge","stavi","stavo","sarei","nuestros","stiate","tivermos","niets","maar","persze","yourselves","tra","tuosta","tinha","starebbero","blitt","zo","ze","vele","zu","eurent","biri","einige","indem","lei","les","sind","sine","sina","honom","avreste","tegen","avresti","ovat","wie","wil","amelynek","volt","wir","zijn","meihin","viszont","from","che","chi","fel","few","kuin","estabais","mindent","themselves","zij","slik","estuvieseis","vuestra","farebbe","hatte","this","siksi","nekem","pour","meer","votre","faceste","reeds","ette","zwischen","seriam","tai","sit","siz","sia","sig","waren","cual","delas","itse","sin","facevate","houve","isso","olisitte","azonban","le","la","eue","lo","li","demselben","keiksi","eux","eut","eus","sie","dal","dan","dai","dat","doch","das","stette","stetti","hossen","solches","solcher","vilken","hubisteis","doing","mijn","joilta","olemme","our","solchen","solchem","out","tuya","tuyo","olette","stessero","omdat","deras","fuerais","faceva","eravamo","facevo","formos","ill.","que","qui","fuimos","milyen","sintiendo","tuvierais","ihr","furono","suya","ihn","akkor","illetve","ihm","suyo","estemos","their","abbia","blivit","heb","quando","ebbero","herself","sinuun","bei","ben","houvemos","seinem","seinen","eusses","blir","have","seiner","seines","mij","mio","min","mia","mie","mig","isto","which","seront","mille","mir","mit","serons","teria","eres","who","detta","noina","estivera","mange","sedan","why","medan","houvessem","denn","kenelle","muy","nagy","niet","soyez","moet","hade","should","forem","noin","ayez","joina","sinun","deine","sinua","avete","wordt","sinut","viel","keiner","keines","she","keinem","keinen","aquelas","ahol","tengo","miei","sehr","facciano","fuese","tuvieron","nossas","lui","jos","haja","faremo","avuti","avuto","kez","avuta","avute","ett","joka","szerint","ci","ce","blive","niihin","tiene","farai","ai","tenidos","estava","igen","meus","siamo","ile","ours","vort","ott","estuvimos","facessero","hubo","inn","hube","will","estiver","niiksi","vilkas","at","kuka","nous","ve","vi","nincs","sitt","welche","nada","tuohon","essendo","pelos","estado","sugli","off","am","i","avevate","con","lesz","weg","houvermos","disse","utan","dess","jonka","ayant","houvesse","sokat","emme","hubimos","teremos","because","mihin","otras","werden","jotka","csak","est","dagl","fanno","doen","ese","does","esa","eso","desde","teihin","mitt","fordi","ayons","hoss","niille","about","anden","onder","ander","hier","einig","em","own","stanno","mert","donde","eine","staremo","vai","van","eens","ayantes","vad","quante","eussions","quanta","var","quanto","quanti","azzal","faranno","but","ho","ha","he","dagli","j","below","fueseis","sein","hvad","vuestros","amelyek","ins","vostri","amelyet","vostro","ind","vostra","vostre","arra","deires","siano","other","seus","sich","sarete","agli","hubieron","stai","vuestras"]

		req=(self.request.get('req')).encode('utf-8')

		trans=["only","fact","addition","coupled","mention","important","token","equally","identically","uniquely","moreover","together","likewise","comparatively","correspondingly","similarly","furthermore","additionally","summarize","summation","concluding","conclusion","henceforthe","therefore","resulting","result","knowingly"]
		date=self.request.get('date')
		url=self.request.get('a')
		title=self.request.get('title')
		# url="http://www.thehindu.com/todays-paper/handle-trivandrum/article6495436.ece"
		source_code=requests.get(url)
		html=source_code.text
		soup = BeautifulSoup(html,'html.parser')
		art=soup.find('div',{'class':'article-body'})
		article_text=""
		article_head=soup.find('h1',{'class':'detail-title'}).text.encode("utf-8")
		if art!=None:
			for pp in art.findAll('p',{'class':'body'}):
				article_text=article_text+(pp.text).encode("utf-8")
		else:
			art=soup.find('div',{'class':'article-text'})
			for pp in art.findAll('p',{'class':'body'}):
				article_text=article_text+(pp.text).encode("utf-8")
		# print article_head
		# print article_text

		if article_text.strip()=="":
			article_text="No Body To Display"
			summary_text="No Body To Display"
	
		if article_text!="No Body To Display":
			title=[]
			title_text=article_head.replace("-"," ")
			title_temp=title_text.split()

			for tt in title_temp:
				if string.lower(tt) not in prep:
					title.append(string.lower(tt))

			sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')
			sentences=sent_detector.tokenize(article_text.decode("utf-8"))
			# sentences=article_text.split(".")
			art_size=len(sentences)
			if art_size<3:
				summary_text=article_text

			if art_size>=3 and art_size<=7:
				summary_text=sentences[0]+sentences[int(art_size/2)]+sentences[art_size-1]	
			
			if art_size>7:	
				score=[]
				for i in range(art_size):
					score.append(0)

				if art_size>=12:
					score[0]=score[1]=score[2]=score[3]=score[art_size-2]=score[art_size-3]=score[art_size-4]=50
				else:
					score[0]=score[1]=score[art_size-2]=50
				score[art_size-1]=70
				i=0
				for sent in sentences:
					temp_words=sent.split()
					words=[]
					prop_score=0
					for tt in temp_words:
						if tt[:1] in list(map(chr, range(65, 90))):
							prop_score=prop_score+30
						if tt not in prep:
							words.append(string.lower(tt)) 
					conc_score=0
					tit_score=0
					wd_score=len(words)*5
					for wd in words:
						if wd in trans:
							conc_score=conc_score+70
						if wd in title:
							tit_score=150
					score[i]=score[i]+prop_score+conc_score+tit_score+wd_score
					i=i+1
				array=[]
				for s in score:
					array.append(s)
				for c in range(len(array)):
					for d in range(len(array)-c-1):
						if array[d] > array[d+1]:
							swap       = array[d];
							array[d]   = array[d+1];
							array[d+1] = swap;

				med=array[int(len(array)/2)]
				i=0
				summary=[]
				summary_text=""
				for s in score:
					if s>=med:
						summary.append(sentences[i])
						summary_text=summary_text+sentences[i]
					i=i+1
				array1=[]
				array2=[]
				array3=[]

				if len(score)%3==0:
					div1=div2=div3=len(score)/3
				else:
					div1=div3=int(len(score))/3
					div2=div1+len(score)%3
				d=0
				for s in score:
					if d<div1:
						array1.append(s)
					if div1==div2:
						if d>=div1 and d<2*div1:
							array2.append(s)
						if d>=2*div1:
							array3.append(s)	
					if div1 != div2:
						if d>=div1 and d<(div1+div2):
							array2.append(s)
						if d>=(div1+div2):
							array3.append(s)
					d=d+1
				# print array2
				# exit()
				x=Summary()	
				s1=x.median(array1)
				s2=x.median(array2)
				s3=x.median(array3)
				m1=s1[0]
				m2=s2[0]
				m3=s3[0]
				h1=s1[1]
				h2=s2[1]
				h3=s3[1]
				summary=[]
				summary_text=""
				i=0
				if len(score)>7:
					count=0
					for a in array1:
						if count>1:
							i=i+1
							continue
						if a>=m1:
							summary.append(sentences[i])
							summary_text=summary_text+sentences[i]+" "

							count=count+1
							i=i+1
					count=0
					for a in array2:
						if count>1:
							i=i+1
							continue
						if a>=m2:
							summary.append(sentences[i])
							summary_text=summary_text+sentences[i]+" "

							count=count+1
							i=i+1
					count=0
					for a in array3:
						if count>1:
							i=i+1
							continue
						if a>=m3:
							summary.append(sentences[i])
							summary_text=summary_text+sentences[i]+" "

							count=count+1
							i=i+1
				else:
					c=0
					for a in array1:
						if a>=h1 and c==0:
							summary.append(sentences[i])
							summary_text=summary_text+sentences[i]+" "

							i=i+1
							c=1
						else:
							i=i+1
							pass
					c=0
					for a in array2:
						if a>=h2 and c==0:
							summary.append(sentences[i])
							summary_text=summary_text+sentences[i]+" "
							i=i+1
							c=1
						else:
							i=i+1
							pass
					c=0
					for a in array3:
						if a>=h3 and c==0:
							summary.append(sentences[i])
							summary_text=summary_text+sentences[i]+" "
							i=i+1
							c=1
						else:
							i=i+1
							pass
		if date=='':
			hrf='/headlines?req='+req
		else:
			hrf='/pastNews?date='+date.encode('utf-8')
		links="""
		<head>
		<title>Summary: """+article_head+"""</title>
		<style>
		.myButton {
			moz-box-shadow: 0px 1px 0px 0px #1c1b18;	webkit-box-shadow: 0px 1px 0px 0px #1c1b18;	box-shadow: 0px 1px 0px 0px #1c1b18;	background:-webkit-gradient(linear, left top, left bottom, color-stop(0.05, #eae0c2), color-stop(1, #ccc2a6));	background:-moz-linear-gradient(top, #eae0c2 5%, #ccc2a6 100%);	background:-webkit-linear-gradient(top, #eae0c2 5%, #ccc2a6 100%);	background:-o-linear-gradient(top, #eae0c2 5%, #ccc2a6 100%);	background:-ms-linear-gradient(top, #eae0c2 5%, #ccc2a6 100%);	background:linear-gradient(to bottom, #eae0c2 5%, #ccc2a6 100%);	filter:progid:DXImageTransform.Microsoft.gradient(startColorstr='#eae0c2', endColorstr='#ccc2a6',GradientType=0);	background-color:#eae0c2;	moz-border-radius:15px;	webkit-border-radius:15px;	border-radius:15px;	border:2px solid #333029;	display:inline-block;	cursor:pointer;	color:#505739;	font-family:arial;	font-size:14px;	font-weight:bold;	padding:12px 16px;text-decoration:none;text-shadow:0px 1px 0px #ffffff;
		}
		.myButton:hover {
			background:-webkit-gradient(linear, left top, left bottom, color-stop(0.05, #ccc2a6), color-stop(1, #eae0c2));
			background:-moz-linear-gradient(top, #ccc2a6 5%, #eae0c2 100%);
			background:-webkit-linear-gradient(top, #ccc2a6 5%, #eae0c2 100%);
			background:-o-linear-gradient(top, #ccc2a6 5%, #eae0c2 100%);
			background:-ms-linear-gradient(top, #ccc2a6 5%, #eae0c2 100%);
			background:linear-gradient(to bottom, #ccc2a6 5%, #eae0c2 100%);
			filter:progid:DXImageTransform.Microsoft.gradient(startColorstr='#ccc2a6', endColorstr='#eae0c2',GradientType=0);
			background-color:#ccc2a6;
		}
		.myButton:active {
			position:relative;
			top:1px;
		}
		</style>
		</head>
		<body bgcolor='	#A3A6A6'>
		<div align='center'><button style="width:1000px" class="myButton"><h2>"""+article_head+"""</h2><h4>"""+summary_text+"""</h4></button><br><br>
		<a style="width:300px" class="myButton" href='"""+hrf+"""'>Go Back To Headlines</a>
		</div></body>
		"""
		# links=links+"</div>"
		self.response.write(links)
	
app = webapp2.WSGIApplication([
	('/', DateHandler),
	('/category', MainHandler),
	('/pastNews', PastHandler),
	('/headlines',Headlines),
	('/article',Articles_Text),
	('/summary', Summary)
], debug=True)
