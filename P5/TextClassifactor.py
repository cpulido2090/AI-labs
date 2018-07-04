#########################################
#										#
#	CARLOS PULIDO MARQUEZ - 163842		#
#	ALBERT BOVE CASTELLVI - 163729		#
#										#
#####################################

from os import listdir
import operator, argparse, sys


def getWords(diccionario):

	for file in listdir('./dataset/'):
		file_read= open('./dataset/'+ file,'r')
	
		#Leemos linia a linia cada fichera, y para cada palabra la anadimos al diccionario si no aparece,
		#en caso contrario, le aumentamos en 1 el numero de apariencias
		for line in file_read:
			line = line.decode('latin_1').encode('utf-8').split()
			for word in line:
				word = word.replace('\'','')
				word = word.strip()
				if not word == '':
					if not diccionario.has_key(word):
						diccionario[word]=1
					else:
						diccionario[word]+=1
		file_read.close()
	return diccionario

def getFrequentWords(diccionario):
	#En frequentWord, ordenamos de mayor a menor las palabras del diccionario, y guardamos
	#las N palabras mas frecuentes
	frequentWord = sorted(diccionario.items(), key=operator.itemgetter(1),reverse=True)
	frequentWord = frequentWord[0:n]

	return frequentWord

def calculateFrequencies(arff_file, frequentWord):
	#A continuacion empezamos a generar el fichero .arff para poder utilizar el wefa
	#Primerament, anadimos las N palabras mas relevantes
	file_write = open(arff_file, 'w')
	file_write.write('@RELATION trainning\n\n')
	for word, frequency in frequentWord:
		file_write.write('@ATTRIBUTE \''+ word + '\' NUMERIC\n')
	file_write.write('@ATTRIBUTE \'gender\' {male,female}\n')
	file_write.write('@DATA\n')

	#Volvemos a leer los ficheros del dataset para comprovar fichero a fichero,
	#en que frecuencia aparecen las N palabras mas frequentes en cada fichero
	for file in listdir('./dataset/'):

		file_read= open('./dataset/'+ file,'r')
		wordInFile = dict()
		lenFile = 0
		for line in file_read:
			line = line.decode('latin_1').encode('utf-8').split()

			for word in line:
				lenFile+=1
				for w,f in frequentWord:
					if w == word:
						if not wordInFile.has_key(word):
							wordInFile[word]=1
						else:
							wordInFile[word]+=1

		#Para cada fichero, una vez leido todo el fichero, calculmaos las frecuencias
		#para cada palabra, en caso de que la palabra no se encuentre en el fichero, aplicaremos
		#el smmoothing
		for w,f in frequentWord:

			if w in wordInFile:
				wordInFile[w] = str((float(wordInFile[w])/lenFile)*100)[0:4]
				file_write.write(wordInFile[w]+ ',')
			else:
				file_write.write(str(float(1/n)*100)+',')

		file_write.write(file.split('_')[1]+'\n')
		file_read.close()

	file_write.close()

##MAIN##

#Parseamos la entrada por consola
#El parametro para introducir el numero de palabras mas frecuentes en el dataset es n
parser = argparse.ArgumentParser(description='Number of frequency words')
parser.add_argument( '-n', '--num',help='Number of frequency words')
args= parser.parse_args()
n = int(args.num)

#Creamos un diccionario donde guardaremos las diferentes palabras que aparecen en los
#ficheros de dataste y vamos acumulando sus apariencias
diccionario = dict()
diccionario = getWords(diccionario)
print '\nDataset read'

frequentWord = getFrequentWords(diccionario)
print 'Calculating frequencies'
arff_file = 'datasetFrequencies_'+str(n)+'.arff'
calculateFrequencies(arff_file,frequentWord)

print 'Arff file generated'



