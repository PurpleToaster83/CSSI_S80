
**CSCI S-80 Week 6 Traffic Project TenserFlow Model Documentation**

Input Neurons: 900
Output Neurons: 43
Dimensions: 30 x 30 pixels

**Most values in the tables are approximate or ranges because the model often had small variations in numerical values**

I started by deciding on the options for paramaters that would influence function within the network. This became my Base Model:

# Table 1 - Non-Layer Architecture Related Parameters of Base Model

|       Model      |   Interpolation   |   Model Type  |   Optimizer   |           Losses           |            Metrics            |
| ---------------- | ----------------- | ------------- | ------------- | -------------------------- | ----------------------------- |
|     Base Model   |   INTER_LINEAR    |   Sequential  |     adam      |  categorical_crossentropy  |           accuracy            |


The layer architecture of my Base Model was based on the Sequential Model in handwritting.py but instead had a input_shape of (IMG_WIDTH, IMG_HEIGHT, 3). This model resulted in a 5.53% accuracy and a 3.5086 loss value. I noticed that for most of the values the number of filters in the covolution layer and number the of neurons in the hidden layer were base 2, so I decided I would scale by base 2 when changing those and similar paramters. I began with changing the number of filters from 2^5 to 2^(5 + 1) (see elements 1 of Table 2). Because using more filters slightly improved the accuracy, increasing the filter size would likely also greatly improve performance. I tested 5x5 and 7x7 filter sizes which drastically improved the networks performance (see elements 2 and 3 of Table 2). I then tried adding another convolution layer with 64 filters and a 3x3 kernal before and after the maxpooling layer (see elements 4 and 5 of Table 2). I decided to place another convolution layer after the pooling layer and experimented with the filter and kernal parameters of that layer, finding 32 filters with a 3x3 kernel worked best.


# Table 2 - Convolution Layer Kernel Size and Filter Approximate Effect on Accuracy

*the (2) below signifies that this is the second convolution layer*

| Kernel Size | Filters | Accuracy % |
| ----------- | ------- | ---------- |
|    3x3      |   64    |    5.82    |
|    5x5      |   64    |   90.95    |
|    7x7      |   64    |   89.78    |
|3x3 after (2)|   32    |   93.00    |
|3x3 before(2)|   32    |    5.66    |

 
After optimising the performance of the convolutional layers, I experimented with the performance of the pooling layers. I tried using a 4x4 and 3x3 kernal sizes for the pooling layer which resulted in a significant drop in accuracy (see elements 1 and 2 of Table 3). Because pooling reduces the total number of parameters while convolution layers increases the number of parameters, I tried a few runs where I increased the pool kernal size and increased the filter number in the suceeding convolution layer. I found that increasing the maxpooling kernal to 3x3 and increasing the filters to 64 improved the accuracy more than 2x2 kernal and 32 filters (see elements 3 and 4 of Table 3). I then tried adding another pooling layer after the last convolution layer but before the flatten with a 2x2 kernal (see element 5 of Table 3). Next, I tried increasing the second maxpool kernal size to 4x4 and a 3x3 (see elements 6 and 7 of Table 3). I decided not to keep the second maxpooling layer becuase it didn't vastly improve the networks accuracy performance, but did add more complexity to the netowork.

# Table 3 - Pooling Kernal Size Approximate Effect on Accuracy

*the (2) below signifies that this is the second pooling layer*

| Kernel Size | Filters | Accuracy % |
| ----------- | ------- | ---------- |
|    4x4      |   32    |    ~ 5     |
|    3x3      |   32    |    ~ 5     |
|    3x3      |   64    |   90 - 95  |
|    2x2      |   32    |   89 - 94  |
|  2x2 (2)    |   64    |   ~ 93     |
|  4x4 (2)    |   64    |   ~ 64     |
|  4x4 (2)    |   64    |   ~ 90     |


The next layer I wanted to optimize was the hidden layer, specifically the number of hidden neurons. I went about choosing numbers to compare by looking at base two numbers. The results I got indicated that a higher numbers of hidden neurons improved accuracy (see elements 1-4 of Table 4); however, too many neurons both started to slightly decrease accuracy and greatly impacted the time to run 10 epochs. I decided to stay at 128 hidden neurons rather than using 256 to maximize accuracy and decrease the complexity of the network model. Also involving the hidden layers, I wanted to see the effects of another hidden layer so I created a second 128 neuron hidden layer (see element 5 of Table 4). I tried similar neuron numbers with the second layer (see elements 5-8 of Table 4). I decided to exclude this second layer because it didn't increase the accuracy performance by a lot, but added a lot more paramters and complexity to the network. 

# Table 4 - Hidden Layer Neuron Count Approximate Effect on Accuracy

*the (2) below signifies that this is the second hidden layer*

| Hidden Layer Neurons | Accuracy |
| -------------------- | -------- |
|         64           |   ~ 5    |
|        128           |  ~ 95    |
|        256           |  ~ 95    |
|        512           |  ~ 94    |
|      128 (2)         |  ~ 95    |
|       64 (2)         |  ~ 91    |
|      256 (2)         |  ~ 96    |
|      512 (2)         |  ~ 95    |


One of the last things I wanted to try was adjusting the dropout rate which was originally at 50% so that I could make my model efficient but not overfit the training data. I decided I would test values at 10% intervals below 50% because it seems that values over 50% would be reducing the number of neurons by too large of a factor (see Table 5). Although 0% and 20% dropout rates scored 1% higher, I decided to keep the dropout rate at 50% to better ensure that the model doesn't become overfit.

# Table 5 - Dropout Percentage Apprximate Effect on Accuracy

| Dropout % | Accuracy % |
| --------- | ---------- |
|     0     |     96     |
|    10     |     88     |
|    20     |     96     |
|    30     |     94     |
|    40     |     95     |
|    50     |     95     |


At this point, I wanted to evaluate the model with multiple runs (see Table 6).

# Table 6 - Performance of Network Model (Pre-Revision)

| Run # | Accuracy % |  Loss  |
| ----- | ---------- | ------ |
|   0   |   95.91    | 0.1859 |
|   1   |   96.50    | 0.2186 |
|   2   |   94.02    | 0.3099 |
|   3   |   95.13    | 0.2642 |
|   4   |   96.09    | 0.1731 |
|   5   |   94.83    | 0.1985 |
|   6   |   97.13    | 0.1229 |
|   7   |   93.95    | 0.2561 |
|   8   |   91.67    | 0.3365 |
|   9   |   95.18    | 0.1960 |

-------------------------------

| Mean  |   95.041   | 0.22617|
| Median|   95.155   | 0.20855|
| Range |    5.46    | 0.1634 |


I decided I would make one last round of revisions to see if I could beat the 95% accuracy and 0.22617 loss mean values of my model. The previous evidence has pointed towards more neurons, filters, etc oftentimes increasing the accuracy, despite increasing the network's complexity and the time to train the model. I first wanted to try re-implementing a second maxpooling layer with a 2x2 kernal, resulting in a 95.02% accuracy and 0.1944 loss. I then wanted to scale other values in the network that seemed to optimize perfomance, following the rule of thumb output neurons is less than hidden neurons is less than input neurons. I then wanted to try increasing the number of filters in both convolution layers (see elements 1 and 2 of Table 7). I thought that the many filters of the convolution layer could serve as inputs to more hidden neurons, so I increased the number of hidden neurons also (see elements 3 and 4 of Table 7). I eventually found that 256 for both convolution layers and 512 hidden neurons worked well which made sense because the filters summed to 512 and then went into 512 hidden neurons. I decided not to test more activation functions for the model because the compiling took a long time (~ 30-35 sec. / epoch) and the ReLU activation function was the least complex as opposed to other activation functions like sigmoid or GeLU.

# Table 7 - Performance of Network Model (Intra-Revision)

| Conv. 1 Filters | Conv. 2 Filters | Hidden Neurons | Accuracy % |  Loss  |
| --------------- | --------------- | -------------- | ---------- | ------ |
|      128        |       128       |      128       |    5.59    | 3.4940 |
|      256        |       256       |      128       |    5.58    | 3.4957 |
|      256        |       256       |      256       |   94.19    | 0.2422 |
|      256        |       256       |      512       |   94.59    | 0.2416 |


Conclusion:

Below is an evaluation of the final model running 10 time with 10 epochs and running 5 times with 20 epochs. The adjustments got it to about 95% accuracy at 10 epochs; however, the accuracy increased by about 2% when I doubled the epochs. The training time for the 20 epoch runs ranged from about 36-41 sec. / epoch which might not be worthwile for the 2% increase from 10 epochs.


# Table 8 - Performance of Final Convolutional Neural Network Model

| Run # | # Epochs | Accuracy % |  Loss  |
| ----- | -------- | ---------- | ------ |
|   0   |    10    |   97.12    | 0.1174 |
|   1   |    10    |   93.59    | 0.2730 |
|   2   |    10    |   95.83    | 0.1756 |
|   3   |    10    |   95.97    | 0.2250 |
|   4   |    10    |   95.36    | 0.2046 |
|   5   |    10    |   80.97    | 0.7181 |
|   6   |    10    |   97.18    | 0.1541 |
|   7   |    10    |   94.75    | 0.2269 |
|   8   |    10    |   95.18    | 0.2216 |
|   9   |    10    |   94.85    | 0.2550 |

------------------------------------------

|      Mean        |   94.08    | 0.2571 |
|      Median      |   95.27    | 0.2233 |
|      Range       |   16.21    | 0.6007 |

------------------------------------------

|  10   |    20    |   97.03    | 0.2407 |
|  11   |    20    |   97.79    | 0.1609 |
|  12   |    20    |   97.05    | 0.2587 |
|  13   |    20    |   91.85    | 0.3045 |
|  14   |    20    |   96.35    | 0.2320 |

-------------------------------------------

|      Mean        |   96.01    | 0.2394 |
|      Median      |   97.03    | 0.2407 |
|      Range       |    5.94    | 0.0638 |

