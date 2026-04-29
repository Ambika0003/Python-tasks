# ==========================================================================================================
#================================scikit-learn===========================================
# performing Linear Regression on euquation X = 7a + 3b + 4c + 9d
# ==========================================================================================================

#Import the libraries 
from random import randint 
from sklearn.linear_model import LinearRegression

# Create a range limit for random numbers and a count of the number of rows
train_set_limit=1000
train_set_count=100

# Create an empty list of the input set 'X' and output for each training set 'Y'
train_input=list()
train_output=list()

##Create and append a randomly generated data set to the input and output
for i in range(train_set_count):
    a= randint(0, train_set_limit)
    b= randint(0, train_set_limit)
    c= randint(0, train_set_limit)
    d= randint(0, train_set_limit)
    #Create a linear function for the output dataset 'Y' 
    op=(7*a)+(3*b)+(4*c)+(9*d)
    train_input.append ([a,b,c,d])
    train_output.append(op)

#Create a linear regression object 
predictor=LinearRegression(n_jobs=-1)
#fit the linear model
predictor.fit(X=train_input, y=train_output)

#Create our testing data set
X_test= [[10,20,30,40]]

# Predict the ouput of the test data
outcome=predictor.predict(X=X_test)

#The estimated coefficients for the linear regression problem.
coefficients= predictor.coef_

#print the outcome
print("the outcome of the dataset is:")
print('Outcome:{}\nCoefficients:{}'.format(outcome,coefficients))