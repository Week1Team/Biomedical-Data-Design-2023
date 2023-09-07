# Biomedical-Data-Design-2023
This algorithm starts with a set of rankings of hospitals provided by doctors, and can perform the following tasks:
<br> Identify whether there are enough positions.
<br> Convert the NAN value to equally unwanted positions.
<br> Determine the solution with minimum costs through algorithm based on Hungarian.
<br> Output match result between doctors and hospitals.
<br> 
<br> Input Requirements：
<br> To run this algorithm, the input should be:
<br> - an N x L NumPy array, each row represents a ranking a certain doctor provides for all hospitals (positions).
<br> - an L Numpy array, each position represent the capacity of the hospital.
<br> 
<br> Output:
<br> - an N Numpy array, each position represent a matched hospital to that doctor.
<br> 
<br> How to use:
<br> 1. open main file, input the ranking array of doctors and the capacity of each hospital, and see the match result.
<br> 2. open test file, play with the parameters and test.
