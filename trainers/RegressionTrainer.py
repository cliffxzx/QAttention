import tensorflow as tf
from tensorflow.keras import layers
from datasets import DatasetWrapper
from models import get_model
from utils.lr_finder import LRFinder, MaxStepStoppingWithLogging

def train(args, dataset: DatasetWrapper):
    vectorize_layer = layers.TextVectorization(
        standardize="lower_and_strip_punctuation",
        output_mode='int',
        output_sequence_length=args.seq_len
    )

    train_data, test_data = dataset.getData(args.batch_size)

    train_text = train_data.flat_map(lambda text, label: tf.data.Dataset.from_tensor_slices(text))
    vectorize_layer.adapt(train_text)
    vocab_size = vectorize_layer.vocabulary_size()
    print('Vocab size:', vocab_size)

    model = tf.keras.models.Sequential([
        tf.keras.Input(shape=(1,), dtype=tf.string),
        vectorize_layer,
        get_model(args, vocab_size),
        layers.GlobalAveragePooling1D(),
        layers.Dense(1),
    ])

    mss_l = MaxStepStoppingWithLogging(max_steps=-1) # just logging
    lr_finder = LRFinder(
                    train_data,
                    args.batch_size,
                    window_size=int(args.lr_finder[0]),
                    max_steps=int(args.lr_finder[1]),
                    filename=args.lr_finder[2]
                )
    callbacks = [mss_l]
    if args.lr <= 0:
        callbacks.append(lr_finder)

    lr_decayed_fn = tf.keras.optimizers.schedules.CosineDecay(args.lr, args.epochs * len(train_data), alpha=1e-2)
    opt = tf.keras.optimizers.Adam(learning_rate=lr_decayed_fn)

    model.compile(
        opt,
        loss=tf.keras.losses.MeanSquaredError(),
    )

    print(model.summary())
    fitting = model.fit(
                train_data,
                batch_size=args.batch_size,
                epochs=args.epochs,
                validation_data=test_data,
                verbose=1,
                callbacks=callbacks
            )

    fitting.history['batch'] = mss_l.history

    return fitting
