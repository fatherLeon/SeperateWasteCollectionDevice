import os
import cv2
import numpy as np
import tensorflow as tf

WIDTH = 60
HEIGHT = 60
BATCH = 32

def loadImage(path):
    '''
    Input - path
    Output - numpy array(Image)
    '''
    print(f"Loading Image : {path}")
    data = []
    listName = os.listdir(path)
    for fileName in listName:
        img = cv2.imread(path + fileName, cv2.IMREAD_COLOR)
        img = cv2.resize(img, dsize=(HEIGHT, WIDTH), interpolation=cv2.INTER_AREA)
        img = img / 255
        data.append(img)

    return np.array(data).astype("float16")

def learnModel(input_tensor):
    x = tf.keras.layers.Conv2D(8, (3, 3), activation='relu', padding='same')(input_tensor)
    x = tf.keras.layers.Conv2D(8, (3, 3), activation='relu', padding='same')(x)
    x = tf.keras.layers.MaxPooling2D((2, 2))(x)

    x = tf.keras.layers.Conv2D(32, (3, 3), activation='relu', padding='same')(x)
    x = tf.keras.layers.Conv2D(32, (3, 3), activation='relu', padding='same')(x)
    x = tf.keras.layers.Conv2D(32, (3, 3), activation='relu', padding='same')(x)
    x = tf.keras.layers.MaxPooling2D((2, 2))(x)

    x = tf.keras.layers.Flatten()(x)
    x = tf.keras.layers.Dense(64, activation="relu")(x)
    output_tensor = tf.keras.layers.Dense(2, activation='softmax')(x)

    return output_tensor

trainDatagen = tf.keras.preprocessing.image.ImageDataGenerator(
    rescale=1./255,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True,
    validation_split=0.2
)
testDatagen = tf.keras.preprocessing.image.ImageDataGenerator(rescale=1./255)

trainSet = trainDatagen.flow_from_directory("./train",
                                              target_size=(WIDTH, HEIGHT),
                                              batch_size=BATCH,
                                              class_mode="binary")
validationSet = trainDatagen.flow_from_directory(
    "./train",
    target_size=(WIDTH, HEIGHT),
    batch_size=BATCH,
    class_mode="binary",
    subset="validation"
)
testSet = testDatagen.flow_from_directory("./test",
                                            target_size=(WIDTH, HEIGHT),
                                            batch_size=BATCH,
                                            class_mode="binary")

inputs = tf.keras.layers.Input(shape=(WIDTH, HEIGHT, 3))
outputs = learnModel(inputs)

model = tf.keras.models.Model(inputs, outputs)

modelFilePath = "./model/model1-{epoch:04d}-{val_loss:.4f}.h5"
checkpoint = tf.keras.callbacks.ModelCheckpoint(modelFilePath, monitor="val_acc", verbose=1, save_best_only=False, save_freq='epoch')
logger = tf.keras.callbacks.CSVLogger("ModelLog.csv", separator=",", append=False)

model.compile(optimizer="adam",
              loss="sparse_categorical_crossentropy",
              metrics=['acc'])

model.fit_generator(trainSet, steps_per_epoch=trainSet.samples//BATCH,
                    validation_data=validationSet,
                    validation_steps=validationSet.samples//BATCH,
                    epochs=1000, callbacks=[checkpoint, logger])

print(model.evaluate_generator(testSet))