import tensorflow as tf

def build_model(inference=False, num_players=1):

    learning_rate = 0.0006

    frames = tf.placeholder(tf.float32, [None, 128, 128, 5])
    can_afford = tf.placeholder(tf.float32, [None, 3])
    turns_left = tf.placeholder(tf.float32, [None, 1])
    my_ships = tf.placeholder(tf.uint8, [None, 128, 128, 1])
    
    my_ships = tf.cast(my_ships, tf.float32)

    moves = tf.placeholder(tf.uint8, [None, 128, 128, 1])
    generate = tf.placeholder(tf.float32, [None, 1])
    is_training = tf.placeholder(tf.bool)

    tf.add_to_collection('frames', frames)
    tf.add_to_collection('can_afford', can_afford)
    tf.add_to_collection('turns_left', turns_left)
    tf.add_to_collection('my_ships', my_ships)
    tf.add_to_collection('moves', moves)
    tf.add_to_collection('generate', generate)
    tf.add_to_collection('is_training', is_training)

    moves = tf.one_hot(moves, 6)

    ca = tf.layers.dense(can_afford, 16)
    tl = tf.layers.dense(turns_left, 16)

    ca = tf.expand_dims(ca, 1)
    ca = tf.expand_dims(ca, 1)
    tl = tf.expand_dims(tl, 1)
    tl = tf.expand_dims(tl, 1)

    d_l2_a_1 = tf.layers.conv2d(frames, 64, 3, activation=tf.nn.relu, padding='same', name='c1') # 128
    d_l2_a_1 = tf.layers.batch_normalization(d_l2_a_1, training=is_training, name='bn1')

    d_l2_p = tf.layers.conv2d(d_l2_a_1, 32, 3, strides=2, activation=tf.nn.relu, padding='same', name='c4') # 64
    d_l2_p = tf.layers.batch_normalization(d_l2_p, training=is_training, name='bn4')

    d_l3_a = tf.layers.conv2d(d_l2_p, 32, 3, activation=tf.nn.relu, padding='same', name='c5')
    d_l3_a = tf.layers.batch_normalization(d_l3_a, training=is_training, name='bn5')
    d_l3_p = tf.layers.conv2d(d_l3_a, 32, 3, strides=2, activation=tf.nn.relu, padding='same', name='c6') # 32
    d_l3_p = tf.layers.batch_normalization(d_l3_p, training=is_training, name='bn6')

    d_l4_a = tf.layers.conv2d(d_l3_p, 32, 3, activation=tf.nn.relu, padding='same', name='c7')
    d_l4_a = tf.layers.batch_normalization(d_l4_a, training=is_training, name='bn7')
    d_l4_p = tf.layers.conv2d(d_l4_a, 32, 3, strides=2, activation=tf.nn.relu, padding='same', name='c8') # 16
    d_l4_p = tf.layers.batch_normalization(d_l4_p, training=is_training, name='bn8')

    d_l5_a = tf.layers.conv2d(d_l4_p, 32, 3, activation=tf.nn.relu, padding='same', name='c9')
    d_l5_a = tf.layers.batch_normalization(d_l5_a, training=is_training, name='bn9')
    d_l5_p = tf.layers.conv2d(d_l5_a, 32, 3, strides=2, activation=tf.nn.relu, padding='same', name='c10') # 8
    d_l5_p = tf.layers.batch_normalization(d_l5_p, training=is_training, name='bn10')

    d_l6_a = tf.layers.conv2d(d_l5_p, 64, 3, activation=tf.nn.relu, padding='same', name='c11')
    d_l6_a = tf.layers.batch_normalization(d_l6_a, training=is_training, name='bn11')
    d_l6_p = tf.layers.conv2d(d_l6_a, 64, 3, strides=2, activation=tf.nn.relu, padding='same', name='c12') # 4
    d_l6_p = tf.layers.batch_normalization(d_l6_p, training=is_training, name='bn12')

    d_l7_a = tf.layers.conv2d(d_l6_p, 128, 3, activation=tf.nn.relu, padding='same', name='c13')
    d_l7_a = tf.layers.batch_normalization(d_l7_a, training=is_training, name='bn13')
    d_l7_p = tf.layers.conv2d(d_l7_a, 128, 3, strides=2, activation=tf.nn.relu, padding='same', name='c14') # 2
    d_l7_p = tf.layers.batch_normalization(d_l7_p, training=is_training, name='bn14')

    d_l8_a_2 = tf.layers.conv2d(d_l7_p, 128, 3, activation=tf.nn.relu, padding='same', name='c16')
    d_l8_a_2 = tf.layers.batch_normalization(d_l8_a_2, training=is_training, name='bn16')
    d_l8_p = tf.layers.conv2d(d_l8_a_2, 128, 3, strides=2, activation=tf.nn.relu, padding='same', name='c17') # 1
    d_l8_p = tf.layers.batch_normalization(d_l8_p, training=is_training, name='bn17')

    final_state = tf.concat([d_l8_p, ca, tl], -1)
    latent = tf.layers.dense(final_state, 256, activation=tf.nn.relu, name='c19')

    u_l8_a = tf.layers.conv2d_transpose(latent, 128, 3, 2, activation=tf.nn.relu, padding='same', name='c20') # 2
    u_l8_c = tf.concat([u_l8_a, d_l8_a_2], -1)
    u_l8_s = tf.layers.conv2d(u_l8_c, 128, 3, activation=tf.nn.relu, padding='same', name='c21')
    u_l8_s = tf.layers.batch_normalization(u_l8_s, training=is_training, name='bn18')

    u_l7_a = tf.layers.conv2d_transpose(u_l8_s, 128, 3, 2, activation=tf.nn.relu, padding='same', name='c22') # 4
    u_l7_c = tf.concat([u_l7_a, d_l7_a], -1)
    u_l7_s = tf.layers.conv2d(u_l7_c, 128, 3, activation=tf.nn.relu, padding='same', name='c23')
    u_l7_s = tf.layers.batch_normalization(u_l7_s, training=is_training, name='bn19')

    u_l6_a = tf.layers.conv2d_transpose(u_l7_s, 64, 3, 2, activation=tf.nn.relu, padding='same', name='c24') # 8
    u_l6_c = tf.concat([u_l6_a, d_l6_a], -1)
    u_l6_s = tf.layers.conv2d(u_l6_c, 64, 3, activation=tf.nn.relu, padding='same', name='c25')
    u_l6_s = tf.layers.batch_normalization(u_l6_s, training=is_training, name='bn20')

    u_l5_a = tf.layers.conv2d_transpose(u_l6_s, 64, 3, 2, activation=tf.nn.relu, padding='same', name='c26') # 16
    u_l5_c = tf.concat([u_l5_a, d_l5_a], -1)
    u_l5_s = tf.layers.conv2d(u_l5_c, 64, 3, activation=tf.nn.relu, padding='same', name='c27')
    u_l5_s = tf.layers.batch_normalization(u_l5_s, training=is_training, name='bn21')

    u_l4_a = tf.layers.conv2d_transpose(u_l5_s, 64, 3, 2, activation=tf.nn.relu, padding='same', name='c28') # 32
    u_l4_c = tf.concat([u_l4_a, d_l4_a], -1)
    u_l4_s = tf.layers.conv2d(u_l4_c, 64, 3, activation=tf.nn.relu, padding='same', name='c29')
    u_l4_s = tf.layers.batch_normalization(u_l4_s, training=is_training, name='bn22')

    u_l3_a = tf.layers.conv2d_transpose(u_l4_s, 64, 3, 2, activation=tf.nn.relu, padding='same', name='30') # 64
    u_l3_c = tf.concat([u_l3_a, d_l3_a], -1)
    u_l3_s = tf.layers.conv2d(u_l3_c, 64, 3, activation=tf.nn.relu, padding='same', name='c31')
    u_l3_s = tf.layers.batch_normalization(u_l3_s, training=is_training, name='bn23')

    u_l2_a = tf.layers.conv2d_transpose(u_l3_s, 64, 3, 2, activation=tf.nn.relu, padding='same', name='c32') # 128
    u_l2_c = tf.concat([u_l2_a, d_l2_a_1], -1)
    u_l2_s_1 = tf.layers.conv2d(u_l2_c, 128, 3, activation=tf.nn.relu, padding='same', name='c33')
    u_l2_s_1 = tf.layers.batch_normalization(u_l2_s_1, training=is_training, name='bn24')
    u_l2_s_2 = tf.layers.conv2d(u_l2_s_1, 128, 3, activation=tf.nn.relu, padding='same', name='c34')
    u_l2_s_2 = tf.layers.batch_normalization(u_l2_s_2, training=is_training, name='bn25')
    
    player_generate_logits = []
    player_move_logits = []
    for i in range(num_players):

        gen_latent = tf.layers.dense(latent, 64, activation=tf.nn.relu, name='c39_{}'.format(i))
        generate_logits = tf.layers.dense(gen_latent, 1, activation=None, name='c40_{}'.format(i))
        generate_logits = tf.squeeze(generate_logits, [1, 2])

        moves_latent = tf.layers.conv2d(u_l2_s_2, 64, 3, activation=tf.nn.relu, padding='same', name='c41_{}'.format(i)) # Try 1 kernel
        moves_logits = tf.layers.conv2d(moves_latent, 6, 3, activation=None, padding='same', name='c42_{}'.format(i)) # Try 1 kernel
    
        player_generate_logits.append(generate_logits)
        player_move_logits.append(moves_logits)

    tf.add_to_collection('m_logits', tf.stack(player_move_logits))
    tf.add_to_collection('g_logits', tf.stack(player_generate_logits))
    tf.add_to_collection('latent', latent)
    
    if inference:
        return

    # TODO: Can be improved with gather_nd
    moves_logits = [tf.split(x, num_players) for x in player_move_logits]
    generate_logits = [tf.split(x, num_players) for x in player_generate_logits]

    moves_logits = [x[i] for x, i in zip(moves_logits, range(num_players))]
    generate_logits = [x[i] for x, i in zip(generate_logits, range(num_players))]

    moves_logits = tf.concat(moves_logits, 0)
    generate_logits = tf.concat(generate_logits, 0)

    losses = tf.nn.softmax_cross_entropy_with_logits_v2(labels=moves,
                                                logits=moves_logits,
                                                dim=-1)

    losses = tf.expand_dims(losses, -1)

    masked_loss = losses * my_ships

    ships_per_frame = tf.reduce_sum(my_ships, axis=[1, 2])

    frame_loss = tf.reduce_sum(masked_loss, axis=[1, 2])

    average_frame_loss = frame_loss / tf.maximum(ships_per_frame, 1e-13) # First frames have no ship

    generate_losses = tf.nn.sigmoid_cross_entropy_with_logits(labels=generate, logits=generate_logits)

    sanity_gen_loss = tf.reduce_mean(tf.split(generate_losses, 3)[0])
    sanity_average_frame_loss = tf.reduce_mean(tf.split(average_frame_loss, 3)[0])
    
    generate_losses = tf.reduce_mean(generate_losses) # TODO: do I need to add to frames before averaging?

    loss = tf.reduce_mean(average_frame_loss) + 0.03*generate_losses

    sanity_loss = sanity_average_frame_loss + 0.03*sanity_gen_loss
    
    vars = [tf.nn.l2_loss(v) for v in tf.trainable_variables()
                    if 'bias' not in v.name and 'c' == v.name[0]]
    L2_loss = tf.add_n(vars) * 0.0000001
    
    loss += L2_loss
    
    update_ops = tf.get_collection(tf.GraphKeys.UPDATE_OPS)
    with tf.control_dependencies(update_ops):
        optimizer = tf.train.AdamOptimizer(learning_rate).minimize(loss)

    tf.add_to_collection('loss', loss)
    tf.add_to_collection('sanity_loss', sanity_loss)
    tf.add_to_collection('optimizer', optimizer)

    return


