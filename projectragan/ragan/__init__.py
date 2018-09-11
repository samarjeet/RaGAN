import tensorflow as tf
import numpy as np


def sample_Z(m,n):
    return np.random.uniform(-1., 1., size=[m,n])

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


    # Loss functions
    disc_loss = tf.reduce_mean(
        tf.nn.sigmoid_cross_entropy_with_logits(
            logits=r_logits, labels=tf.ones_like(r_logits)) + 
        tf.nn.sigmoid_cross_entropy_with_logits(
            logits=f_logits, labels=tf.zeros_like(f_logits))) 

    #print(disc_loss)    

    gen_loss = tf.reduce_mean(
        tf.nn.sigmoid_cross_entropy_with_logits(
            logits=f_logits, labels=tf.ones_like(f_logits)))

    #print(gen_loss)    
    # Optimizers
    gen_vars = tf.get_collection(tf.GraphKeys.GLOBAL_VARIABLES,
        scope="GAN/Generator")
    disc_vars = tf.get_collection(tf.GraphKeys.GLOBAL_VARIABLES,
        scope="GAN/Discriminator")

    gen_step = tf.train.RMSPropOptimizer(learning_rate=0.001).minimize(gen_loss, 
        var_list=gen_vars) # G train step
    disc_step = tf.train.RMSPropOptimizer(learning_rate=0.001).minimize(disc_loss, 
        var_list=disc_vars) # G train step


    #Session
    sess = tf.Session()
    tf.global_variables_initializer().run(session=sess)

    # Training the network
    batch_size=256
    nd_steps = 10
    ng_steps = 10
    for i in range(10001):
        X_batch = sample_data(n=batch_size);
        Z_batch = sample_Z(batch_size, 2);

        for _ in range(nd_steps):
            _ ,dloss = sess.run([disc_step, disc_loss], 
                feed_dict={X:X_batch, Z:Z_batch})

        rrep_gstep, grep_step  = sess.run([r_rep, g_rep], 
            feed_dict={X:X_batch, Z:Z_batch})

        for _ in range(ng_steps):
            _ ,gloss = sess.run([gen_step, gen_loss], 
                feed_dict={Z:Z_batch})

        rrep_gstep, grep_step  = sess.run([r_rep, g_rep], 
            feed_dict={X:X_batch, Z:Z_batch})

        print("Iteration: %d\t Discriminator loss: %.4f\t Generator loss: %.4f"%(i, dloss, gloss))


main();
