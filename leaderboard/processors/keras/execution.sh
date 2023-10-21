docker run -v /home/mohamed/Projects/lbml/leaderboard/media/files/test/test:/code/dataset -v /home/mohamed/Projects/lbml/leaderboard/media/submissions/small_xpection_2023_sidi.h5:/code/model.h5 -v /home/mohamed/Projects/lbml/leaderboard/processors/keras/fire_detection_keras.py:/code/script.py tensorflow/tensorflow:2.8.4 python /code/script.py -d /code/dataset -m /code/model.h5

docker run -v /home/mohamed/Projects/lbml/leaderboard/media/files/test/test:/code/dataset -v /home/mohamed/Projects/lbml/leaderboard/media/submissions/small_xpection_2023_sidi.h5:/code/model.h5 fennecinspace/hackia-keras-fire-classify python /code/script.py -d /code/dataset -m /code/model.h5


docker run -v Resource.name[FIRE_CLASSIFICATION_TEST_DATASET]:/code/dataset -v Submission.file:/code/model.h5 fennecinspace/hackia-keras-fire-classify python /code/script.py -d /code/dataset -m /code/model.h5