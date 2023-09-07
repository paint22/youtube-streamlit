import streamlit as st

import time

st.title('streamlit 超入門')

st.write('プレぐれすばーの表示')
'start!!'

latest_iteration=st.empty()
bar=st.progress(0)

for i in range(100):
    latest_iteration.text(f'Itetation{i+1}')
    bar.progress(i+1)
    time.sleep(0.1)

'Done!!!!!!!'

left_column, right_column = st.columns(2)
button=left_column.button('右カラムに文字を表示')
if button:
    right_column.write('ここは右カラム')

expander=st.expander('問い合わせ')
expander.write('問い合わせ内容を書く')
# text=st.text_input('あなたの趣味を教えてください')
# 'あなたの趣味:',text

# condition=st.sidebar.slider('あなたの今の調子は？',0,100,50)
# 'コンディション：',condition
# if st.checkbox('show Image'):
#     img = Image.open('ao.jpg')
#     st.image(img, caption='Ao', use_column_width=True)
