from pointnet.model_cls import PointNet
import os
import numpy as np
import pickle
import tensorflow as tf
nb_classes = 40

#读off
def read_off(filename):
    points = []
    with open(filename, 'r') as f:
        f.readline()
        n, m, c = f.readline().rstrip().split(' ')[:]
        n = int(float(n))
        for i in range(n):
            value = f.readline().rstrip().split(' ')
            points.append([float(x) for x in value])
    points = np.array(points)
    # centroid = np.mean(points, axis=0)
    # points_unit_sphere = points - centroid
    # furthest_distance = np.max(np.sqrt(np.sum(abs(points) ** 2, axis=-1)))
    # points_unit_sphere /= furthest_distance
    # npoints = 2048
    # points = points_unit_sphere
    # choice = np.random.choice(len(points), npoints, replace=True)
    # # points_subset = points[choice, :]
    # # print(type(points_subset))
    xyz = points.copy()
    points_farthest_index = farthest_point_sample(xyz, 2048).astype(np.int64)
    points_farthest = xyz[points_farthest_index, :]
    # 单位圆化
    centroid = np.mean(points_farthest, axis=0)
    points_unit_sphere = points_farthest - centroid
    furthest_distance = np.max(np.sqrt(np.sum(abs(points_farthest) ** 2, axis=-1)))
    points_unit_sphere /= furthest_distance
    return list(points_unit_sphere)

#最远点采样
def farthest_point_sample(xyz, npoint):
    N, C = xyz.shape
    centroids = np.zeros(npoint)
    distance = np.ones(N) * 1e10
    farthest = np.random.randint(0, N)# random select one as centroid
    for i in range(npoint):
        centroids[i] = farthest
        centroid = xyz[farthest, :].reshape(1, 3)
        dist = np.sum((xyz - centroid) ** 2, -1)
        mask = dist < distance
        distance[mask] = dist[mask]
        farthest = np.argmax(distance)# select the farthest one as centroid
        #print('index:%d, dis:%.3f'%(farthest,np.max(distance)))
    return centroids
#测试类
class Test():
    # 构造函数
    def __init__(self):
        self.graph = tf.get_default_graph()
        self.model = PointNet(nb_classes)
        # 加载模型权重
        self.model.load_weights('./results/pointnet.h5')
        fr = open('train_labels_name.pkl', 'rb')
        self.labels_name = pickle.load(fr)
        fr.close()



    # 预测
    def Predict(self):
        points = read_off('test/test.off')
        import show
        show.pyplot_draw_point_cloud(np.array(points),'static/test.png')
        test_points_r = np.array(points).reshape(-1, 2048, 3)
        #flask django 必须加，原因未知
        with self.graph.as_default():
            name=self.labels_name[np.argmax(self.model.predict(test_points_r), axis=1)[0]]
        return name


