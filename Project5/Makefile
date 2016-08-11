all: submit

xor:
	python xor.py

customdataset:
	python extra_data.py

clean:
	rm -f *.pyc
	rm -f pjain67.zip

submit: pjain67.zip

pjain67.zip: clean
	zip pjain67.zip Testing.py NeuralNet.py NeuralNetUtil.py xor.py pjain67.pdf Makefile extra_data.py datasets/extra.data.txt