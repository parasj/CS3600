#!/bin/bash
rm submission.zip autograder.out
(cd search && python autograder.py) > autograder.out
zip submission autograder.out search/search.py search/searchAgents.py