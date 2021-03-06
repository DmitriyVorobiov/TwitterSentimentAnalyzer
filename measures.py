import tensorflow as tf
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt


def measure(dim):
    # Import data
    data = pd.read_csv('result.csv')

    # Drop date variable
    data['date'] = pd.to_datetime(data['date'])
    data['day_of_week'] = data['date'].dt.dayofweek / 2 - 1
    data['day_of_week'] = data["day_of_week"].astype('category')

    cols = ['eur_sent_mean', 'aur_close', 'eurusd_close']
    # cols = ['aur_close', 'eurusd_close']

    data = data[cols]

    data_frozen = data.copy()
    for i in range(4):
        data = pd.concat([data, data_frozen.shift(-i - 1)], axis=1)

    # data.fillna(method='ffill', inplace=True)
    data = data.dropna()

    # Dimensions of dataset
    n = data.shape[0]
    p = data.shape[1]

    # Make data a np.array
    data = data.values

    # Training and test data
    train_start = 0
    train_end = int(np.floor(0.8 * n))
    test_start = train_end + 1
    test_end = n
    data_train = data[np.arange(train_start, train_end), :]
    data_test = data[np.arange(test_start, test_end), :]

    # Scale data
    scaler = MinMaxScaler(feature_range=(-1, 1))
    scaler.fit(data_train)
    data_train = scaler.transform(data_train)
    data_test = scaler.transform(data_test)

    # Build X and y
    X_train = data_train[:-1, 0:]
    y_train = data_train[1:, 2] # data_train[1:, 1]
    X_test = data_test[:-1, 0:]
    y_test = data_test[1:, 2] # data_test[1:, 1]

    # Number of stocks in training data
    n_stocks = X_train.shape[1]

    # Neurons
    n_neurons_1 = 1024
    n_neurons_2 = 512
    n_neurons_3 = 256
    n_neurons_4 = 128

    # Session
    net = tf.InteractiveSession()

    # Placeholder
    X = tf.placeholder(dtype=tf.float32, shape=[None, n_stocks])
    Y = tf.placeholder(dtype=tf.float32, shape=[None])

    # Initializers
    sigma = 1
    weight_initializer = tf.variance_scaling_initializer(mode="fan_avg", distribution="uniform", scale=sigma)
    bias_initializer = tf.zeros_initializer()

    # Hidden weights
    W_hidden_1 = tf.Variable(weight_initializer([n_stocks, n_neurons_1]))
    bias_hidden_1 = tf.Variable(bias_initializer([n_neurons_1]))
    W_hidden_2 = tf.Variable(weight_initializer([n_neurons_1, n_neurons_2]))
    bias_hidden_2 = tf.Variable(bias_initializer([n_neurons_2]))
    W_hidden_3 = tf.Variable(weight_initializer([n_neurons_2, n_neurons_3]))
    bias_hidden_3 = tf.Variable(bias_initializer([n_neurons_3]))
    W_hidden_4 = tf.Variable(weight_initializer([n_neurons_3, n_neurons_4]))
    bias_hidden_4 = tf.Variable(bias_initializer([n_neurons_4]))

    # Output weights
    W_out = tf.Variable(weight_initializer([n_neurons_4, 1]))
    bias_out = tf.Variable(bias_initializer([1]))

    # Hidden layer
    hidden_1 = tf.nn.relu(tf.add(tf.matmul(X, W_hidden_1), bias_hidden_1))
    hidden_2 = tf.nn.relu(tf.add(tf.matmul(hidden_1, W_hidden_2), bias_hidden_2))
    hidden_3 = tf.nn.relu(tf.add(tf.matmul(hidden_2, W_hidden_3), bias_hidden_3))
    hidden_4 = tf.nn.relu(tf.add(tf.matmul(hidden_3, W_hidden_4), bias_hidden_4))

    # Output layer (transpose!)
    out = tf.transpose(tf.add(tf.matmul(hidden_4, W_out), bias_out))

    # Cost function
    mse = tf.reduce_mean(tf.squared_difference(out, Y))

    # Optimizer
    opt = tf.train.AdamOptimizer().minimize(mse)

    # Init
    net.run(tf.global_variables_initializer())

    # Setup interactive plot
    # plt.ion()
    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    line1, = ax1.plot(y_test)
    line2, = ax1.plot(y_test * 0.5)
    plt.show()

    # Fit neural net
    batch_size = 256
    mse_train = []
    mse_test = []

    # Number of epochs and batch size
    epochs = 10

    for e in range(epochs):

        # Shuffle training data
        shuffle_indices = np.random.permutation(np.arange(len(y_train)))
        X_train = X_train[shuffle_indices]
        y_train = y_train[shuffle_indices]

        # Minibatch training
        for i in range(0, len(y_train) // batch_size):
            start = i * batch_size
            batch_x = X_train[start:start + batch_size]
            batch_y = y_train[start:start + batch_size]
            # Run optimizer with batch
            net.run(opt, feed_dict={X: batch_x, Y: batch_y})

            # Show progress
            if np.mod(i, 99) == 0:
                # Prediction
                pred = net.run(out, feed_dict={X: X_test})

                # fig = plt.figure()
                # ax1 = fig.add_subplot(111)
                # lineS, = ax1.plot(y_test)
                # line1, = ax1.plot(pred[0])
                # plt.title('Epoch ' + str(e) + ', Batch ' + str(i))
                # plt.show()
                # file_name = 'img/epoch_' + str(e) + '_batch_' + str(i) + '.png'
                # plt.savefig(file_name)
                # plt.pause(0.01)
                # print(net.run(mse, feed_dict={X: X_test, Y: y_test}))
    # Print final MSE after Training
    mse_final = net.run(mse, feed_dict={X: X_test, Y: y_test})
    print(mse_final)
    return mse_final
