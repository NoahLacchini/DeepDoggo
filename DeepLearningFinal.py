"""
Created on Sun Apr 23 15:55:37 2023
@author: CYTech Student
"""
import tensorflow as tf
from keras import layers, models, optimizers

VIR_FILE_PATH = "data/viral2.txt"
NONVIR_FILE_PATH = "data/nonviral2.txt"
CHECKPOINT_PATH = "checkpoints/cp-{epoch:03d}.ckpt"
SAVED_MODEL_PATH = "saved_model/model.h5"

# Dataset infos --------------------

DATASET_SIZE = 49220324
WEIGHTS = [0.026, 0.974]
INPUT_SHAPE = (50, 4, 1)
# ----------------------------------

SHUFFLE_BUFFER_SIZE = 10000
DATASET_SPLIT = [0.8, 0.2]

# Hyper parameters -----------------
EPOCHS = 150
BATCH_SIZE = 64
# ----------------------------------

# One-hot encode the sequences
def one_hot_encode(sequence, y):
    # Split the string tensor into individual characters
    chars = tf.strings.unicode_split(sequence, 'UTF-8')

    # Generate a mapping from characters to indices
    vocabulary = tf.constant(['A', 'T', 'C', 'G'])
    char_to_index = tf.lookup.StaticHashTable(
        tf.lookup.KeyValueTensorInitializer(vocabulary, tf.range(tf.size(vocabulary))),
        default_value=-1
    )

    # Convert each character to its corresponding index
    char_indices = char_to_index.lookup(chars)

    # Perform one-hot encoding
    one_hot_encoded = tf.one_hot(char_indices, depth=tf.size(vocabulary))
    one_hot_encoded = tf.reshape(one_hot_encoded, shape=INPUT_SHAPE)

    return one_hot_encoded, y

def get_dataset_partitions_tf(ds, ds_size, train_split=0.8, test_split=0.2, shuffle=True, shuffle_size=10000):
    assert (train_split + test_split) == 1
    
    if shuffle:
        ds = ds.shuffle(shuffle_size, seed=12)

    train_size = int(train_split * ds_size)
    test_size = ds_size - train_size
    
    train_ds = ds.take(train_size)
    test_ds = ds.skip(train_size)
    
    return train_ds, test_ds

# Extract the data from the two files and combine it into one dataset
def extract_data(vir_file_path, nonvir_file_path):
    # Create positive dataset
    positive_dataset = tf.data.TextLineDataset(vir_file_path)
    positive_dataset = positive_dataset.map(lambda line: (line, tf.constant(1)))  # Set class to 0 for negative samples

    # Create negative dataset
    negative_dataset = tf.data.TextLineDataset(nonvir_file_path)
    negative_dataset = negative_dataset.map(lambda line: (line, tf.constant(0)))  # Set class to 0 for negative samples

    # Combine positive and negative datasets
    combined_dataset = tf.data.Dataset.sample_from_datasets([positive_dataset, negative_dataset], weights=WEIGHTS)
    combined_dataset = combined_dataset.map(one_hot_encode)

    return combined_dataset


def construct_model():
    # Create model
    model = models.Sequential()
    model.add(layers.Conv2D(64, (2, 1), activation='relu', input_shape=INPUT_SHAPE))
    model.add(layers.MaxPooling2D((2, 1)))
    model.add(layers.BatchNormalization())  # Add BatchNormalization layer
    model.add(layers.Dropout(0.25))  # Add Dropout layer
    model.add(layers.Flatten())
    model.add(layers.Dense(54, activation='relu'))
    model.add(layers.Dropout(0.25))  # Add Dropout layer
    model.add(layers.Dense(1, activation='sigmoid'))
    optimizer = optimizers.Adam(learning_rate=0.0005)
    # Compile model
    model.compile(loss='binary_crossentropy', optimizer=optimizer, metrics=['accuracy'])

    return model

# Calculate 
def evaluate_model(actual, prediction):
    TP = TN = FP = FN = 0  # Initialize the counters

    # Iterates over the results
    for ac, pred in zip(actual, prediction):
        if ac == 1:
            if pred >= 0.5:
                TP += 1
            else:
                TN += 1
        else:
            if pred >= 0.5:
                FP += 1
            else:
                FN += 1

    precision = TP / (TP + FP)
    recall = TP / (TP + FN)
    f1 = 2 * precision * recall / (precision + recall)

    return precision, recall, f1

def main():
    # Extract the dataset
    dataset = extract_data(VIR_FILE_PATH, NONVIR_FILE_PATH)

    # Splits the data
    dataset_train, dataset_test = get_dataset_partitions_tf(
        dataset, DATASET_SIZE,
        DATASET_SPLIT[0], DATASET_SPLIT[1],
        shuffle_size=SHUFFLE_BUFFER_SIZE)
    
    # Batch the dataset
    dataset_train = dataset_train.batch(BATCH_SIZE)
    dataset_test = dataset_test.batch(BATCH_SIZE)

    # Create the model once
    model = construct_model()

    # Create a callback that saves the model's weights
    cp_callback = tf.keras.callbacks.ModelCheckpoint(
        filepath=CHECKPOINT_PATH, 
        verbose=1, 
        save_weights_only=True,
        save_freq='epoch',
        period=5)
    
    # model.summary()

    # Fit the data
    model.fit(dataset_train, epochs=EPOCHS, batch_size=BATCH_SIZE, callbacks=[cp_callback])
    
    # Save model
    model.save(SAVED_MODEL_PATH)

    # Evaluate the keras model
    prediction = model.predict(dataset_test)
    actual = dataset.map(lambda x, y: y)
    precision, recall, f1 =evaluate_model(actual, prediction)

    print("Precision : ", precision)
    print("Recall : ", recall)
    print("F1 score : ", f1)

main()
