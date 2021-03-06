from models.resnet import setup_resnet_2d_model
from utilities.train import *


def run_resnet_test(data, num_classes, device, recover, ckpt_path, prev_epochs,
                    epochs):
  # Create Model
  print("Setting up model...")
  data_shape = list(data['X_train'][0].shape)
  model = setup_resnet_2d_model(data_shape, num_classes, learning_rate=1e-3)
  saver = tf.train.Saver()
  sess = tf.Session()
  sess.run(tf.global_variables_initializer())

  # Recover Saved Model (if available)
  if recover:
    print("Recovering model...")
    recover_model_checkpoint(sess, saver, 'checkpoints/')

  # Train Model
  print("Training model...")
  train_model(device, sess, model, data['X_train'], data['y_train'],
              epochs=epochs, batch_size=64, is_training=True, log_freq=100,
              plot_loss=False)

  # Check Final Training Accuracy
  print("\nFinal Training Accuracy:")
  train_model(device, sess, model, data['X_train'], data['y_train'], epochs=1,
              batch_size=64, is_training=False, log_freq=100, plot_loss=False)

  # Check Validation Accuracy
  print('\nFinal Validation Accuracy:')
  train_model(device, sess, model, data['X_val'], data['y_val'], epochs=1,
              batch_size=64, is_training=False, log_freq=100, plot_loss=False)

  # Save Model Checkpoint
  save_model_checkpoint(sess, saver, ckpt_path, prev_epochs + epochs)
