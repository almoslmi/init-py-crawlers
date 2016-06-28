import string
import requests
from bs4 import BeautifulSoup


def median(score):
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

prep=["a","about",  "above",   "across",  "afore",  "after",   "along",  "alongside",   "among",  "amongst",  "an",  "anenst",  "apropos",  "apud",  "around",  "as",  "aside",  "astride",  "at",   "atop",   "before",  "behind",  "below",  "beneath",  "beside",  "besides",  "between",  "beyond",  "but",  "by",  "circa",  "concerning",  "despite",  "down",  "during",  "for",   "from",  "given",  "in",  "including",  "inside",  "into",  "lest",  "like", "if", "is",  "mid",  "midst",  "minus",  "modulo",  "near",  "next",  "notwithstanding",  "of",  "off",  "on",  "onto",  "opposite",  "out",  "outside",  "over",  "pace",  "past",  "per",  "plus",  "pro",   "regarding",  "round",  "sans",  "save",  "since",  "than",  "through",  "throughout",  "till",  "times",  "to",   "under", "unlike",  "until",  "unto",  "up",  "upon",  "vice",  "with", "within", "without", "am","is","i","m","are","the","that","this","there","here","their","were","those","ebben","negl","dere","otro","noista","dazu","auf","otra","aus","under","aux","dela","dele","dell","algunos","tinham","olisimme","haben","upp","fuera","esos","zonder","fece","varit","n","ellas","feci","ebbi","nem","avranno","nei","emilyen","ned","tuolta","while","ebbe","kun","estuvo","above","estuve","ekkor","facevi","starei","med","meg","daha","wezen","men","facesse","here","meu","met","nicht","mes","hers","amolyan","sidan","jolta","gli","aki","vosostras","della","esteve","desselben","erais","sarai","estive","heille","niin","einiges","fussions","loro","seraient","einigem","einigen","wollen","until","seja","facemmo","abbiamo","quale","me","olet","fossimo","ma","avremo","mi","minuun","mu","mellett","era","olen","ero","akik","avaient","tuvieses","gegen","eussent","tuoksi","auraient","dykk","want","tuviesen","anderer","anderes","hoe","end","enn","how","dieselben","hos","anderen","anderem","facesti","sanki","after","las","hasta","sentid","einmal","vart","vars","aient","over","hubiese","nostra","vara","nostre","ezzel","nostri","before","begge","hon","then","them","sinulta","deinem","deinen","deines","deiner","they","mucho","pelas","wenn","hubieran","l","each","damit","seriez","diye","mikor","facevamo","aurais","aurait","diesen","dieser","dieses","suyas","werde","icke","elle","inom","noille","noilla","ist","att","staranno","hennar","einer","eines","avrebbe","tuoi","tuon","einen","hogyan","ingen","tot","toi","ton","too","tuossa","hiszen","estavam","minun","verte","fussent","sille","etter","minua","varje","haya","hemos","minut","habidos","este","esta","esto","mine","vagyok","korso","mint","tiveram","fosti","foste","deres","derer","houveremos","ohne","erano","the","somme","fusse","don","majd","m","dog","yours","dov","yani","fussiez","sentidos","och","wirst","dessen","sarebbero","olivat","avrete","do","meget","sobre","di","de","da","geen","du","furent","stiamo","sentida","nichts","estados","sentido","iets","blev","sugl","skulle","tenham","nur","nun","nuo","num","blei","inni","egyes","staremmo","weiter","estiveram","we","legyen","diese","wo","soyons","were","anche","queste","uns","questa","estuviera","ill","questo","questi","against","una","und","une","veel","com","col","uno","foram","durante","niye","fra","been","estaban","estabas","noen","tenemos","joiden","jossa","nagyon","aies","zich","hvilken","stavano","suas","mivel","avessimo","aqueles","auras","ait","avrei","seras","egyik","dello","serai","vagy","aie","delle","aurai","faremmo","unos","is","it","ik","im","il","io","in","if","manchem","manchen","manches","mancher","manche","ella","jetzt","kim","hans","kvarhelst","depois","ihrem","ihren","stettero","ihres","avrebbero","noihin","andere","just","anderm","andern","ikkje","anderr","anders","estiverem","farei","hai","antes","ezen","ham","han","kell","hab","ela","had","estuvieron","ele","hay","har","has","hat","opp","unter","mis","d","stavate","mykje","szemben","ole","kunne","oli","facendo","sinussa","ich","for","valaki","muito","uma","tuviese","foi","annak","unse","dette","estuvieran","hvordan","eravate","estuvieras","tenidas","zur","theirs","o","algo","kellett","einiger","zum","aber","sok","som","erre","son","down","sou","stavamo","soy","jene","avait","kven","keille","avais","minusta","wat","was","war","suyos","ellos","uten","veya","fora","avions","abbiate","tuviste","muss","tengan","nerde","azt","tengas","facevano","efter","abbiano","ni","no","na","tivemos","when","somt","til","jona","nu","tuyas","kva","dies","havemos","kvi","siente","joita","josta","thi","oss","sollte","aurions","selbst","sejam","habidas","quienes","ved","vem","fuiste","ert","ihnen","houveria","hatten","belki","din","did","die","warst","dig","meille","somos","dit","dir","ville","hvem","hver","mely","facessi","joilla","joille","sareste","saresti","serait","negli","semmi","my","geweest","amely","nel","melyek","nereye","pero","abban","teljes","vous","auront","aurons","ook","siate","jag","seremos","can","tuviera","ihre","fossem","mintha","noch","hayamos","noita","nyt","till","tengamos","mas","habremos","tuyos","aos","such","lhes","dove","man","poikki","su","benne","si","so","sa","se","sejamos","hende","hubierais","stia","mais","avessi","facciate","estuviese","joihin","coi","non","noi","noe","nog","aquilo","not","qu","now","nor","nos","avons","olit","hanno","olin","kann","el","en","ei","ej","ennek","ed","eg","ez","eu","et","es","er","stiano","dort","hajam","poco","bli","ble","voltunk","denselben","tienen","farebbero","auch","tienes","starebbe","noiden","zal","noget","yourself","amelyekben","ons","tenhamos","degl","ont","jenem","jenen","ikke","cikkek","jenes","jener","vilka","that","hun","lhe","qual","hur","egyetlen","than","amikor","werd","avevano","and","alles","aller","sull","himself","allen","allem","miksi","any","estamos","zou","lehetett","wird","amit","dykkar","ahogy","joksi","saremo","lenni","solche","lenne","seria","estejam","elas","estoy","estos","estou","ayants","daar","serais","dich","only","ayante","olimme","toch","ehhez","nell","dasselbe","avendo","siihen","leur","where","seas","volna","kvifor","olisivat","sean","facessimo","hvorfor","estad","tuolla","estar","estas","between","nostro","tiverem","ju","tus","mellan","jo","como","tuo","tua","come","ja","koska","estivermos","s","aura","vuestro","hva","avevamo","por","je","ante","maga","siete","oder","tue","hepsi","houverem","those","houverei","myself","eit","these","minulle","fuisteis","minulla","vaikka","ein","eran","eram","soit","teille","sois","par","pas","sentidas","same","hvilke","ya","eri","hvis","staresti","eitt","olleet","quien","fecero","stareste","tenha","defa","hebben","tenho","estivessem","tivessem","machen","noka","soient","deze","being","ne","quella","avesti","aveste","quello","lett","ami","ditt","ama","serei","mot","moi","mon","tanto","serez","vosostros","mod","aurez","eussiez","t","nosotras","avrai","korleis","ezt","eddig","naar","havde","eurer","sommes","jobban","meinen","meinem","meiner","meines","kenen","sarebbe","aveva","seine","kenet","habe","on","om","og","of","ob","neden","ou","os","or","op","houvera","habiendo","esses","tuvisteis","your","het","welches","welcher","hep","her","there","los","starete","eues","euer","hem","welchem","hei","welchen","gibi","mich","with","vere","keine","ad","af","vors","am","al","ao","an","as","saremmo","au","uit","av","az","tenga","vore","again","pedig","you","avessero","olitte","hubiste","etwas","sullo","sulla","sulle","unsen","unsem","eusse","u","unser","unses","estuviste","all","noilta","diesem","noissa","alt","als","tu","to","niiden","derselbe","ti","kvar","te","ta","estando","estaba","very","sono","fai","sont","tuvimos","minden","worden","sinulla","hendes","joista","sinulle","tem","altijd","haar","kunnen","further","tes","teu","what","sua","suo","sul","sui","sus","sur","deles","jede","iemand","farete","hadde","toen","ahhoz","eras","avesse","stava","durch","vid","vil","otros","hogy","fueras","tutto","minussa","tutti","varte","houver","dieselbe","fueran","sondern","more","mellom","door","fusses","hubieras","nerede","der","des","det","dei","minhas","del","dem","den","tuas","deg","wieder","avemmo","mesmo","voltam","voltak","nagyobb","fu","tuvieseis","notre","tuona","numa","a","egy","kein","ise","through","itt","its","zelf","alle","alla","allo","joissa","sinusta","allt","hvor","nossos","musste","yo","ces","ilyenkor","tuvieran","denne","heihin","denna","vannak","stemmo","hubieseis","nossa","ugyanis","todo","nosso","einem","tenida","serions","tenido","suoi","jolle","jolla","estaremos","lehet","mukaan","nokre","estada","voor","nosotros","estejamos","tivesse","mindenki","hubiera","dina","nach","tuvieras","tendremos","jer","kom","kon","esas","avec","avez","contra","jeg","seamos","contro","para","sera","tive","sta","aan","dans","dann","teve","teriam","tiver","faccio","noiksi","estuvieses","euch","faccia","henne","also","estuviesen","todos","nuestras","selv","szinte","tuve","estivesse","tuvo","kan","essa","most","esse","tivera","minha","meine","ki","hubieses","fossi","hubiesen","stessimo","fosse","ezek","tened","olyan","quem","mina","faresti","fareste","valami","joiksi","porque","steste","his","mein","esteja","stesti","stando","during","hij","him","hin","houveriam","vilket","vissza","seu","sto","ses","fuesen","seg","fueses","egyre","bare","are","sea","sen","sem","sei","ingi","inkje","sonst","dein","deim","soll","dalla","jeden","jedem","dalle","dallo","ison","estivemos","jedes","jeder","both","c","quelle","olisi","quelli","samma","samme","olla","auriez","hajamos","fummo","estuvisteis","teus","whom","ollut","dus","amelyeket","johon","estuvierais","fut","fus","mindig","fue","fui","alatt","vom","voi","itself","vor","vos","acaba","fueron","estes","nokon","keiden","zwar","eure","cikkeket","nokor","entre","eles","y","stesse","estadas","stessi","skal","nuestra","nuestro","bliver","olisin","vagyis","olisit","keihin","cui","bin","hennes","bij","aviez","hayan","habida","hayas","biz","bis","habido","facciamo","houveram","jota","valamint","een","sokkal","mycket","ihrer","sue","some","hinter","ilyen","aquele","ourselves","aquela","minulta","terei","per","algunas","pelo","pela","be","nello","nella","nelle","bu","mutta","weil","by","von","bist","fomos","saranno","yli","inte","teniendo","into","keneen","gewesen","kanssa","vaan","neki","heeft","degli","fossero","keneksi","avremmo","suis","deira","dessa","azok","kunde","azon","ut","uw","up","cikk","um","un","tuolle","ud","nogle","noko","elles","eller","wollte","nas","ellen","hanem","cuando","siden","temos","avevo","avevi","eures","dall","starai","derselben","dos","euren","eurem","agl","e","muchos","having","once","sitta","essas","ge","stavi","stavo","sarei","nuestros","stiate","tivermos","niets","maar","persze","yourselves","tra","tuosta","tinha","starebbero","blitt","zo","ze","vele","zu","eurent","biri","einige","indem","lei","les","sind","sine","sina","honom","avreste","tegen","avresti","ovat","wie","wil","amelynek","volt","wir","zijn","meihin","viszont","from","che","chi","fel","few","kuin","estabais","mindent","themselves","zij","slik","estuvieseis","vuestra","farebbe","hatte","this","siksi","nekem","pour","meer","votre","faceste","reeds","ette","zwischen","seriam","tai","sit","siz","sia","sig","waren","cual","delas","itse","sin","facevate","houve","isso","olisitte","azonban","le","la","eue","lo","li","demselben","keiksi","eux","eut","eus","sie","dal","dan","dai","dat","doch","das","stette","stetti","hossen","solches","solcher","vilken","hubisteis","doing","mijn","joilta","olemme","our","solchen","solchem","out","tuya","tuyo","olette","stessero","omdat","deras","fuerais","faceva","eravamo","facevo","formos","ill.","que","qui","fuimos","milyen","sintiendo","tuvierais","ihr","furono","suya","ihn","akkor","illetve","ihm","suyo","estemos","their","abbia","blivit","heb","quando","ebbero","herself","sinuun","bei","ben","houvemos","seinem","seinen","eusses","blir","have","seiner","seines","mij","mio","min","mia","mie","mig","isto","which","seront","mille","mir","mit","serons","teria","eres","who","detta","noina","estivera","mange","sedan","why","medan","houvessem","denn","kenelle","muy","nagy","niet","soyez","moet","hade","should","forem","noin","ayez","joina","sinun","deine","sinua","avete","wordt","sinut","viel","keiner","keines","she","keinem","keinen","aquelas","ahol","tengo","miei","sehr","facciano","fuese","tuvieron","nossas","lui","jos","haja","faremo","avuti","avuto","kez","avuta","avute","ett","joka","szerint","ci","ce","blive","niihin","tiene","farai","ai","tenidos","estava","igen","meus","siamo","ile","ours","vort","ott","estuvimos","facessero","hubo","inn","hube","will","estiver","niiksi","vilkas","at","kuka","nous","ve","vi","nincs","sitt","welche","nada","tuohon","essendo","pelos","estado","sugli","off","am","i","avevate","con","lesz","weg","houvermos","disse","utan","dess","jonka","ayant","houvesse","sokat","emme","hubimos","teremos","because","mihin","otras","werden","jotka","csak","est","dagl","fanno","doen","ese","does","esa","eso","desde","teihin","mitt","fordi","ayons","hoss","niille","about","anden","onder","ander","hier","einig","em","own","stanno","mert","donde","eine","staremo","vai","van","eens","ayantes","vad","quante","eussions","quanta","var","quanto","quanti","azzal","faranno","but","ho","ha","he","dagli","j","below","fueseis","sein","hvad","vuestros","amelyek","ins","vostri","amelyet","vostro","ind","vostra","vostre","arra","deires","siano","other","seus","sich","sarete","agli","hubieron","stai","vuestras"]

print len(prep)
exit()
# for pr in prep:
# 	if pr not in sw:
# 		print pr

# exit()


trans=["only","fact","addition","coupled","mention","important","token","equally","identically","uniquely","moreover","together","likewise","comparatively","correspondingly","similarly","furthermore","additionally","summarize","summation","concluding","conclusion","henceforthe","therefore","resulting","result","knowingly"]

source_code=requests.get("http://www.thehindu.com/todays-paper/tp-opinion/the-freedom-to-marry/article6498397.ece")
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

if article_text.strip()=="":
	article_text="No Body To Display"
	
if article_text!="No Body To Display":
	title=[]
	title_text=article_head.replace("-"," ")
	title_temp=title_text.split()

	for tt in title_temp:
		if string.lower(tt) not in prep:
			title.append(string.lower(tt))
	print title
	exit()
	sentences=article_text.split(".")

	art_size=len(sentences)
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
			if tt[:1] in list(map(chr, range(65, 90))) or tt[:1] in list(map(chr, range(49, 57))):
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
	s1=median(array1)
	s2=median(array2)
	s3=median(array3)
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
				summary_text=summary_text+sentences[i]
				count=count+1
				i=i+1
		count=0
		for a in array2:
			if count>1:
				i=i+1
				continue
			if a>=m2:
				summary.append(sentences[i])
				summary_text=summary_text+sentences[i]
				count=count+1
				i=i+1
		count=0
		for a in array3:
			if count>1:
				i=i+1
				continue
			if a>=m3:
				summary.append(sentences[i])
				summary_text=summary_text+sentences[i]
				count=count+1
				i=i+1
	else:
		c=0
		for a in array1:
			if a>=h1 and c==0:
				summary.append(sentences[i])
				summary_text=summary_text+sentences[i]
				i=i+1
				c=1
			else:
				i=i+1
				pass
		c=0
		for a in array2:
			if a>=h2 and c==0:
				summary.append(sentences[i])
				summary_text=summary_text+sentences[i]
				i=i+1
				c=1
			else:
				i=i+1
				pass
		c=0
		for a in array3:
			if a>=h3 and c==0:
				summary.append(sentences[i])
				summary_text=summary_text+sentences[i]
				i=i+1
				c=1
			else:
				i=i+1
				pass
	# print len(summary)







		
