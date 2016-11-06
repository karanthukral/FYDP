import itertools
from os import path

from ngram import NGram
import numpy as np
import tensorflow as tf

from sklearn.cross_validation import train_test_split


class domain_classifier:

    def __init__(self):

        self.DATA_DIR = "data"
        self.CKPT_DIR = path.join(self.DATA_DIR, "ckpt")
        bro_file = path.join(self.DATA_DIR, "bro.dat")
        good_urls_file = path.join(self.DATA_DIR, "top-1m.csv")

        DOMAIN_STR = 'Intel::DOMAIN'

        NGRAM_N = 3
        MAX_DOMAINS = 50000

        self.bad_domains = []
        self.good_domains = []

        with open(bro_file) as f:
            f.readline()  # first line is a comment. skip over it now
            for idx, line in enumerate(f):
                l = line.strip().split("\t")
                if len(l) is not 4:
                    continue

                if l[1] == DOMAIN_STR and len(self.bad_domains) < MAX_DOMAINS:
                    self.bad_domains.append(l[0].lower())

        with open(good_urls_file) as f:
            self.good_domains = []

            for idx, line in enumerate(f):
                if idx < MAX_DOMAINS:
                    good_domain = line.rstrip().split(",")[1].lower()
                    self.good_domains.append(good_domain)

        char_list = list("abcdefghijklmnopqrstuvwxyz1234567890.-")

        self.ngram_gen = NGram(N=NGRAM_N)

        n_perm = []
        for tup in itertools.product(char_list, repeat=NGRAM_N):
            n_perm.append("".join(tup))

        self.perm_lookup = {perm: idx for idx, perm in enumerate(n_perm)}
        self.feature_length = len(self.perm_lookup)

        self.data = data_vomit(self.good_domains, self.bad_domains)
        self.sess = tf.InteractiveSession()
        self._define_network()

    def _str2ngram(self, domains_arr):
        ngram_result = []
        for d in domains_arr:
            gram_result = np.zeros(self.feature_length)
            for gram in list(self.ngram_gen._split(d)):
                gram_result[self.perm_lookup[gram]] += 1
            ngram_result.append(gram_result)
        return ngram_result

    def _define_network(self):
        self.x = tf.placeholder(tf.float32, [None, self.feature_length])
        W1 = tf.Variable(tf.random_normal([self.feature_length, 1000]))
        b1 = tf.Variable(tf.random_normal([1000]))
        hl1 = tf.matmul(self.x, W1) + b1

        W2 = tf.Variable(tf.random_normal([1000, 500]))
        b2 = tf.Variable(tf.random_normal([500]))
        hl2 = tf.matmul(hl1, W2) + b2

        W3 = tf.Variable(tf.random_normal([500, 2]))
        b3 = tf.Variable(tf.random_normal([2]))
        self.y = tf.matmul(hl2, W3) + b3

        # regular cross entropy for reporting
        self.prob = tf.nn.softmax(self.y)

        # Define loss and optimizer
        self.y_ = tf.placeholder(tf.float32, [None, 2], name="correct_label")

        cross_entropy = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(self.y, self.y_))
        self.train_step = tf.train.AdamOptimizer().minimize(cross_entropy)

    def evaluate_success(self):
        correct_prediction = tf.equal(tf.argmax(self.y, 1),
                                      tf.argmax(self.y_, 1))
        accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
        return self.sess.run(accuracy, feed_dict={
                self.x: self._str2ngram(self.data.test.domains),
                self.y_: self.data.test.labels
            }) * 100

    def evaluate_domain(self, domain):
        return self.sess.run(self.prob, feed_dict={
                self.x: self._str2ngram([domain])
            })[0]

    def train(self):
        NUM_EPOCHS = 10
        MINIBATCH_SIZE = 200

        saver = tf.train.Saver()

        tf.initialize_all_variables().run()

        for i in range(NUM_EPOCHS):
            for _ in range(int(self.feature_length / MINIBATCH_SIZE)):
                batch_xs, batch_ys = self.data._next_batch(MINIBATCH_SIZE)
                self.sess.run(self.train_step, feed_dict={
                        self.x: self._str2ngram(batch_xs),
                        self.y_: batch_ys
                    })
            print("Epoch: " + str(i+1) + ": "
                  + str(self.evaluate_success()) + "%")

            saver.save(self.sess,
                       path.join(self.CKPT_DIR, "model.ckpt"),
                       global_step=i+1)

    def load_model(self):
        saver = tf.train.Saver()
        ckpt = tf.train.get_checkpoint_state(self.CKPT_DIR)
        if ckpt and ckpt.model_checkpoint_path:
            saver.restore(self.sess, ckpt.model_checkpoint_path)

# Data vomiterer
class data_vomit():

    def __init__(self, good_domains, bad_domains):

        class testing():
            def __init__(self):
                self.domains = []
                self.labels = []

        self.test = testing()
        self.data_feed = np.array([[d, 1] for d in good_domains] +
                                  [[d, 0] for d in bad_domains])
        np.random.shuffle(self.data_feed)
        self.X_train, self.test.domains, self.y_train, self.test.labels = train_test_split(self.data_feed[:, 0], self.data_feed[:, 1], test_size=0.03)

        self.test.labels = self._to_one_hot(self.test.labels)
        self.y_train = self._to_one_hot(self.y_train)

        self.loc = 0
        self.total_data = len(self.X_train)

    def _to_one_hot(self, arr):
        arr = np.array(arr, dtype=np.int8)
        result = np.zeros((len(arr), 2))
        result[np.arange(len(arr)), arr] = 1
        return result

    def _next_batch(self, n):
            if n + self.loc <= self.total_data:
                x = self.X_train[self.loc:self.loc+n]
                y = self.y_train[self.loc:self.loc+n]
                self.loc = (self.loc + n) % self.total_data
                return x, y
            else:
                x = np.append(self.X_train[self.loc:self.total_data],
                              self.X_train[0:n-self.total_data+self.loc])
                y = np.append(self.y_train[self.loc:self.total_data],
                              self.y_train[0:n-self.total_data+self.loc])
                self.loc = n-self.total_data+self.loc
                return x, y
