import numpy as np
import timeit

from sklearn import svm
import struct       #modun dung de dinh dạng ban ghi nhi phan , giai nen du lieu #https://www.geeksforgeeks.org/struct-module-python/
import pickle
from skimage import io


TRAIN_ITEMS = 60000
TEST_ITEMS = 10000
# train-images-idx3-ubyte: đào tạo tập hình ảnh
# đào tạo-nhãn-idx1-ubyte: nhãn tập huấn luyện
# t10k-images-idx3-ubyte: kiểm tra tập hình ảnh
# t10k-labels-idx1-ubyte: nhãn thiết lập thử
#Tập huấn luyện có 60000, bài kiểm tra 10000

######################################## Read data MNIST ##########################################
def loadMnistData():
    mnist_data = []
    for img_file,label_file,items in zip(['data/train-images-idx3-ubyte','data/t10k-images-idx3-ubyte'],
                                   ['data/train-labels-idx1-ubyte','data/t10k-labels-idx1-ubyte'],
                                   [TRAIN_ITEMS, TEST_ITEMS]):
        data_img = open(img_file, 'rb').read()
        data_label = open(label_file, 'rb').read()

        fmt = '>iiii'
        offset = 0
        magic_number, img_number, height, width = struct.unpack_from(fmt, data_img, offset)
       
        offset += struct.calcsize(fmt)
      
        image_size = height * width
      
        fmt = '>{}B'.format(image_size)
     
        if items > img_number:
            items = img_number
        images = np.empty((items, image_size))
        for i in range(items):
            images[i] = np.array(struct.unpack_from(fmt, data_img, offset))
           
            images[i] = images[i]/256
            # images[i] = images[i]
            offset += struct.calcsize(fmt)


        fmt = '>ii'
        offset = 0
        magic_number, label_number = struct.unpack_from(fmt, data_label, offset)
        # print('magic number is {} and label number is {}'.format(magic_number, label_number))
       
        offset += struct.calcsize(fmt)
        #B means unsigned char
        fmt = '>B'
       
        if items > label_number:
            items = label_number
        labels = np.empty(items)
        for i in range(items):
            labels[i] = struct.unpack_from(fmt, data_label, offset)[0]
            offset += struct.calcsize(fmt)
        
        mnist_data.append((images, labels.astype(int)))
    return mnist_data

######################################## Train data ##########################################
def train_model():
    start_time = timeit.default_timer()
    print("start_time: ", start_time) #19293.887149361

    training_data, test_data = loadMnistData()
    print("training_data: ", training_data)
    print("test_data: ", test_data)

    # train
    # classifier = svm.SVC()        #9443 trong  10000 gía trị đúng.
    classifier = svm.SVC(C=200,kernel='rbf',gamma=0.01,cache_size=8000,probability=False) #9824 trong 10000 gía trị đúng.

    # cho nó học từ images và label của data train
    classifier.fit(training_data[0], training_data[1])         
    train_time = timeit.default_timer()
    print("train_time: ", train_time)       #19672.935809503
    print('gemfield train cost {}'.format(str(train_time - start_time) ) )

    # test
    print("Bắt đầu test!")
    pickle.dump(classifier, open("handwrite_model", 'wb'))

    #cho ra các label của test gọp lại thành mảng
    predictions = classifier.predict(test_data[0])
    predictions = []
    for a in classifier.predict(test_data[0]):
        predictions.append(a)
    print("PREDICT %r" % predictions)

    # so sánh cái mảng các label vừa được dự đoán được với mảng label mà ban đầu đã cho để xem có đúng thay hông??
    i = 0
    for a, y in zip(predictions, test_data[1]):
        if a == y:
            i = i + 1
    num_correct = i
    # print("predictions", predictions)  # [7,2,1,..]
    print("%s trong %s gía trị đúng." % (num_correct, len(test_data[1])))      

    test_time = timeit.default_timer()
    print('gemfield test cost {}'.format(str(test_time - train_time) ) )          #gemfield test cost 206.6903916629999


##################################### Pham tram test dat dua vao train data ##############################
def test_model():
    classifier = pickle.load(open("handwrite_model", 'rb'))
    training_data, test_data = loadMnistData()
    result = classifier.score(test_data[0], test_data[1])
    print(result)


##################################### Test image ##############################
def predict_image(img):
    logo = img
    if type(img) is str:
        logo = io.imread(img)
    classifier = pickle.load(open("handwrite_model", 'rb'))
    show_image(logo)
    logo = logo.reshape(1, -1)
    result = classifier.predict(logo)
    print("RESULT %r" % result)
    return result


def show_image(img):
    logo = img.reshape(28, 28)
    print(logo.shape)
    print(len(logo[0]))
    for i in range(logo.shape[0]):
        for j in range(logo.shape[1]):
            if logo[i][j] > 0.0:
                print("@", end="");
            else:
                print("-", end="");
        print()


training_data, test_data = loadMnistData()
predict_image(test_data[0][10])

# def image_predict_image(img):
#     logo = img
#     if type(img) is str:
#         logo = io.imread(img, as_grey=True)
#     classifier = pickle.load(open("handwrite_model", 'rb'))
#     logo_train = (logo*256).reshape(1, -1)
#     total_pixel = 28*28
#     logo_train_chia = [[0 for _ in range(total_pixel)]]
#     for i in range(total_pixel):
#         logo_train_chia[0][i] = logo_train[0][i] / 256

#     show_image(logo)

#     result = classifier.predict(logo_train_chia)
#     print("RESULT %r" % result)
#     return result[0]


















# def show_image1(img):
#     logo = img
#     if type(img) is str:
#         logo = io.imread(img)

#     show_image(logo)







####-----------------------
#-------- De train du lieu----------------------
# train_model()
#-------- 
# test_model()
#-------- Doc du lieu tu bo du lieu MNist--------
# training_data, test_data = loadMnistData()

#--------
# print(test_data[1][221:400])
# print(test_data[0][45])
# show_image(test_data[0][45])

#-------- Doan anh la so nao? -------------------
# predict_image(test_data[0][10])

#-------- Chia anh cho 256 roi Doan anh la so nao------
# image_predict_image("/home/admin/teo/images/image_0.jpg")

#dung
# image_predict_image("/home/teo/STUDY/digit_prediction/temp.jpg")




#thu
# logo = io.imread("/home/teo/STUDY/digit_prediction/temp.jpg", as_grey=True)
# logo1 = misc.imresize(logo, (28,28))
# image_predict_image(logo1)
# print(logo.shape)       #28*28