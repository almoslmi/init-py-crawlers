#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os
import shutil
import pdfminer
import re

from bs4 import BeautifulSoup

import nltk
from nltk.tokenize import sent_tokenize, word_tokenize

class CaseContentExtractor:
	def __init__(self, filename, path=''):
		self.case_meta_data = {
			'name': '',
			'docket_number': '',
			'date_of_judgement': ''
		}

		self.filename = filename
		
		if path == '':
			path = os.getcwd() + '/case_pdfs'
		
		self.path = path

	def get_contents_as_html(self, destination=''):
		if destination == '':
			destination = self.filename.split('.')[0] + '_html.html'

		command = 'pdf2txt.py -t html case_pdfs/' + self.filename + ' > ' + 'case_htmls/' + destination
		os.system(command)

	def get_contents_as_xml(self, destination=''):
		if destination == '':
			destination = self.filename.split('.')[0] + '_xml.xml'

		command = 'pdf2txt.py -t xml case_pdfs/' + self.filename + ' > ' + 'case_xmls/' + destination
		os.system(command)

	def get_contents_as_tagged_html(self, destination=''):
		if destination == '':
			destination = self.filename.split('.')[0] + '_tag.html'

		command = 'pdf2txt.py -t tag case_pdfs/' + self.filename + ' > ' + 'case_tagged_htmls/' + destination
		os.system(command)

	def get_contents_as_text(self, destination=''):
		if destination == '':
			destination = self.filename.split('.')[0] + '.txt'

		command = 'pdf2txt.py case_pdfs/' + self.filename + ' > ' + 'case_texts/' + destination
		os.system(command)

	# TODO: Add re substitute for pattern [a-z]-\w with ''
	def clean_text_of_case(self):
		def remove_page_headers():
			print 'PAGE HEADERS'

			number_of_lines = len(filelines)

			for line_number in range(number_of_lines):
				if '' in filelines[line_number]:
					try:				
						for i in range(10):
								temp = line_number + i

								if 'v.' in filelines[temp]:
									filelines.pop(temp)
									break
								elif filelines[temp].strip().startswith('Cite as:'):
									filelines.pop(temp)
									break
								else:
									temp = temp + 1
					except IndexError:
						break

		def strip_all_lines():
			print 'STRIP ALL LINES'
			
			count = 0
			for line in filelines:
				filelines[count] = filelines[count].strip()
				count = count + 1

		def remove_page_separators():
			print 'PAGE SEPARATORS'
			
			count = 0
			for line in filelines:
				if '' in line:
					filelines[count] = '\n'

				count = count + 1

		def remove_blank_lines():
			print 'BLANK LINES'
			
			count = 0
			for line in filelines:
				if line == '':
					filelines.pop(count)

				count = count + 1

		def merge_cleaned_lines():
			return ' '.join(filelines)

		f = open('case_texts/' + self.filename.split('.')[0] + '.txt', 'r')
		filelines = f.readlines()

		remove_page_headers()
		strip_all_lines()		
		remove_page_separators()
		remove_blank_lines()
		cleaned_content = merge_cleaned_lines()

		g = open('cleaned_text_files/' + self.filename.split('.')[0] + '.txt', 'w')
		g.write(cleaned_content)


class CitationsExtractor:
	def __init__(self, filename='', path=''):
		self.filename = filename
		
		if path == '':
			path = os.getcwd() + '/case_pdfs'
		
		self.path = path

	def get_contents_as_formatted_html(self, destination=''):
		if destination == '':
			destination = self.filename.split('.')[0] + '_formatted.html'

		command = 'pdf2txt.py -t xml case_pdfs/' + self.filename + ' | python ama_generate.py | tidy -utf8 > case_formatted/' + destination
		print command

		os.system(command)
		
	def get_cleaned_case_content(self):
		f = open('cleaned_text_files/' + self.filename.split('.')[0] + '.txt', 'r')
		self.content = f.read()

	def get_html_content(self):
		f = open('case_htmls/' + self.filename.split('.')[0] + '_html.html', 'r')
		self.html = f.read()

	def break_content_into_sentence_tokens(self):
		return sent_tokenize(self.content)

	def break_sentence_into_word_tokens(self, sentence):
		return nltk.word_tokenize(sentence)

	def is_case_present_in_sentence(self, sentence):
		if 'v.' in sentence:
			return True

		return False

	def is_capitalised(self, word):
		return word[0].isupper()


class CasesCitedExtractor(CitationsExtractor):
	def get_pos_tag_sentence(self, sentence):
		words = nltk.word_tokenize(sentence)
		pos_tagged_words = nltk.pos_tag(words)

		return pos_tagged_words

	def get_case_names(self):
		casenames = []

		soup = BeautifulSoup(self.html)
		cases = soup.findAll('span')

		for i in range(len(cases)):
			if 'v.' in cases[i].text:
				if cases[i-1].text.isupper():
					continue

				casename = ' '.join([cases[i-1].text.strip() , cases[i].text.strip(), cases[i+1].text.strip()]).strip()
				casenames.append(casename)
		print casenames
		return casenames


class ActsCitedExtractor(CitationsExtractor):
	def get_acts_from_symbols(self, sentence):
		s = re.findall(r'§\w?\d+', sentence)
		print s

		act_numbers = []
		for i in s:
			act_numbers.append(i.split('\xa7')[-1])

		print act_numbers

	def get_act_name_from_sentence(self, sentence):
		acts = []

		words = nltk.word_tokenize(sentence)
		pos_tagged_words = nltk.pos_tag(words)
		act_indices = self.get_index_of_act_in_sentence(pos_tagged_words)

		for act_index in act_indices:
			flag = 0
			act = []
			word_index = act_index

			while flag == 0:
				print pos_tagged_words[word_index]
				if pos_tagged_words[word_index][1] != 'DT':
					act.append(pos_tagged_words[word_index][0])
				else:
					act.append(pos_tagged_words[word_index][0])
					flag = 1

				word_index = word_index - 1

			act.reverse()
			act = ' '.join(act)
			acts.append(act)

		return acts

	def get_index_of_act_in_sentence(self, word_pos_tokens):
		act_indices = []
		count = 0

		for i in word_pos_tokens:
			if i[0] == 'Act':
				act_indices.append(count)

			count = count + 1

		return act_indices


class PartiesExtractor(CitationsExtractor):
	def get_parties_from_casename(self):
		parts = self.name.split('v.')

		try:
			self.parties = {
				'petitioner': parts[0].strip(),
				'defendant': parts[1].strip()
			}
		except:
			self.parties = {}

		return self.parties

	def classify_parties(self):
		petitioner_identifiers = [
			'petitioner',
			'appelent',
			'plaintiff'
		]

		petitioner_index = None

		sentences = self.break_content_into_sentence_tokens()

		for sentence in sentences:
			temp_sent = sentence.lower()

			for identifier in petitioner_identifiers:
				if identifier in temp_sent:
					petitioner_index = temp_sent.index()
					break

		if petitioner_index == None:
			return None

		if 'v.' in sentence:
			if sentence.index('v.') < petitioner_index:
				self.swap_parties()
			return

		party_one_index = sentence.index(self.parties['petitioner'])
		party_two_index = sentence.index(self.parties['defendant'])

		distance_party_one = abs(petitioner_index - party_one_index)
		distance_party_two = abs(petitioner_index - party_two_index)

		if distance_party_one > distance_party_two and distance_party_two < 2:
			self.swap_parties()

	def swap_parties(self):
		temp = self.parties['petitioner']
		self.parties['petitioner'] = self.parties['defendant']
		self.parties['defendant'] = self.parties['petitioner']


class JudgeExtractor(CitationsExtractor):
	def get_judges_involved(self):
		sents = self.break_content_into_sentence_tokens()

		judges_involved = {}
		judges_involved['judges'] = []
		judges_involved['chief_judges'] = []
		judges_involved['joint_judges'] = []
		judges_involved['others'] = []

		for i in sents:
			if 'JUSTICE' in i:
				parts = i.split('JUSTICE')

				for j in parts[1:]:
					t = nltk.word_tokenize(j)

					for k in t:
						if k.isupper():
							judges_involved['others'].append(k)
						elif k.strip() == ',':
							continue
						else:
							break


			if ('J.' in i):
				# print 'Sentence=', i
				parts = i.split('J.')

				for j in parts[:-1]:
					t = nltk.word_tokenize(j)
					t.reverse()

					for k in t:
						if k.isupper():
							judges_involved['judges'].append(k)
						elif k.strip() == ',':
							continue
						else:
							break

			if ('C. J.' in i):
				# print 'Sentence=', i
				parts = i.split('C. J.')

				for j in parts[:-1]:
					t = nltk.word_tokenize(j)
					t.reverse()

					for k in t:
						if k.isupper():
							judges_involved['chief_judges'].append(k)
						elif k.strip() == ',':
							continue
						else:
							break

			if ('JJ.' in i):
				# print 'Sentence=', i
				parts = i.split('JJ.')

				for j in parts[:-1]:
					t = nltk.word_tokenize(j)
					t.reverse()

					for k in t:
						if k.isupper():
							judges_involved['joint_judges'].append(k)
						elif k.strip() == ',':
							continue
						else:
							break

		return judges_involved
		
case = '1185.pdf'

t = CaseContentExtractor(case)
print t.filename
print t.path
print t.get_contents_as_text()
print t.get_contents_as_xml()
print t.get_contents_as_tagged_html()
print t.get_contents_as_html()
print t.clean_text_of_case()

print
print
print 'ACTS'
print
print

u = ActsCitedExtractor(case)
print u.filename
print u.path
u.get_cleaned_case_content()
print u.content
sents = u.break_content_into_sentence_tokens()
u.acts = []
for i in sents:
	if 'Act' in i:
		temp1 = u.get_act_name_from_sentence(i)
		u.acts.append(temp1)

	if '§' in i:
		temp2 = u.get_acts_from_symbols(i)
		u.acts.append(temp2)

print
print
print 'CASES'
print
print

v = CasesCitedExtractor(case)
print v.filename
print v.path
v.get_cleaned_case_content()
# print v.content
sents = v.break_content_into_sentence_tokens()

for i in sents:
	if 'v.' in i:
		print i
		print v.get_pos_tag_sentence(i)

v.get_html_content()
# print v.html
v.get_case_names()

print
print
print 'JUDGES'
print
print

w = JudgeExtractor(case)
print w.filename
print w.path
w.get_cleaned_case_content()
print w.content
print w.get_judges_involved()