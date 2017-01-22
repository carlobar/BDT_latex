import os
import sys
import re


def not_command(text):
	""" Returns true if the line does not match the pattern of a command
	
	Keyword arguments:
	text -- String with the words that might be commands
	"""
	m_node = p_node.search(text)
	if m_node != None:
		return False
	else:
		return True


def remove_command(c_match):
	m_word = p_color_word.search(c_match.group())
	if m_word != None:
		word = m_word.group()
		word = word.replace('{', '')
		word = word.replace('}', '')
		return word
		

def color_code(word, match, color):
	"""Returns the LaTeX command used to color a word
	
	Keyword arguments:
	word -- Word that must be colored
	match -- Pattern that will be replaced with a LaTeX command
	color -- Color to be used 
	"""
	
	code = r'\BDT' + color + '{'+word+'}'
	match = match.replace(word, code)
	return match


def find_words(list_w, color, text):
	"""Takes a line of text and returns it coloring words in list_w

	Keyword arguments:
	list_w -- List of words that must be colored
	color -- Color used to highlight words
	text -- String with the words that must be colored
	"""
	text = ' ' + text + ' '
	for word in list_w:
		p_w = re.compile('\s+' + word + '[\s\W]', re.IGNORECASE)
		m_w = p_w.finditer(text)
		for match_str in m_w:
			match = match_str.group()
			# we have to find the matchd word, to allow upper case
			p_word = re.compile(word, re.IGNORECASE)
			m_word = p_word.search(match)
			new_word = color_code(m_word.group(), match, color)
			text = text.replace(match, new_word)
	n = len(text)
	text = text[1:n-1]
	return text


def find_end_words(list_wildcards, color, text):
	"""Takes a line of text and returns it coloring words the match a wildcard

	Keyword arguments:
	list_wildcards -- List of wildcards that must be colored
	color -- Color used to highlight words
	text -- String with the words that must be colored
	"""
	text = ' ' + text + ' '
	for wild_c in list_wildcards:
		p_w = re.compile('\s+\w+' + wild_c + '[\W\s]', re.IGNORECASE)
		m_w = p_w.finditer(text)
		for match_str in m_w:
			match = match_str.group()
			# we have to find the match word, to allow upper case
			p_word = re.compile('\w+' + wild_c, re.IGNORECASE)
			m_word = p_word.search(match)
			new_word = color_code(m_word.group(), match, color)
			text = text.replace(match, new_word)
	n = len(text)
	text = text[1:n-1]
	return text


def open_file(name, mod):
	"""Function that opens a file in mode 'mod'

	Keyword arguments:
	name -- Name of the file
	mod -- Modes 'r': read; 'w': write
	"""
	file_name = os.path.normpath(name)
	try:
		file_obj = open(file_name, mod)
	except:
		print('Error opening the file '+file_name)
		exit()
	return file_obj


def find_path(file_route):
	"""Function that finds the path of a file called from LaTeX

	Keyword arguments:
	file_route -- Route to the file
	"""
	m_path = p6.match(file_route)
	if m_path != None:
		path = m_path.group()
	else:
		path = ''
	#print(file_route)
	#print('the path is: '+path)
	return path



def check_recursion(line, global_path, p):
	"""Check if the line imports a file and performs the diagnostic test if necessary 

	Keyword arguments:
	line -- LaTeX line
	global_path -- Path of the file that contains this line
	p -- Pattern of the insertion command
	"""
	m = p.findall(line)
	if len(m) > 0:
		for file_x in m:
			# find the name of the file
			m_file = p8.search(file_x)
			file_name = m_file.group()
			file_name = file_name.replace('{', '')
			file_name = file_name.replace('}', '')
			file_name = file_name.replace(' ', '')

			# path of the file
			path_file = find_path(file_name)

			file_name = file_name.replace(path_file, '')
			
			# check if the name has an extension
			m_ext = p7.findall(file_name)
			if len(m_ext) > 0:
				extension = m_ext[-1]
				file_name = file_name.replace(extension, '')
			else:
				extension = '.tex'

			file_route = global_path + path_file + file_name + extension

			# recursive call to diagnostic_test
			diagnostic_test(file_route)
			new_segment_line  = file_x.replace(file_name, file_name+test_tag)
			line = line.replace(file_x, new_segment_line)
	return line




def diagnostic_test(name):
	"""Executes the Belcher diagnostic test on a file

	Keyword arguments:
	name -- Route to the LaTeX file
	"""
	path = find_path(name)

	# ideintify the extension of the file
	m_ext = p7.findall(name)
	if len(m_ext) > 0:
		extension = m_ext[-1]
		new_name = name.replace(extension, test_tag+extension)
	else:
		new_name = name + test_tag
	
	# opens the file and creates the file that will have the colored words
	tex_in_file = open_file(name, 'r')
	tex_out_file = open_file(new_name, 'w')

	# list of open environments
	environments = []

	# read the content of the file, process and write them into the optput
	line = tex_in_file.readline()
	while (line != ''):
		# check if this line is a comment
		m0 = p5.match(line)
		if m0 == None:
			# check if this line is the begining of the document
			m1 = p1.match(line)
			if m1 != None:
				# write the commands to color words
				for c in commands:
					tex_out_file.write(c + '\n')
			
			# check if the line imports another document
			line = check_recursion(line, path, p2)
			line = check_recursion(line, path, p3)
			line = check_recursion(line, path, p4)

			# check if the line opens or closes an environment
			for env in forbiden_env:
				p_env = re.compile('\{' + env + '\}')
				m_env = p_env.search(line)
				if m_env != None:
					# check if the environment is opened or closed
					p_open_env = re.compile('begin\s*\{' + env )
					m_open = p_open_env.search(line)
					if m_open != None:
						environments.append(env)
						break
					p_close_env = re.compile('end\s*\{' + env )
					m_close = p_close_env.search(line)
					if m_close != None:
						environments.remove(env)
						break

			valid_line = True
			for command in forbiden_commands:
				p_command = re.compile('\\\\'+command)
				m_command = p_command.match(line)
				if m_command != None:
					valid_line = False
				
	
			# check if there is any environment open
			if (len(environments) == 0) & (valid_line):

				# check if the line has any of the words to be highlighted
				if 'r' in actions:
					line = find_words(words_red, 'Red', line)
				if 'b' in actions:
					line = find_words(words_blue, 'Blue', line)
				if 'p' in actions:
					line = find_words(words_purple, 'Purple', line)
				if 'o' in actions:
					line = find_words(words_orange, 'Orange', line)
				if 'g' in actions:
					line = find_words(words_green, 'Green', line)
					line = find_end_words(wildcard_green, 'Green', line)
				if 'B' in actions:
					line = find_words(words_brown, 'Brown', line)
					line = find_end_words(wildcard_brown, 'Brown', line)

		tex_out_file.write(line)
		line = tex_in_file.readline()
	tex_in_file.close()
	tex_out_file.close()



def undo_diagnostic_test(name):
	"""Removes the commands of the diagnostic test

	Keyword arguments:
	name -- Route to the LaTeX file
	"""
	path = find_path(name)

	# ideintify the extension of the file
	m_ext = p7.findall(name)
	if len(m_ext) > 0:
		extension = m_ext[-1]
		new_name = name.replace(extension, undo_test_tag + extension)
	else:
		new_name = name + undo_test_tag
	
	# opens the file and creates the file that will have the colored words
	tex_in_file = open_file(name, 'r')
	tex_out_file = open_file(new_name, 'w')

	# read the content of the file, process and write them into the optput
	line = tex_in_file.readline()
	while (line != ''):
		# check if this line is a comment
		m0 = p5.match(line)
		if m0 == None:	
			m_color_command = p_color_command.finditer(line)
			# Remove the color commands of the line
			for m in m_color_command:
				word = remove_command(m)
				line = line.replace(m.group(), word)


		tex_out_file.write(line)
		line = tex_in_file.readline()
	tex_in_file.close()
	tex_out_file.close()




# check if there are enough input arguments
input_args = sys.argv

if (len(input_args) < 2):
	print('The program needs a latex source code')
	exit()
elif  (len(input_args) > 4):
	print('Too many arguments')
	exit()

# definition of punctuation symbols
punct = [".", "\,", ";", ":", "?", "\'", "\"", ""]

# text to be inserted in the preamble of the TeX files
commands = []
commands.append("%%%%% commands added automatically to highlight words")
commands.append(r"\RequirePackage{xcolor}")
commands.append(r"\definecolor{green}{rgb}{0,.9,.15}")
commands.append(r"\definecolor{violet}{rgb}{.8,.12,.86}")
commands.append(r'\newcommand{\BDTRed}[1]{{\color{red}#1}}')
commands.append(r'\newcommand{\BDTBlue}[1]{{\color{blue}#1}}')
commands.append(r'\newcommand{\BDTPurple}[1]{{\color{violet}#1}}')
commands.append(r'\newcommand{\BDTOrange}[1]{{\color{orange!50!yellow}#1}}')
commands.append(r'\newcommand{\BDTGreen}[1]{{\color{green}#1}}')
commands.append(r'\newcommand{\BDTBrown}[1]{{\color{brown!80!red}#1}}')
commands.append('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')
commands.append('')

# tag of new created files
test_tag = '_BDT'
undo_test_tag = '_undo'

# lists of words that will be highlighted
words_red = ['and', 'or']
words_blue = ['there', 'it', 'that', 'which', 'who']
words_purple = ['by', 'of', 'to', 'for', 'toward', 'on', 'at', 'from', 'in', 'with', 'as']
words_orange = ['this', 'these', 'those', 'their', 'them', 'they', 'its']
words_green = ['is', 'are', 'was', 'were', 'am', 'be', 'being', 'been', 'have', 'has', "hasn't", "haven't", 'having', 'did', 'does', "don't", 'doing', 'make', 'makes', 'making', 'provide', 'perform', 'get', 'seem', 'serve']
words_brown = ['not', 'very']

# list of words that have the following end will be highlighted
wildcard_green = ['ent', 'ence', 'ion', 'ize', 'ed']
wildcard_brown = ['ly']

# list of forbidden environments and commands
forbiden_env = ['tikz', 'tikzpicture']
forbiden_commands = ['usepackage']

#### definition of patterns for latex's commands
# begining of the document
p1 = re.compile('\s*\\\\begin\s*\{document\}')
# insertion of files 
p2 = re.compile('\s*\\\\include\s*\{[^\\\\]*\}')
p3 = re.compile('\s*\\\\input\s*\{[^\\\\]*\}')
p4 = re.compile('\s*\\\\subfile\s*\{[^\\\\]*\}')
# comments
p5 = re.compile('\s*\%')
# path of a file
p6 = re.compile('~?[\./\w\_\-\:\\\\]*[/\\\\]')
# extension of a file
p7 = re.compile('\.[\w\.]+')
# find file name
p8 = re.compile('\{.*\}')
# find '\node' at the beginning of the line
p_node = re.compile('\s*\\\\node')
# color's commands
p_color_command = re.compile("\\\\BDT(Red|Blue|Purple|Orange|Green|Brown)\s*\{[^\s]*\}")
p_color_word = re.compile('\{.*\}')

# define the set of actions to make in the text
set_actions = set()
for i in ['r', 'b', 'p', 'o', 'g', 'B']:
	set_actions.update(i)

actions = set()
tex_file = ''

if input_args[1][0] == '-':
	try:
		tex_file = input_args[2]
	except:
		exit('.tex file not found.')
	
	if input_args[1] == '--undo':
		undo_diagnostic_test(tex_file)
		exit()
	else:
		len_a = len(input_args[1])
		for i in input_args[1][1:len_a]:
			if i in set_actions:
				actions.update( i )
			else:
				exit('Parameter %s is not part of the available actions', i)
	
else:
	tex_file = input_args[1]
	actions = set_actions


# call the test method on the input file
diagnostic_test(tex_file)




