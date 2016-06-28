########################################################################
# PDF -> EPUB conversion
# Copyright (C) 2013 Daniel Beer <dlbeer@gmail.com>
#
# Permission to use, copy, modify, and/or distribute this software for
# any purpose with or without fee is hereby granted, provided that the
# above copyright notice and this permission notice appear in all
# copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL
# WARRANTIES WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE
# AUTHOR BE LIABLE FOR ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL
# DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR
# PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER
# TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR
# PERFORMANCE OF THIS SOFTWARE.
########################################################################
# Tuned for "A Mathematician's Apology", by G.H. Hardy, available in
# PDF format from:
#
#    http://www.math.ualberta.ca/mss/
########################################################################

import xml.sax, sys, cgi, math, re

########################################################################
# Take XML input from pdf2txt.py and feed it to a SAX parser which will
# extract pages of unordered glyphs.
########################################################################

def runFilters(filep):
    parser = xml.sax.make_parser()
    parser.setContentHandler(GlyphExtractor())
    parser.parse(filep)

########################################################################
# Parse the output of pdf2txt.py and produce a stream of tuples
# containing glyphs with their positions, fonts and sizes
########################################################################

class GlyphExtractor(xml.sax.ContentHandler):
    def __init__(self):
	self.handler = LineGrouper()

    def startElement(self, name, attrs):
	if name == 'text':
	    self.textattrs = attrs
	elif name == 'page':
	    self.handler.page()

    def characters(self, content):
	if content == '\n':
	    return

	try:
	    fontBits = self.textattrs['font'].split(',')
	    if len(fontBits) < 2:
		fontBits.append(None)

	    bbox = map(float, self.textattrs['bbox'].split(','))
	    fontBits.append(int(round(float(self.textattrs['size']))))

	except:
	    return

	self.handler.glyph(tuple(bbox), tuple(fontBits), content)

    def endDocument(self):
	self.handler.end()

class GlyphExtractorPrinter():
    def page(self):
	print 'page'

    def glyph(self, bbox, font, char):
	print ('  glyph: bbox=%s, font=%s, char=%r' % \
	    ('(%.02f, %.02f, %.02f, %.02f)' % bbox,
	     '(%s, %s, %d)' % font, char)).encode('utf-8')

    def end(self):
	print '<<<EOF>>>'

########################################################################
# Take the output of the glyph extractor and then identify common
# baselines within each page. Emit glyphs grouped by line, then by page.
# Lines are ordered top-to-bottom, but glyphs are unordered within each
# line.
########################################################################

class LineGrouper():
    def __init__(self):
	self.handler = ChunkJoiner()
	self.glyphs = None

    def emit_page(self):
	if self.glyphs is None:
	    return

	lines = {}
	for bi, glyph in self.glyphs:
	    klass = self.get_class(bi)

	    if not lines.has_key(klass):
		lines[klass] = []

	    lines[klass].append(glyph)

	klasses = lines.keys()
	klasses.sort(lambda a, b: cmp(self.baselines[a], self.baselines[b]))
	klasses.reverse()

	self.handler.page()
	for klass in klasses:
	    bl = self.baselines[klass]
	    self.handler.line(bl)
	    for bottom, span, font, char in lines[klass]:
		lift = int(round(bottom - bl))
		self.handler.glyph(span, font + tuple([lift]), char)

	self.glyphs = None

    def page(self):
	self.emit_page()
	self.glyphs = []
	self.eqClass = {}
	self.baselines = {}

    # Obtain the class to which the given index currently belongs.
    # Initially, all indices belong solely to distinct classes.
    def get_class(self, bi):
	if not self.eqClass.has_key(bi):
	    return bi

	cl = self.get_class(self.eqClass[bi])
	self.eqClass[bi] = cl
	return cl

    # Record the given baseline value as being associated with the class
    # idx. We keep track of the smallest baseline seen in each class.
    def notice_baseline(self, idx, value):
	if not self.baselines.has_key(idx) or \
	   self.baselines[idx] > value:
	       self.baselines[idx] = value

    # Join two classes
    def join_classes(self, a, b):
	if a < b:
	    self.eqClass[b] = a
	    self.notice_baseline(a, self.baselines[b])
	elif b > a:
	    self.eqClass[a] = b
	    self.notice_baseline(b, self.baselines[a])

    def glyph(self, bbox, font, char):
	left, bottom, right, top = bbox

	bi = int(math.ceil(bottom))
	ti = int(math.floor(top))

	klass = self.get_class(bi)
	self.notice_baseline(klass, bottom)

	if char != ' ':
	    for i in xrange(bi + 1, (bi + ti + ti) / 3):
		ic = self.get_class(i)
		self.notice_baseline(ic, bottom)
		self.join_classes(klass, ic)

	self.glyphs.append((klass, (bottom, (left, right), font, char)))

    def end(self):
	self.emit_page()
	self.handler.end()

class LineGrouperPrinter():
    def page(self):
	print 'page'

    def line(self, base):
	print '  line: base=%.02f' % base

    def glyph(self, span, font, char):
	print ('    glyph: span=%s, font=%s, char=%r' % \
	    ('(%.02f, %.02f)' % span,
	     '(%s, %s, %d, %d)' % font, char)).encode('utf-8')

    def end(self):
	print '<<<EOF>>>'

########################################################################
# Take the output of line grouping, and within each line, sort and join
# glyphs into substring chunks with common styling. Chunks are ordered
# by left edge.
########################################################################

GLUE_MARGIN = 20.0

class ChunkJoiner:
    def __init__(self):
	self.handler = Depaginator()
	self.glyphs = None

    def emit_line(self):
	if self.glyphs is None:
	    return

	self.glyphs.sort(lambda a, b: cmp(a[0][0], b[0][0]))

	chunkText = ''
	chunkFont = None
	chunkLeft = None
	chunkRight = None

	self.handler.line(self.baseline)

	for (l, r), font, char in self.glyphs:
	    if chunkFont != font or abs(chunkRight - l) > GLUE_MARGIN:
		if chunkText != '':
		    self.handler.chunk((chunkLeft, chunkRight),
			    chunkFont, chunkText)
		chunkText = ''
		chunkFont = font
		chunkLeft = l

	    chunkRight = r
	    chunkText += char

	if chunkText != '':
	    self.handler.chunk((chunkLeft, chunkRight),
		    chunkFont, chunkText)

	self.glyphs = None

    def page(self):
	self.emit_line()
	self.handler.page()

    def line(self, baseline):
	self.emit_line()
	self.baseline = baseline
	self.glyphs = []

    def glyph(self, span, font, char):
	self.glyphs.append((span, font, char))

    def end(self):
	self.emit_line()
	self.handler.end()

class ChunkJoinerPrinter:
    def page(self):
	print 'page'

    def line(self, base):
	print '  line: base=%.02f' % base

    def chunk(self, span, font, text):
	print ('    chunk: span=%s, font=%s, text=%r' % \
	    ('(%.02f, %.02f)' % span,
	     '(%s, %s, %d, %d)' % font, text)).encode('utf-8')

    def end(self):
	print '<<<EOF>>>'

########################################################################
# Take the output of the chunk joiner, and depaginate the document. We
# classify lines based on content and position to identify:
#    - title-page material
#    - page numbers
#    - footnotes
# Page numbers are thrown away, and footnotes are reassembled at the end
# of the document. Pages and baselines disappear, and we emit sections,
# consisting of lines of chunks.
########################################################################

SPECIAL_PAGES = ['title', 'copyright', 'dedication', 'preface']

class Depaginator:
    def __init__(self):
	self.chunks = None
	self.footnotes = []
	self.page_number = -1
	self.handler = Unwrapper()

    def emit_chunks(self):
	if self.chunks is None:
	    return

	chunks = self.chunks
	self.chunks = None

	# Throw away the footer
	if self.baseline < 170.0:
	    return

	# Throw away lines with no content
	haveContent = False
	for x in chunks:
	    if x[2].rstrip() != '':
		haveContent = True
	if not haveContent:
	    return

	if self.isFootnote:
	    self.footnotes.append(chunks)
	else:
	    self.handler.line()
	    for span, font, text in chunks:
		self.handler.chunk(span, font, text)

    def page(self):
	self.emit_chunks()
	self.page_number += 1
	self.isFootnote = False

	if self.page_number < len(SPECIAL_PAGES):
	    self.handler.section(SPECIAL_PAGES[self.page_number])
	elif self.page_number == len(SPECIAL_PAGES):
	    self.handler.section('main')

    def line(self, baseline):
	self.emit_chunks()
	self.chunks = []
	self.baseline = baseline

    def chunk(self, span, font, text):
	if span[0] < 130.0 and font[2] == 9:
	    self.isFootnote = True

	self.chunks.append((span, font, text))

    def emit_footnotes(self):
	self.handler.section('footnotes')
	for line in self.footnotes:
	    self.handler.line()
	    for span, font, text in line:
		self.handler.chunk(span, font, text)

    def end(self):
	self.emit_chunks()
	self.emit_footnotes()
	self.handler.end()

class DepaginatorPrinter:
    def section(self, ident):
	print 'section: ident=%r' % ident

    def line(self):
	print '  line'

    def chunk(self, span, font, text):
	print ('    chunk: span=%s, font=%s, text=%r' % \
	    ('(%.02f, %.02f)' % span,
	     '(%s, %s, %d, %d)' % font, text)).encode('utf-8')

    def end(self):
	print '<<<EOF>>>'

########################################################################
# Take the output of the depaginator, and rejoin lines into paragraphs.
# Dehyphenate and add spacing as necessary
########################################################################

PARA_INDENT = 16.0
PARA_WOBBLE = 2.0
BLOCKQUOTE_EDGE = 160.0
RIGHT_JUSTIFY = 450.0

class Unwrapper:
    def __init__(self):
	self.handler = HTMLGenerator()
	self.paragraph = []
	self.chunks = []

    def dehyphenate(self):
	if len(self.paragraph) <= 0:
	    return

	font, text = self.paragraph.pop()

	if len(text) > 0 and text[len(text) - 1] == '-':
	    self.paragraph.append((font, text[:len(text) - 1]))
	elif text == '\n':
	    self.paragraph.append((font, text))
	else:
	    self.paragraph.append((font, text.rstrip() + ' '))

    def rstrip_paragraph(self):
	font, text = self.paragraph.pop()
	if len(text) > 0:
	    self.paragraph.append((font, text.rstrip()))

    def emit_paragraph(self):
	if len(self.paragraph) <= 0:
	    return

	self.rstrip_paragraph()

	self.handler.paragraph(self.leftEdge)
	for font, text in self.paragraph:
	    self.handler.chunk(font, text)

	self.paragraph = []

    def emit_line(self):
	if len(self.chunks) <= 0:
	    return

	# Look for paragraph breaks
	lineEdge = self.chunks[0][0][0]
	if len(self.paragraph) > 0:
	    if lineEdge > self.lastLineEdge + PARA_WOBBLE or \
	       lineEdge < (self.lastLineEdge - PARA_INDENT):
		self.emit_paragraph()
	    elif abs(lineEdge - self.leftEdge) < 0.1 and \
		 lineEdge > BLOCKQUOTE_EDGE:
		self.rstrip_paragraph()
		self.paragraph.append((self.chunks[0][1], '\n'))
	    elif self.lastRightEdge < RIGHT_JUSTIFY:
		self.emit_paragraph()

	self.lastLineEdge = lineEdge
	if len(self.paragraph) == 0:
	    self.leftEdge = lineEdge

	# Feed in line chunks
	self.dehyphenate()
	for (l, r), font, text in self.chunks:
	    self.paragraph.append((font, text))
	    self.lastRightEdge = r

	self.chunks = []

    def section(self, ident):
	self.emit_line()
	self.emit_paragraph()
	self.handler.section(ident)

    def line(self):
	self.emit_line()

    def chunk(self, span, font, text):
	self.chunks.append((span, font, text))

    def end(self):
	self.emit_line()
	self.emit_paragraph()
	self.handler.end()

class UnwrapperPrinter:
    def section(self, ident):
	print 'section: ident=%r' % ident

    def paragraph(self, edge):
	print '  paragraph: edge=%.02f' % edge

    def chunk(self, font, text):
	print ('    chunk: font=%s, text=%r' % \
	    ('(%s, %s, %d, %d)' % font, text)).encode('utf-8')

    def end(self):
	print '<<<EOF>>>'

########################################################################
# Take unflowed paragraphs and produce an HTML document.
########################################################################

# Chunk attributes
ATTR_SUPERSCRIPT = 0x01
ATTR_ITALIC = 0x02

# Paragraph attributes
ATTR_BLOCKQUOTE = 0x01
ATTR_HEADING = 0x02
ATTR_FOOTNOTE = 0x04

class HTMLGenerator:
    def __init__(self):
	self.handler = OutputWriter()
	self.chunk_text = []
	self.para_chunks = []

    def section(self, ident):
	self.emit_chunk()
	self.emit_paragraph()
	self.current_section = ident
	self.handler.block(ident.replace(' ', '_'))

    def paragraph(self, edge):
	self.emit_chunk()
	self.emit_paragraph()
	self.para_attr = 0

	if edge > 150.0 and self.current_section == 'main':
	    self.para_attr |= ATTR_BLOCKQUOTE

    def emit_chunk(self):
	if len(self.chunk_text) == 0:
	    return

	self.para_chunks.append((self.chunk_attr, ''.join(self.chunk_text)))
	self.chunk_text = []

    def emit_paragraph(self):
	if len(self.para_chunks) == 0:
	    return

	raw_text = ''.join([text for _, text in self.para_chunks])

	if self.para_attr & ATTR_HEADING:
	    self.para_chunks = []
	    name = (self.current_section + ' ' + raw_text).replace(' ', '_')
	    self.handler.block(name)
	    self.handler.data('<a name="%s"></a>' % name)
	    self.handler.data('<h2 class="chapter">')
	    self.handler.data(cgi.escape(raw_text))
	    self.handler.data('</h2>')
	    return

	# Hack to look for math-like paragraphs
	if re.match('^[A-Za-z]?([^A-Za-z]+[A-Za-z])*[^A-Za-z]*$', raw_text):
	    self.para_attr |= ATTR_BLOCKQUOTE

	if self.para_attr & ATTR_BLOCKQUOTE:
	    self.handler.data('<blockquote>')

	self.handler.data('<p>')

	for attr, text in self.para_chunks:
	    if text == '\n':
		self.handler.data('<br />')
	    elif text == '':
		pass
	    else:
		if attr & ATTR_ITALIC != 0:
		    self.handler.data('<em>')
		if attr & ATTR_SUPERSCRIPT != 0:
		    self.handler.data('<sup>')
		if attr & ATTR_FOOTNOTE:
		    if self.current_section == 'footnotes':
			dst = 'fnsrc_'
			src = 'fndef_'
		    else:
			src = 'fnsrc_'
			dst = 'fndef_'
		    self.handler.data('<a name="%s%s"></a>' % (src, text))
		    self.handler.data('<a href="#%s%s">' % (dst, text))

		self.handler.data(cgi.escape(text))
		if attr & ATTR_FOOTNOTE:
		    self.handler.data('</a>')
		if attr & ATTR_SUPERSCRIPT != 0:
		    self.handler.data('</sup>')
		if attr & ATTR_ITALIC != 0:
		    self.handler.data('</em>')

	self.handler.data('</p>')

	if self.para_attr & ATTR_BLOCKQUOTE:
	    self.handler.data('</blockquote>')

	self.para_chunks = []

    def chunk(self, font, text):
	face, style, size, lift = font
	attr = 0

	if text == '\n':
	    self.emit_chunk()
	    self.para_chunks.append((0, '\n'))
	    return

	if style == 'Italic':
	    attr |= ATTR_ITALIC
	if lift >= size / 2:
	    attr |= ATTR_SUPERSCRIPT
	if face == 'TimesNewRoman' and \
	 ((self.current_section == 'footnotes' and size == 9 and lift >= 5) or
	 (self.current_section == 'main' and size == 12 and lift == 8)):
	    attr |= ATTR_FOOTNOTE

	if self.chunk_text != [] and self.chunk_attr != attr:
	    self.emit_chunk()

	if face == 'EDONCD+cmr10' and size == 18:
	    self.para_attr |= ATTR_HEADING

	self.chunk_attr = attr
	self.chunk_text.append(text)

    def end(self):
	self.emit_chunk()
	self.emit_paragraph()
	self.handler.end()

class HTMLGeneratorPrinter:
    def __init__(self):
	self.have_line = False

    def end_line(self):
	if self.have_line:
	    sys.stdout.write('\n')
	    self.have_line = False

    def block(self, name):
	self.end_line()
	sys.stdout.write('<!-- block: %s -->' % name)

    def data(self, text):
	sys.stdout.write(text.encode('utf-8'))
	self.have_line = True

    def end(self):
	self.end_line()
	sys.stdout.write('<!-- EOF -->\n')

########################################################################
# Regex rewriter. This takes text from the HTML generator, organized
# into blocks, and applies various regexes to it to fix minor issues.
########################################################################

OUTPUT_PREAMBLE = """<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"
    "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en">
<head>
  <meta http-equiv="content-type" content="text/html; charset=utf8" />
  <meta name="author" content="G.H. Hardy" />
  <title>A Mathematician's Apology</title>
</head>
<body>
"""

OUTPUT_POSTAMBLE = """</body>
</html>
"""

OUTPUT_GLOBAL = [
    (u'\u00a7([0-9]*)', u'\u00a7<a href="#main_\\1">\\1</a>'),
    ('\(cid:34\)', u'\u22ef'),
    ('10<sup>1010</sup>', '10<sup>10<sup>10</sup></sup>')
]

OUTPUT_LOCAL = {
    'title': [
	('<p>(.*Apology)</p>', '<h1>\\1</h1>'),
	('<p>(G. H. Hardy)</p>', '<strong>\\1</strong>')
    ],
    'copyright': [
	('^', '<hr />'),
	('<br />', ' '),
	('by the</p><p>', 'by the '),
	('Web at</p><p>', 'Web at '),
	('$',
	 '<p>HTML generated by <code>ama_generate.py</code>, '
	 '2 Jan 2013, http://www.dlbeer.co.nz/</p>'),
	('(http://[a-z\./]+)', '<a href="\\1">\\1</a>')
    ],
    'dedication': [('^', '<hr />')],
    'preface_Preface': [('18July1940', '18 July 1940')],
    'footnotes': [('^', '<h2>Footnotes</h2>')],
    'main_7': [
	('(Against the fall of night\?)<br />', '\\1</p><p>')
    ],
    'main_13': [
	('<sup>(ality.*is fraction )</sup>', '\\1'),
	('<sup>in the form.*</sup>.*<sup>2;(.* that the equation )</sup>',
	 'in the form (<em>a</em>/<em>b</em>)<sup>2</sup>;\\1'),
	('is fraction .*, where.*<sup>are </sup>integers',
	 'is a fraction (<em>a</em>/<em>b</em>), where ' +
	     '<em>a</em> and <em>b</em> are integers'),
	('the equation \(B\)', 'the equation</p><p>(B)'),
	('<em>b</em>([a-z])', '<em>b</em> \\1'),
	('(<p>\(B\) <em>a</em><sup>2</sup>=2<em>b</em><sup>2</sup></p>)',
	 '<blockquote>\\1</blockquote>'),
	# Missing square-root glyphs
	('(irrationality. of )2', u'\\1\u221a2'),
	('(2 is irrational)', u'\u221a\\1'),
	('(2 cannot be expressed)', u'\u221a\\1')
    ],
    'main_14': [
	('3,5,11,13,17', u'\u221a3,\u221a5,\u221a11,\u221a13,\u221a17'),
	('<sup>3</sup>', u'<sup>3</sup>\u221a'),
	('(314159265)', '<u>\\1</u>')
    ],
    'main_18': [
	('profoundly15',
	 'profoundly<a name="fnsrc_15"></a>'
	 '<sup><a href="#fndef_15">15</a></sup>')
    ]
}

def do_subs(text, subs):
    for pat, repl in subs:
	text = re.sub(pat, repl, text)
    return text

class OutputWriter:
    def __init__(self):
	self.bits = []
	sys.stdout.write(OUTPUT_PREAMBLE)

    def emit_block(self):
	if len(self.bits) == 0:
	    return

	text = ''.join(self.bits)
	self.bits = []

	text = do_subs(text, OUTPUT_LOCAL.get(self.block_name, []))
	text = do_subs(text, OUTPUT_GLOBAL)
	print text.encode('utf-8')

    def block(self, name):
	self.emit_block()
	self.block_name = name

    def data(self, text):
	self.bits.append(text)

    def end(self):
	self.emit_block()
	sys.stdout.write(OUTPUT_POSTAMBLE)

########################################################################
# Entry point
########################################################################

if __name__ == '__main__':
    runFilters(sys.stdin)
