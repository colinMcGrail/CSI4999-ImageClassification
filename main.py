import streamlit as st
from keras.models import load_model
from PIL import Image
import numpy as np

from util import classify, set_background

st.title('Osteoarthritis classification')
st.header('Upload your file here')

file = st.file_uploader('', type=['jpeg', 'jpg', 'png'])
model = load_model('./model/osteoarthritis.h5')
with open('./model/labels.txt') as f:
    class_names = [a[:-1].split(' ')[1] for a in f.readlines()]
    f.close()

if file is not None:
    image = Image.open(file).convert('RGB')
    st.image(image, use_column_width=True)

    class_name, conf_score = classify(image, model, class_names)

    st.write("## {}".format(class_name))
    st.write("### score: {}%".format(int(conf_score * 1000) / 10))

