import os
import argparse
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image_dataset_from_directory


def test(model_path, test_dataset, batch_size):
    print(f'Loading Model at {model_path}')
    model = load_model(model_path, compile=False)
    model.compile(
        loss = 'categorical_crossentropy',
        optimizer = tf.keras.optimizers.SGD(learning_rate = 0.1),
        metrics=['accuracy']
    )
    
    config = model.get_config() # Returns pretty much every information about your model
    input_size = config["layers"][0]["config"]["batch_input_shape"][1:3]
    print(f'Input Size is: {input_size}')

    print(f'Loading Dataset at {test_dataset}')
    test_ds = image_dataset_from_directory(
        test_dataset,               # chemin vers le jeu de données
        seed=42,                    # Initialisation du générateur aléatoire (permutations)
        image_size=input_size,       # Taille des images d'entrée
        batch_size=batch_size,      # Taille du mini-batch
        label_mode='categorical'    # Conversion au format One-Hot
    )

    print(f'Calculating Score')
    score = model.evaluate(test_ds, steps = len(test_ds), workers = 1, verbose = 2)
    print(f'Score is: {score[1] * 100}')
    
    return score

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--dataset')
    parser.add_argument('-m', '--model')
    parser.add_argument('-b', '--batch_size', default = 32)
    args = parser.parse_args()
    test(args.model, args.dataset, args.batch_size)