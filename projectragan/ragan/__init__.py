import tensorflow as tf
import numpy as np


def get_y(x):
    return 10 + x*x;

def sample_data(n=10000, scale=100):
    data = []

    x = scale*(np.random.random_sample((n,))-0.5)

    for i in range(n):
        yi = get_y(x[i])
        data.append([x[i], yi])

    return np.array(data)

def generator(Z, hsize=[16,16]):
    with tf.variable_scope("GAN/Generator", reuse=False):
        h1 = tf.layers.dense(Z,hsize[0], activation=tf.nn.leaky_relu)
        h2 = tf.layers.dense(h1,hsize[1], activation=tf.nn.leaky_relu)
        out = tf.layers.dense(h2,2)
    return out

def discriminator(X, hsize=[16,16], reuse=False):
    with tf.variable_scope("GAN/Discriminator", reuse=reuse):
        h1 = tf.layers.dense(X, hsize[0],activation=tf.nn.leaky_relu)
        h2 = tf.layers.dense(h1,hsize[1],activation=tf.nn.leaky_relu)
        h3 = tf.layers.dense(h2,2)
        out = tf.layers.dense(h3,1)
    return out, h3

def main():
    print("Hello World from RaGAN")
    a = sample_data()
    X = tf.placeholder(tf.float32, [None,2])
    Z = tf.placeholder(tf.float32, [None,2])
    G_sample = generator(Z )
    r_logits, r_rep = discriminator(X)
    f_logits, g_rep = discriminator(G_sample, reuse=True)

    disc_loss = tf.reduce_mean(
        tf.nn.sigmoid_cross_entropy_with_logits(
            logits=r_logits, labels=tf.ones_like(r_logits)) + 
        tf.nn.sigmoid_cross_entropy_with_logits(
            logits=f_logits, labels=tf.zeros_like(f_logits))) 

    #print(disc_loss)    

    gen_loss = tf.reduce_mean(
        tf.nn.sigmoid_cross_entropy_with_logits(
            logits=f_logits, labels=tf.ones_like(f_logits)))

    print(gen_loss)    

main();
