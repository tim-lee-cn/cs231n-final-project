import math
import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt

# Save Checkpoint of Model
def save_model_checkpoint(session, saver, filename, epoch_num):
  save_path = saver.save(session, filename, epoch_num)
  print("\nCheckpoint saved in file: %s" % save_path)

# Recover Saved Model Checkpoint
def recover_model_checkpoint(session, saver, checkpoint_path):
  saver.restore(session, tf.train.latest_checkpoint(checkpoint_path))
  print("Model restored!\n")

# Train the Model
def train_model(device, sess, model, X_data, labels, epochs=1, batch_size=64,
                is_training=False, log_freq=100, plot_loss=False):

  with tf.device(device):
    # Calculate Prediction Accuracy
    correct_prediction = tf.equal(tf.argmax(model['y_out'],1), model['y'])
    accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

    # Shuffle Training Data
    train_indicies = np.arange(X_data.shape[0])
    np.random.shuffle(train_indicies)

    # Populate TensorFlow Variables
    variables = [model['loss_val'], correct_prediction, accuracy]
    if is_training:
      variables[-1] = model['train_step']

    # Iteration Counter 
    iter_cnt = 0
    losses = []
    for epoch in range(epochs):
      # Keep Track of Loss and Number of Correct Predictions
      num_correct = 0
      epoch_loss = 0

      # Iterate Over the Entire Dataset Once
      for i in range(int(math.ceil(X_data.shape[0] / float(batch_size)))):
        # Indices for Batch
        start_idx = (i * batch_size) % X_data.shape[0]
        idx = train_indicies[start_idx:start_idx + batch_size]
        actual_batch_size = labels[i:i + batch_size].shape[0]

        # Feed Dictionary for Batch
        feed_dict = {model['X']: X_data[idx,:],
                     model['y']: labels[idx],
                     model['is_training']: is_training}

        # Run TF Session (Returns Loss and Correct Predictions)
        loss, corr, _ = sess.run(variables, feed_dict=feed_dict)
        # print(loss)
        num_correct += np.sum(corr)
        epoch_loss += loss * actual_batch_size

        # Print Loss and Accuracies
        if is_training and (iter_cnt % log_freq) == 0:
          print("Iteration {0}: Training Loss = {1:.3g} and Accuracy = {2:.2g}"\
                .format(iter_cnt + 1, loss, np.sum(corr) / float(actual_batch_size)))
        iter_cnt += 1

      # Calculate Performance
      accuracy = num_correct / float(X_data.shape[0])
      total_loss = epoch_loss / float(X_data.shape[0])
      losses.append(total_loss)

      print("Epoch {0}: Overall Loss = {1:.3g} and Accuracy = {2:.3g}"\
            .format(epoch + 1, total_loss, accuracy))

    if plot_loss:
      plt.plot(losses)
      plt.grid(True)
      plt.xlim(-10, 800)
      plt.title('Total Loss vs. Epoch')
      plt.xlabel('Epoch')
      plt.ylabel('Total Loss')
      plt.show()

  return total_loss, accuracy