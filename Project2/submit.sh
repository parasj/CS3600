#!/bin/bash
rm submit.zip autograder.out extracredit.out
python autograder.py > autograder.out
python autograder.py -t ExtraCredit/6queens.test > extracredit.out  
zip -r submit.zip BinaryCSP.py ExtraCredit autograder.out extracredit.out